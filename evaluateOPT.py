# -*- coding: utf-8 -*-
"""
Here I define:  
    -the functions that measure the Delta of the selected metrics 
    -the politics, ie those function that evaluate the compensation according to the choosen policy 
    (a policy determine the metrics and classes of LU to be considered)
"""

import numpy as np
#from os import rename
#import matplotlib.pyplot as plt

def evaluateLPI(delta_lpi,len_cl) :
    Fmax=0
    #I evaluate only the 1-5 classes NOT the urban one
    len_cl=len_cl-1  
    cond_list=[None]*len_cl
    F_lu=np.zeros(len_cl)
    for cl in range(0,3):
        cond_list[cl]=delta_lpi[cl]
        fc=0
        Fmax+=100
        if cond_list[cl]== 0:
            fc+= float(100)
        elif cond_list[cl] != 0:
            fc+=float(min(0,cond_list[cl])+(float(100/cond_list[cl]))*max(0,cond_list[cl]))
        print("Fitness for LU ",cl+1, " = ", fc)
        F_lu[cl]=fc
    F=sum(F_lu)
    print(F)
    print(Fmax)
    return F, Fmax, #cond_list

def evaluateCOH(delta_coh,len_cl) :
    Fmax=0
    #I evaluate only the 1-5 classes NOT the urban one
    len_cl=len_cl-1  
    cond_list=[None]*len_cl
    F_lu=np.zeros(len_cl)
    for cl in range(0,3):
        cond_list[cl]=delta_coh[cl]
        fc=0
        Fmax+=100
        if cond_list[cl]== 0:
            fc+= float(100)
        elif cond_list[cl] != 0:
            fc+=float(min(0,cond_list[cl])+(float(100/cond_list[cl]))*max(0,cond_list[cl]))
        print("Fitness for LU ",cl+1, " = ", fc)
        F_lu[cl]=fc
    F=sum(F_lu)
    print(F)
    print(Fmax)
    return F, Fmax, #cond_list

def evaluatePLAND(delta_pland,len_cl) :
    Fmax=0
    #I evaluate only the 1-5 classes NOT the urban one
    len_cl=len_cl-1  
    cond_list=[None]*len_cl
    F_lu=np.zeros(len_cl)
    #for classes 4-5 (index 3-4) I only have area condition 
    for cl in range(3,5):
        cond_list[cl]=delta_pland[cl]
        fc=0
        Fmax+=100
        if cond_list[cl] == 0:
            fc+= float(100)
        elif cond_list[cl] != 0:
            fc+=float(min(0,cond_list[cl])+(float(100/cond_list[cl]))*max(0,cond_list[cl]))
#        print(fc)
        F_lu[cl]=fc
    F=sum(F_lu)
#    print(F)
#    print(Fmax)
    return F, Fmax #, cond_list


#only biodiversity, only area preservation
def evaluate0(delta_pland,tol):
    Fmax=0
    cond_list=list()
    F_lu=list()
    for i in range(0,2):
        cond_list.append(delta_pland[i]+(abs(delta_pland[i])*tol)/100)
        fc=0
        Fmax+=100
        if cond_list[i]==0:
            fc+=float(100)
        elif cond_list[i] != 0:
            fc+=float(min(0,cond_list[i])+(float(100/cond_list[i]))*max(0,cond_list[i]))
        F_lu.append(fc)
    F=sum(F_lu)
#    print(F)
    return F, Fmax

#only biodiversity, only area preservation (PLAND)
#tol gives the possibility to apply a tolerance concerning the delta
def evaluate1_relax(delta_pland,tol):
    Fmax=0
    cond_list=list()
    F_lu=list()
    for i in range(0,3):
        cond_list.append(delta_pland[i]+(abs(delta_pland[i])*tol)/100)
        fc=0
        Fmax+=100
        if cond_list[i]==0:
            fc+=float(100)
        elif cond_list[i] != 0:
            fc+=float(min(0,cond_list[i])+(float(100/cond_list[i]))*max(0,cond_list[i]))
        F_lu.append(fc)
    F=sum(F_lu)
#    print(F)
    return F, Fmax

#only biodiversity, preserving LPI and COH
def evaluate1b(delta_lpi,delta_coh) : #delta_pland,
    Fmax=0
    cond_list=[None]*3
    F_lu=np.zeros(3)
    for cl in range(0,3):
        #for LU 1,2,3 (index 0,1,2) I impose two conditions
        cond_list[cl]=[delta_lpi[cl],delta_coh[cl]]
        fc=0
        #I check the distances for all conditions imposed for LU cl
        for i in range(0,len(cond_list[cl])):
#            print("For classes cl= ",cl,"condition ",i,"we have, delta = ", cond_list[cl][i])
            Fmax+=100
            if cond_list[cl][i] == float(0):
                fc+= float(100)
            elif cond_list[cl][i] != float(0):
                fc+=float(min(0,cond_list[cl][i])+(float(100/cond_list[cl][i]))*max(0,cond_list[cl][i]))
#            print("This means fc= ",fc)
        F_lu[cl]=fc
    F=sum(F_lu)
#    print(F)
#    print(Fmax)
    return F, Fmax, #cond_list 
    

#biodiversity & food security: 
#here I evaluate biodiversity as in evaluate 1b (LPI and COH)
#food security: I evaluate pland LU 4-5    
def evaluate3(delta_pland,delta_lpi,delta_coh,len_cl) :
    Fmax=0
    #I evaluate only the 1-5 classes NOT the urban one
    len_cl=len_cl-1  
    cond_list=[None]*len_cl
    F_lu=np.zeros(len_cl)
    for cl in range(0,3):
        #for LU 1,2,3 (index 0,1,2) I impose two conditions
        cond_list[cl]=[delta_lpi[cl],delta_coh[cl]]
    #for classes 4-5 (index 3-4) I only have area condition 
    for cl in range(3,5):
        cond_list[cl]=[delta_pland[cl]]
    for cl in range(0,len_cl):
        fc=0
        #I check the distances for all conditions imposed for LU cl
        for i in range(0,len(cond_list[cl])):
#            print("For classes cl= ",cl,"condition ",i,"we have, delta = ", cond_list[cl][i])
            Fmax+=100
            if cond_list[cl][i] == float(0):
                fc+= float(100)
            elif cond_list[cl][i] != float(0):
                fc+=float(min(0,cond_list[cl][i])+(float(100/cond_list[cl][i]))*max(0,cond_list[cl][i]))
#            print("This means fc= ",fc)
        F_lu[cl]=fc
    F=sum(F_lu)
    print(F)
#    print(Fmax)
    return F, Fmax, #cond_list      
#biodiversity & food security: 
#here I evaluate biodiversity as in evaluate 1b (LPI and COH)
#food security: I evaluate pland LU 4-5    
#tol gives the possibility to apply a tolerance concerning the delta
def evaluate3_relax(delta_pland,delta_lpi,delta_coh,len_cl,tol) :
    Fmax=0
    #I evaluate only the 1-5 classes NOT the urban one
    len_cl=len_cl-1  
    relax=[None]*len_cl
    F_lu=np.zeros(len_cl)
    for cl in range(0,3):
        #for LU 1,2,3 (index 0,1,2) I impose two conditions
        relax[cl]=[delta_lpi[cl]+tol,delta_coh[cl]+tol]
    #for classes 4-5 (index 3-4) I only have area condition 
    for cl in range(3,5):
        relax[cl]=[delta_pland[cl]+tol]
    for cl in range(0,len_cl):
        fc=0
        #I check the distances for all conditions imposed for LU cl
        for i in range(0,len(relax[cl])):
#            print("For classes cl= ",cl,"condition ",i,"we have, delta relaxed = ", relax[cl][i], ", with tol=",tol )
            Fmax+=float(100)
            if relax[cl][i] == float(0):
                fc+= float(100)
            elif relax[cl][i] != float(0):
                fc+=float(min(0,relax[cl][i])+(float(100/relax[cl][i]))*max(0,relax[cl][i]))
#            print("This means fc= ",fc)
        F_lu[cl]=fc
    F=float(sum(F_lu))
#    print(F)
#    print(Fmax)
    return F, Fmax, #cond_list      

        
def getcost(complistLU, bestLU):
    cost=0
    for i in range(0,6):
        cost+=complistLU[i]*(i+1-bestLU)
    return cost
        
