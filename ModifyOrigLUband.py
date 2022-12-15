# -*- coding: utf-8 -*-
"""
In this program, we approximate the original landscape, so that:  

  1 plot of land is covered by 1 LU 
  
We associate to each plot of its mains land use.
  
  Tha main LU of the plot is considered

@author: ilari
"""
import numpy as np
import matplotlib.pyplot as plt
#import MetricFuntions as mf
import simulate_landscapeOPT as sl
import crop_functions as cf
import rasterio 


#name of the municipality
commstr="45182"
#I select the image of the municipality
dirpath="communes/NewCommunes/"
new=dirpath+"/newband_"+commstr+".tif"
pathcomm="communes/original/commune"+commstr+".tif"

#list of plots' name
listid=np.load("communes/idlist"+commstr+".npy", allow_pickle=True) 


#original band
band=np.load("communes/band_"+commstr+".npy")
#modified id matrix
idband=np.load(dirpath+"newIDband"+commstr+".npy")#id adapted to LUs

cellsize=20
print("Number of crops: ", len(listid))


with rasterio.open(pathcomm) as src :
#    band=src.read(1)
#    band1=src.read(1)
    h=src.height
    w=src.width
    coord=src.crs
    transforma=src.transform 


newband=np.copy(band)
count=0
for id in listid:
    int_list, totpix = cf.checkcrop(id, idband, band)
    shape,size= cf.cropShape(id,idband,band,cellsize) #here I check the size
    if np.count_nonzero(int_list) >= 1: 
        mainLU=np.argmax(int_list)+1
        newband,inter=sl.compensation_fixed(newband, id, idband, mainLU)
#    if size > 3: #this is if I want to do the holes
#        if np.count_nonzero(int_list) >= 1: 
#            mainLU=np.argmax(int_list)+1
#            newband,inter=sl.compensation_fixed(newband, id, idband, mainLU)
#    else :
#        newband,inter=sl.compensation_fixed(newband, id, idband, 0) #I do the holes
        
#I save the modified landscape
np.save(dirpath+"/newBand_"+commstr+".npy",newband)
#I create a tiff
with rasterio.open(new,'w',driver='GTiff',height=h,width=w,count=1,dtype=np.uint8,nodata=0,crs=coord,transform=transforma) as dst:
    dst.write(newband, 1)
plt.figure()
fig,ax=plt.subplots()
img=ax.imshow(band)
fig.colorbar(img, ax=ax)
plt.title("ORIGINAL")
#plt.show()
fig,ax=plt.subplots()
img1=ax.imshow(newband)
fig.colorbar(img1, ax=ax)
plt.title("MODIFIED LANDSCAPE")  
#plt.savefig(idurb+".png")#,bbox_inches='tight'
plt.show(block3=False)