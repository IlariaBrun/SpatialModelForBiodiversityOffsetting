# -*- coding: utf-8 -*-
"""
Created on Thu Oct  3 15:03:27 2019
@author: ilari
BE CAREFUL: THIS PROGRAM MODIFY THE INPUT FIGURE.TIFF, SO ALWAYS BE SURE TO HAVE A COPY OF THE ORIGINAL WHICH WON'T BE TOUCHED
"""

import numpy as np
import geopandas as gpd
from rasterio.mask import mask
import rasterio

#
#path="../../QGis/MyLUclasses/comm45182.tif"
#shape="shapes45182.shp"

commstr=""
path="communes/copy/commune"+commstr+".tif"
path2="communes/copy/commune"+commstr+"2.tif"

shape="communes/shapes"+commstr+".shp"


shapefile = gpd.read_file(shape)
idpar=np.array(shapefile.id)
short=idpar[:10]
idsize=len(idpar[0])

np.save("idlist"+commstr,idpar) #I create a list of all plots id
#np.save("idlist",idpar)
with rasterio.open(path) as src :
    band=src.read(1)
    h=src.height
    w=src.width
    coord=src.crs
    transforma=src.transform
   
    
idband=np.chararray(band.shape, itemsize=idsize, unicode=True)   #empty matrix of strings
 
for i in range (0,band.shape[0]):
    for j in range (0,band.shape[1]): #I set and reset the zero value
        idband[i][j]="zero"
        if band[i][j]==255:
            band[i][j]=0


#I rewrite the raster's band with nodatavalue=0
with rasterio.open(path2,'w',driver='GTiff',height=h,width=w,count=1,dtype=np.uint8,nodata=0,crs=coord,transform=transforma) as dst:
    dst.write(band, 1)
    
with rasterio.open(path, nodata=0) as dst:    
    for idp in idpar : #short:
        ishape=shapefile[shapefile.id==idp]
    #### extract the geometry in GeoJSON format
        geoms = ishape.geometry.values # list of shapely geometries
        from shapely.geometry import mapping
        geoms = [mapping(geoms[0])]
        newband, new_transform=mask(dst, geoms, crop=False, nodata=0)
        newband=newband[0]
        for i in range (0,newband.shape[0]):
                for j in range (0,newband.shape[1]):
                    if newband[i][j]!=0: 
                        idband[i][j]=idp
                        
for i in range (0,band.shape[0]):
                for j in range (0,band.shape[1]):
                    if band[i][j]!=0 and idband[i][j]=='zero':
                        print("There's a problem!!!")
                        
                        
            
np.save("idmatrix45224",idband)
#np.save("idmatrix",idband)
        
#print(idband)
        
        
    

