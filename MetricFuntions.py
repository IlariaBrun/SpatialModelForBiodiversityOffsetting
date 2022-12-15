"""
Set of functions computing different landscape metrics 
 
"""
import numpy as np
import math
from scipy import ndimage
import scipy
from sklearn.metrics.pairwise import euclidean_distances




#this function give the array of a given class
def class_selection(band,classes,nodata,cl):
    if cl in classes:
#        print("Working with class ",cl)
        cl_array = np.copy(band) # create working array
#        cl_array[cl_array==int(nodata)] = 0
        cl_array[band!=cl] = 0 
        return cl_array
    else:
        print("Invalid class!")

#This function takes in input a class array and labels it 
#so that each patch has a label
def f_ccl(self,cl_array,s=2):
        # Binary structure
        self.cl_array = cl_array
        struct = scipy.ndimage.generate_binary_structure(s,s)
        self.labeled_array, self.numpatches = ndimage.label(cl_array,struct)
        return struct, self.labeled_array, self.numpatches

# Return array with a specific labeled patch
def returnPatch(labeled_array,patch):
    # Make an array of zeros the same shape as `a`.
    feature = np.zeros_like(labeled_array, dtype=int)
    feature[labeled_array == patch] = 1
    return feature
      
####################################################################################################
######DIVERSITY#######################################################################################
#################################################################################################### 
def diversity_index(band,classes,index,nodata):
    if(index=="shannon"):
        sh = []
        cl_array = np.copy(band) # create working array
        cl_array[cl_array==int(nodata)] = 0
        for cl in classes:
            if cl == 0: # If class 0 exists
                arr = np.zeros_like(band)
                arr[band==cl] = 1
            else:
                arr = np.copy(band)
                arr[band!=cl] = 0
            prop = np.count_nonzero(arr) / np.count_nonzero(cl_array)
#            prop = np.count_nonzero(arr) / float(sum(res))
            if prop !=0:
                sh.append(prop * math.log(prop))
            shannon=float(sum(sh)*-1)
        return  shannon#, cl_array, (sum(res))
    elif (index=="simpson"):
        si = []
        cl_array = np.copy(band) # create working array
        cl_array[cl_array==int(nodata)] = 0
        for cl in classes:
            if cl == 0: # If class 0 exists
                arr = np.zeros_like(band)
                arr[band==cl] = 1
            else:
                arr = np.copy(band)
                arr[band!=cl] = 0
            prop = np.count_nonzero(arr) / np.count_nonzero(cl_array)
#            prop = np.count_nonzero(arr) / float(sum(res))
            if prop !=0:
                si.append(math.pow(prop,2))
        return float(1-sum(si))
#    elif(index=="eveness"):
#        return self.f_returnDiversity("shannon",nodata) / math.log(len(classes))

####################################################################################################
########EDGES#######################################################################################
####################################################################################################        
def setBorderZero(matrix):
    heightFP,widthFP = matrix.shape #define hight and width of input matrix
    withBorders = np.ones((heightFP+2,widthFP+2))*0 # set the border to borderValue
    withBorders[1:heightFP+1,1:widthFP+1]=matrix # set the interior region to the input matrix
    return withBorders    
  
# Returns sum of patches perimeter
def PatchPerimeter(self,labeled_array):
    labeled_array = self.setBorderZero(labeled_array) # make a border with zeroes
    TotalPerimeter = np.sum(labeled_array[:,1:] != labeled_array[:,:-1]) + np.sum(labeled_array[1:,:] != labeled_array[:-1,:])
    return TotalPerimeter
    
      # Returns total Edge length
def EdgeLength(self,labeled_array, cellsize):
    TotalEdgeLength = self.PatchPerimeter(self,labeled_array)
    #Todo: Mask out the boundary cells
    return TotalEdgeLength *cellsize

####################################################################################################
########PATCHES AREA#######################################################################################
####################################################################################################        

# Return greatest, smallest or mean patch area 
def PatchArea(self,cl_array,labeled_array,numpatches,what,cellsize,cl):
    cellsize2=math.pow(cellsize,2)
    sizes = ndimage.sum(cl_array,labeled_array,list(range(1,numpatches+1)))
    sizes = sizes[sizes!=0] # remove zeros
    if len(sizes) != 0:            
        if what=="max":
            return (np.max(sizes)*cellsize2) / int(cl)
        elif what=="min":
            return (np.min(sizes)*cellsize2) / int(cl)
        elif what=="mean":
            return (np.mean(sizes)*cellsize2) / int(cl)
        elif what=="median":
            return (np.median(sizes)*cellsize2) / int(cl)
    else:
        return None

#Return the total area for the given class
def returnArea(labeled_array,cellsize):
    cellsize2=float(math.pow(cellsize,2))
    #sizes = scipy.ndimage.sum(array, labeled_array, range(numpatches + 1)).astype(labeled_array.dtype)
    area = float(np.count_nonzero(labeled_array)*cellsize2)
    return area

# Aggregates all class area, equals the sum of total area for each class
def LandscapeArea(self,array,classes,cellsize):
    res = []
    for i in classes:
        arr = np.copy(array)
        arr[array!=i] = 0
        res.append(self.returnArea(arr,cellsize))
    Larea = float(sum(res))
#    array[cl_array==int(nodata)] = 0
    return Larea

def LargestPatchIndex(self,cl_array,classes,labeled_array,numpatches,cellsize,cl):
    ma = self.PatchArea(self,cl_array,labeled_array,numpatches,"max",cellsize,cl)
    Larea=self.LandscapeArea(self,cl_array,classes,cellsize)
    if Larea is None or ma is None :
        LPI=0
    else:
        LPI=float(( ma / Larea ) * 100)
    return LPI

    # Returns the proportion of the labeled class in the landscape
def cl_Proportion(self,array,cl):
    arr = np.copy(array)
    arr[array!=cl] = 0
    if np.count_nonzero(arr) == 0:
        prop=0
    elif np.count_nonzero(arr) != 0 :
#        print(np.count_nonzero(arr))
        prop = float(np.count_nonzero(arr)) / float(np.count_nonzero(array))*100
    return prop

# Average shape (ratio perimeter/area) of each patches of each lc-class
def AvgShape(self,labeled_array,cl_array, numpatches,correction):        
    perim = np.array([]).astype(float)
    for i in range(1,numpatches + 1): # Very slow!
            feature = self.returnPatch(labeled_array,i)
            p = np.sum(feature[:,1:] != feature[:,:-1]) + np.sum(feature[1:,:] != feature[:-1,:])
            perim = np.append(perim,p)        
    area = ndimage.sum(cl_array, labeled_array, list(range(numpatches + 1))).astype(float)
    area = area[area !=0]
    if correction:
        a = 0.25 * perim
        b = np.sqrt(area)
        d = np.divide(a,b).astype(float)
    else:
        d = np.divide(perim,area).astype(float)
    return np.mean(d)

####################################################################################################
########SUBDIVISON#######################################################################################
####################################################################################################        

# Returns the Landscape division Index for the given array
def LandscapeDivisionIndex(self,array,labeled_array,numpatches,classes,cl):
    res = []
    for i in classes:
        arr = np.copy(array)
        arr[array!=i] = 0
        res.append(np.count_nonzero(arr))
    Lcell = float(sum(res))
    res = []
    sizes = ndimage.sum(array,labeled_array,list(range(1,numpatches+1)))
    sizes = sizes[sizes!=0] # remove zeros
    for i in sizes:
        area = (i) / int(cl)
        val = math.pow(float(area) / Lcell,2)
        res.append(val)
    return (1 - sum(res)) 

# Returns the Splitting index for the given array
def SplittingIndex(self,array,numpatches,labeled_array,cl,cellsize,classes):
    cellsize2=cellsize*cellsize
    Larea=LandscapeArea(self,array,classes,cellsize) # Calculate LArea
    res = []
    sizes = ndimage.sum(array,labeled_array,list(range(1,numpatches+1)))
    sizes = sizes[sizes!=0] # remove zeros
    for i in sizes:
        area = (i*cellsize2) / int(cl)
        val = math.pow(area,2)
        res.append(val)
    area = sum(res)
    larea2 = math.pow(Larea,2)
    if area != 0:
        si = float(larea2) / float(area)
    else:
        si = None
    return si

# Returns the Effective Mesh Size Index for the given array
def EffectiveMeshSize(self,array,labeled_array,numpatches,cl,cellsize,classes):
    cellsize2=cellsize*cellsize
    Larea=LandscapeArea(self,array,classes,cellsize) # Calculate LArea
    res = []
    sizes = ndimage.sum(array,labeled_array,list(range(1,numpatches+1)))
    sizes = sizes[sizes!=0] # remove zeros
    for i in sizes:
        area = (i*cellsize2) / int(cl)
        res.append(math.pow(area,2))            
    Earea = sum(res)
    try:
        eM = float(Earea) / float(Larea)
    except ZeroDivisionError:
        eM = None
    return eM

def AvgPatchDist(self,labeled_array,numpatches,cellsize,metric = "euclidean"):
    #labeled array is the matrix of a class where patches are labeled (from 1 to num patches)
    if numpatches == 0:
        return np.nan
    elif numpatches < 2:
        return 0
    else:
        """
        Takes a labeled array as returned by scipy.ndimage.label and 
        returns an intra-feature distance matrix.
        Solution by @morningsun at StackOverflow
        """         
        I, J = np.nonzero(labeled_array)#the indices of the nonzero elements 
        labels = labeled_array[I,J] #[I reduce the matrix considering only nonzero values]
        coords = np.column_stack((I,J))#from two 1d arrays to a two comumns one
    
        sorter = np.argsort(labels)#the index of the sorted array
        labels = labels[sorter]
        coords = coords[sorter]
    
#        sq_dists = cdist(coords, coords, 'sqeuclidean')
        sq_dists =euclidean_distances(coords, coords, squared=True)
        start_idx = np.flatnonzero(np.r_[1, np.diff(labels)])   #flat non zero return indices that are non-zero in the flattened version of a         
        nonzero_vs_feat = np.minimum.reduceat(sq_dists, start_idx, axis=1)
        feat_vs_feat = np.minimum.reduceat(nonzero_vs_feat, start_idx, axis=0)
    
        # Get lower triangle and zero distances to nan
        b = np.tril( np.sqrt( feat_vs_feat ) )
        b[b == 0 ] = np.nan
        res = np.nanmean(b) * cellsize # Calculate mean and multiply with cellsize
    
        return res
        



def AvgNearNeigh(self,labeled_array,numpatches,cellsize,metric = "euclidean"):
    if numpatches == 0:
        return np.nan
    elif numpatches < 2:
        return 0
    else:
        for i in range (1, numpatches+1):
            for j in range(i+1, numpatches):
                patchi= self.returnPatch(labeled_array,i)
                patchi1= self.returnPatch(labeled_array,i+1)           
                I, J = np.nonzero(patchi)#the indices of the nonzero elements 
                labels = patchi[I,J] #[I reduce the matrix considering only nonzero values]
                coords = np.column_stack((I,J))#from two 1d arrays to a two comumns one        
                sorter = np.argsort(labels)#the index of the sorted array
                labels = labels[sorter]
                coords = coords[sorter]
                I1, J1 = np.nonzero(patchi1)#the indices of the nonzero elements 
                labels1 = patchi1[I,J] #[I reduce the matrix considering only nonzero values]
                coords1 = np.column_stack((I,J))#from two 1d arrays to a two comumns one        
                sorter1 = np.argsort(labels1)#the index of the sorted array
                labels1 = labels[sorter1]
                coords1 = coords[sorter1]        
        #        sq_dists = cdist(coords, coords, 'sqeuclidean')
                sq_dists =euclidean_distances(coords, coords1, squared=True)
#                print(sq_dists)
#                start_idx = np.flatnonzero(np.r_[1, np.diff(labels)])   #flat non zero return indices that are non-zero in the flattened version of a         
#                nonzero_vs_feat = np.minimum.reduceat(sq_dists, start_idx, axis=1)
#                feat_vs_feat = np.minimum.reduceat(nonzero_vs_feat, start_idx, axis=0)        
#                # Get lower triangle and zero distances to nan
#                b = np.tril( np.sqrt( feat_vs_feat ) )
#                b[b == 0 ] = np.nan
#                res = np.nanmean(b) * cellsize # Calculate mean and multiply with cellsize
#        return res

    # Calculates the Fractal dimension index patchwise
def FractalDimensionIndex(self, patch,cellsize):
    a = float( self.returnArea(patch,cellsize) )
    p = float( self.EdgeLength(self,patch,cellsize) )
    frac = ( 2.0 * np.log( 0.25 * p ) ) / np.log( a )     
    return frac
    
    # Calculates the Fractal dimension index patchwise
def MeanFractalDimensionIndex(self,cl_array,labeled_array,numpatches,cellsize):
    # Calculate patchwise
    frac = np.array([]).astype(float)
    for i in range(1,numpatches + 1): # Very slow!
        feature = self.returnPatch(labeled_array,i)
        a = float( self.returnArea(feature,cellsize) )
        p = float( self.EdgeLength(self,feature,cellsize) )
        fdi = ( 2.0 * np.log( 0.25 * p ) ) / np.log( a )
        frac = np.append(frac,fdi)        
    return np.mean(frac)

# Return greatest, smallest or mean patch area
def f_returnPatchArea(self,cl_array,labeled_array,numpatches,what):
    sizes = ndimage.sum(cl_array,labeled_array,list(range(1,numpatches+1)))
    sizes = sizes[sizes!=0] # remove zeros
    if len(sizes) != 0:            
        if what=="max":
            return (numpy.max(sizes)*self.cellsize_2) / int(self.cl)
        elif what=="min":
            return (numpy.min(sizes)*self.cellsize_2) / int(self.cl)
        elif what=="mean":
            return (numpy.mean(sizes)*self.cellsize_2) / int(self.cl)
        elif what=="median":
            return (numpy.median(sizes)*self.cellsize_2) / int(self.cl)
    else:
        return None

# Internal edge
def f_returnInternalEdge(self,cl_array):
    # Internal edge: Count of neighboring non-zero cell       
    kernel = ndimage.generate_binary_structure(2, 1) # Make a kernel
    kernel[1, 1] = 0
    b = ndimage.convolve(cl_array, kernel, mode="constant")
    n_interior = b[cl_array != 0].sum() # Number of interiror edges
    return n_interior    
    # Calculate the cohesion index    
# Hint: Likely wrong behaviour of internal edges

def CohesionIndex(self,cl_array,labeled_array,numpatches):
#    if np.count_nonzero(cl_array)
    # First calculate internal edges and number of cells of each patch
    internalEdges = np.array([]).astype(float)
    areas = np.array([]).astype(float)
    for i in range(1,numpatches + 1): # Very slow!
        feature = self.returnPatch(labeled_array,i)
        areas = np.append(areas, float( np.count_nonzero(feature) ) )
        #i've changed the original function here, by considering the EXTERNAL perimeter. it works better (even if ther's still a small error)
        internalEdges = np.append(internalEdges, float( self.PatchPerimeter(self,feature) ) )
#        internalEdges = np.append(internalEdges, float( self.f_returnInternalEdge(self,feature) ) )
    Larea = cl_array.size # The total number of cells in the landscape
    val = float((1-(np.sum(internalEdges)/np.sum(np.multiply(internalEdges,np.sqrt(areas)))) )*pow(1-1/np.sqrt(Larea),-1)*100)
    return val
