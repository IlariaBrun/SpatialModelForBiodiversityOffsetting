# -*- coding: utf-8 -*-
"""
(1) Forêt de feuillus
(2) Forêt de conifères
(3) Prairies
(4) Vergers
(5) Cultures saisonnières
(6) Urbain
"""
import numpy as np
import MetricFuntions as mf

#chckcrop returns:
#int_list= a vector with the tobal number of pixels for each land use of a given plot of land, i.e.
#int_list[0]= tot number of pixels of LU1 of "fixid" plot
#int_list[1]= tot number of pixels of LU2 of "fixid" plot...
#totopix=all the pixels of that plot of land
def checkcrop(fixid, idband, band) :    
    #Parameters setting 
    int_list=np.zeros(6)    
    for i in range (0,idband.shape[0]):
        for j in range (0,idband.shape[1]):
            if idband[i][j]==str(fixid) :
                for k in range(1,7):
                    if band[i][j]==k:
                        int_list[k-1]+=1
    totpix=np.sum(int_list)
    return int_list, totpix

def cropShape(gshape, idband, band, cellsize):
    ssize=0
    matrix=np.zeros(band.shape)
    for i in range (0,idband.shape[0]):
        for j in range (0,idband.shape[1]):
            if idband[i][j]==str(gshape) :
                ssize+=1
                matrix[i][j]=1                
    sshape=float(mf.FractalDimensionIndex(mf,matrix,cellsize))
#    print("sshape = ",sshape)
#    print("ssize=",ssize)
    return sshape, ssize

#select_crops return a list of plotos of land of a given size and a given shape
def select_crops(gsize, gshape, idlist, idband, band, cellsize):
    it=0
    parcelle=list()
    sizes=list()
    shapes=list()
    for shape in idlist:
        matrix=np.zeros(band.shape)
        print(it)
        urban=0
        ssize=0
        for i in range (0,idband.shape[0]):
            for j in range (0,idband.shape[1]):
                if idband[i][j]==str(shape) :
                    ssize+=1
                    matrix[i][j]=1
                    if band[i][j]==6:
                        urban+=1
#        print("ssize=",ssize)
#        print("urb= ",urban)
        if ssize !=0 and urban/ssize<0.1:                     
            sshape=float(mf.FractalDimensionIndex(mf,matrix,cellsize))
#            print("ssize=",ssize)
            if gsize-3 <= ssize <= gsize+3 and (gshape - 0.05)< sshape<(gshape+ 0.05) :
                parcelle.append(shape)
                shapes.append(sshape)
                sizes.append(ssize)
                print("sshape = ",sshape)
#                print("sshape = ",sshape)
#                print("ssize=",ssize)
                it+=1
#        else: 
#            print("Already urbanized or no intersection!")
        if it ==20:
            break
    print(len(parcelle))
    return parcelle, shapes, sizes
#    np.save("communes/crops_"+str(gsize)+"p_"+str(gshape), parcelle)
    

#select crop return a list of plotos of land of a given size and a given shape
def select_cropsDiff(gsize, gshape, idlist, idband, band, cellsize):
    it=0 
    parcelle=list()
    shapes=list()
    sizes=list()
    for shape in idlist:
        matrix=np.zeros(band.shape)
        print(it)
        urban=0
        ssize=0
        for i in range (0,idband.shape[0]):
            for j in range (0,idband.shape[1]):
                if idband[i][j]==str(shape) :
                    ssize+=1
                    matrix[i][j]=1
                    if band[i][j]==6:
                        urban+=1
#        print("ssize=",ssize)
#        print("urb= ",urban)
        if ssize !=0 and urban/ssize<0.1:                     
            sshape=mf.FractalDimensionIndex(mf,matrix,cellsize)
#            print("ssize=",ssize)
            if gsize-5 <= ssize <= gsize+5 and sshape >(gshape+float(0.085))  :
                parcelle.append(shape)
                shapes.append(sshape)
                sizes.append(ssize)
                print("sshape = ",sshape)
                print("ssize=",ssize)
                it+=1
            else: 
                print("Already urbanized or no intersection!")
        if it ==5:
            break
#        else:
#            continue
#                break
        
    print(len(parcelle))
    return parcelle, shapes, sizes