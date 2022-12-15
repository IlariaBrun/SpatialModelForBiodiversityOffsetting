# -*- coding: utf-8 -*-
"""
Short program that makes the LU matrix homogeneous: 
since some LUs are not considered and appear as 0 in the matrix, 
here I assign to a 0 element of the matrix, the same LU of its neighbor
"""


import numpy as np

#commstr="45093"
commstr="45182"
new="communes/NewCommunes/"+commstr+"_new.tif"
pathcomm="communes/original/commune"+commstr+".tif"
listid=np.load("communes/idlist"+commstr+".npy", allow_pickle=True)
idband=np.load("communes/idmatrix"+commstr+".npy", allow_pickle=True)
band=np.load("communes/band_"+commstr+".npy") #ORIGINAL LANDSCAPE

#mod_band=np.copy(band)
filled_shape=np.copy(idband)

position=list()


count=0
for i in range (0,band.shape[0]):
    for j in range (0,band.shape[1]):
        if band[i][j]!=0 and filled_shape[i][j]=='zero':
            position.append([i,j])
            count+=1
#            print("There's a problem!!! Position :"+str(i)+", "+str(j))
            for l in range(-2,2):
                for m in range(-2,2):
                    try:
                        if filled_shape[i+l][j+m]!='zero':
                            print("I'm filling")
                            filled_shape[i][j]=filled_shape[i+l][j+m]
                    except : IndexError
#                        continue
# 
print("Unassigned pixels: ", count)
#
countafter=0
for i in range (0,band.shape[0]):
    for j in range (0,band.shape[1]):
        if band[i][j]!=0 and filled_shape[i][j]=='zero':
            position.append([i,j])
            countafter+=1
            print("There's STILL a problem!!! Position :"+str(i)+", "+str(j))
print("Count unassigned After = ", countafter)
#
#
#
#
#
np.save("communes/NewCommunes/newIDband"+commstr,filled_shape)

#  
