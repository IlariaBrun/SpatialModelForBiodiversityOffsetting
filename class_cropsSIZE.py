
"""
Created on Wed Apr 22 16:33:14 2020

@author: ilari
"""

# -*- coding: utf-8 -*-
"""
This program create a list of crops for each land use
Created on Wed Oct 30 09:46:05 2019
@author: ilari
"""
import numpy as np
import crop_functions as cf
from collections import Counter
#import random
#import operator
#import csv


def get_all_modes(a):
    c = Counter(a)  
    mode_count = max(c.values())
    mode = {key for key, count in c.items() if count == mode_count}
    return mode

commstr="45182"
#commstr="45093"


#listid=np.load("communes/NewCommunes/cropidbyLU/45093_95/listid45093_1.npy", allow_pickle=True)

#id band 
dirpath="communes/NewCommunes/"

listid=np.load(dirpath+"plotsbyLU/NewBandNewShapes/listid"+commstr+"_1.npy", allow_pickle=True)
#listid=np.load("communes/idlist"+commstr+".npy", allow_pickle=True)#old list id
#shortlist=np.load(dirpath+"shortidlist"+commstr+".npy", allow_pickle=True)

idband=np.load(dirpath+"newIDband"+commstr+".npy")
#band=np.load("communes/band_"+commstr+".npy")##ORIGINAL band
band=np.load(dirpath+"newBand_"+commstr+".npy")##MODIFIED band 

cellsize=20
print("Number of crops: ", len(listid))


#print("Number of crops short list: ", len(shortlist))
#
##
##idurb="45182000AN0020" #65 urbanized pixels
##idurb="450930000K0150"
#idurb="450930000K0090"
##idurb="450930000M0120"
##idurb="45182000AN0207" #175 urbanized pixels

#
##
#shufflelist=np.copy(listid)
#shufflelist=np.random.shuffle(shufflelist)
##
##

##########################################################################
##LU CLASSIFICATION#######################################################
##########################################################################
####################################################################
###HERE I JUST REDUCE THE CROPS IDLIST 
#shortidlist=list()
#for id in listid:
#    shape,size= cf.cropShape(id,idband,band,cellsize)
#    if size > 3:
#        shortidlist.append(id)       
#print(len(listid))
#print(len(shortidlist))
#np.save(dirpath+"shortidlist"+commstr+"_3pix.npy",shortidlist)
##############################################################

allLU1={}
allsizes=list()



count=0
file = open(dirpath+"idLU1_45182.txt", "w")
for id in listid:
    shape,size= cf.cropShape(id,idband,band,cellsize)
    allLU1[id]=str(size)
    file.write("\n id="+str(id)+ " size="+str(size))
#    allsizes.append(size)
#    if 50 < size <60 :    
#        count+=1
#        print("Parcel "+str(id)+" size: ", size)
file.close()

with open(dirpath+'LU1sizes45182.csv', 'w') as f:
    for key in allLU1.keys():
        f.write("%s, %s\n" % (key, allLU1[key]))

#
###############################################################################
#######SHAPE CLASSIFICATION#######################################################
###############################################################################
####
###
###

#gsize =62
#gshape=1.0913489021325147
#parcelle, shapes, sizes =cf.select_crops(gsize, gshape, listid, idband, band, cellsize)
##parcelleDiff, shapesD,sizesD=cf.select_cropsDiff(gsize, gshape, listid, idband, band, cellsize)
##np.save("communes/cropsbysize/"+"crops"+commstr+"_"+str(gshape)+"_"+str(gsize), parcelle)
#np.save("communes/cropsbysize/"+"crops"+commstr+"_"+str(gshape)+"(tol05_"+str(gsize)+"LU1", parcelle)
##np.save("communes/cropsbysize/"+"crops"+commstr+str(gsize)+"DiffShape0.85", parcelleDiff)
###
##
##
##Luses=list()
##sizes=list()
##for shape in parcelle:
##    print(cf.checkcrop(shape, idband, band))
##    print(cf.cropShape(shape,idband,band,cellsize))
###for shapeD in parcelleDiff:
###    print(cf.checkcrop(shapeD, idband, band))
###    print(cf.cropShape(shapeD,idband,band,cellsize))
###file = open("communes/cropsbysize/"+idurb+"_"+commstr+"SameShape.txt", "w")
##file = open("communes/cropsbysize/"+idurb+"_"+commstr+"SameShapeLU5.txt", "w")    
##file.write(" Parcelles : \n"+str(parcelle))
##file.write("\n Shapes : \n"+str(shapes))
##file.write("\n Sizes : \n"+str(sizes))
##file.close()
##
#
