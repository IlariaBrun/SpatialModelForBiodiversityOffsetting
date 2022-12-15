# -*- coding: utf-8 -*-
"""
e define here all the functions to modify a given lanscape with: 
    -a urban deveoment
    -multiple compensations

input: 
    -path=raster image path (lanscape to modify)
    -shapes= shp file, containing multiple plot shape to use for compensation and development
    -new= output path
    
output: 
    -the new raster image 
"""

import numpy as np
import random
  
#urganize a given parcel
def urbanization(fixid, idband, band) : #listid if I want it to be random     
    #Parameters setting
    min_px_urb= 20 #minimum number of pixel in the intersection - urbanization
    urb_perc=0.1 #maximum % of already urbanized land when developing new area 
    urbanized=np.copy(band)           
    urban=0
    int_pixel=0    
    while int_pixel < min_px_urb:
        for i in range (0,idband.shape[0]):
            for j in range (0,idband.shape[1]):
                if idband[i][j]==str(fixid) :
                    int_pixel+=1
                    if band[i][j]==6:
                        urban+=1
#                        urbanized[i][j]=6
    if urban/int_pixel < urb_perc:
#        fail=0
        k=0 #k counts the number of pixels actually changed
        for i in range (0,idband.shape[0]):
            for j in range (0,idband.shape[1]):
                if idband[i][j]==fixid :
                        urbanized[i][j]=6
                        k+=1
    else:
        k=0
#        fail=1
        print("The selected area is already urbanized!")      
    return urbanized, k


#compensate a random crop, with a fixed LU
def compensation_random(bandU, listid, idband, urb_k, LU) :
    new=np.copy(bandU)
    int_pixel=0           
    while int_pixel==0:
        k=random.randint(0,len(listid)-1) #I select the random shape
        randshape=listid[k]               
        for i in range (0,idband.shape[0]):
            for j in range (0,idband.shape[1]):
                #I change the values of the intersection              
                if idband[i][j]==str(randshape) :
#                            int_pixel+=1
                    if bandU[i][j] != LU and bandU[i][j] !=6 :
#                                LU_pix+=1
                        int_pixel+=1
                        new[i][j]=LU
#    print(int_pixel)
    return new, randshape     

#compensate a given plot of land with a given LU    
def compensation_fixed(bandU, idparc, idband, LU) :
    new=np.copy(bandU)
#    urban=0
    int_pixel=0   
    for i in range (0,idband.shape[0]):
        for j in range (0,idband.shape[1]):
            #I change the values of the intersection              
            if idband[i][j]==str(idparc) :
                if bandU[i][j] != LU and bandU[i][j] != 6:
                    int_pixel+=1                    
                    new[i][j]=LU
                #elif bandU[i][j] == 6:
#                    urban+=1
#    if int_pixel==0:
#        print("No pixel has been changed (no compensation)")
#    elif int_pixel>0:
#        print("Changed pixels (compensation) = ", int_pixel)
    
#    print("Already urban= ", urban)
    return new, int_pixel

#compensate a given parcel with a given LU
def compensation_fixed2(bandU, idparc, idband, LU) :
    new=np.copy(bandU)
    compix=0
    for i in range (0,idband.shape[0]):
        for j in range (0,idband.shape[1]):
            #I change the values of the intersection              
            if idband[i][j]==str(idparc) :
                if bandU[i][j] !=6 :
                    new[i][j]=LU
                    if idband[i][j]!=LU:
                        compix+=1
                #elif bandU[i][j] == 6:
    return new,compix
 