"""
GENETIC ALGORITHM to find a possible compensation for a given urbanization

inputs: 
    -name of the municipality to be analyzed
    -npy list containing all the ID of the plots of land of a given municipality
    -npy list containing all the Land Uses of the plots of land of a given municipality
    -id of the plot to be urbanized
    
outputs:    
    -npy list of ID of compenseted plots
    -npy list of the LU used for the compensation 
    -npy lists of DELTAs of the metric indexes used (LPI;DIV;PLAND)
    -txt file with a first analysis of the compensations 
"""

import numpy as np
import MetricFuntions as mf
import simulate_landscapeOPT as sl
import evaluateOPT as eva
import crop_functions as cf
import random
import time 
import os
import sys

timestr = time.strftime("%d_%m_%Hh%M")

commstr="45093" #name of the municipality to be analized
commpath="communes/NewCommunes/"
listid_path=commpath+"shortidlist"+commstr+"_3pix.npy" #LIST OF PLOTS > 3 pixels

listid=np.load(listid_path, allow_pickle=True) #complete list
idband=np.load(commpath+"newIDband"+commstr+".npy", allow_pickle=True)
band=np.load(commpath+"newBand_"+commstr+".npy") #ORIGINAL LANDSCAPE

####id of the crop I'm going to urbanize
idurb="450930000K0019"

listid=np.delete(listid, np.where(listid == idurb))
cellsize=20
classes=list(np.arange(1,7))
len_cl=len(classes)
tol=0

#results directory 
dirpath="resultsD/SC1b"+idurb+"_"+timestr+"short3"
os.mkdir(dirpath)

##I initialize the lists of each landscape metric
# index used to evaluate the landscape

PLAND=np.zeros(len_cl)#original landscape
LPI=np.zeros(len_cl)
division=np.zeros(len_cl)

PLAND_U=np.zeros(len_cl) #urbanized landscape
LPI_U=np.zeros(len_cl)
division_U=np.zeros(len_cl)

PLAND_af=np.zeros(len_cl) #after urbanization&compensation
LPI_af=np.zeros(len_cl)
division_af=np.zeros(len_cl)

#DELTAS to be evaluated for the policy
delta_plandU=np.zeros(len_cl) 
delta_lpiU=np.zeros(len_cl)
delta_divU=np.zeros(len_cl)

delta_pland=np.zeros(len_cl)
delta_lpi=np.zeros(len_cl)
delta_div=np.zeros(len_cl)
      
nodata=0

#indexes of the original landscape
for cl in classes:   
    cl_array=mf.class_selection(band,classes,nodata,cl) #array of a given class
    struct, label, numpa =mf.f_ccl(mf,cl_array,s=2) #labeled array (wich allows to distinguish each patch-8neigh distance is set        
    PLAND[cl-1]=mf.cl_Proportion(mf,band,cl)#mf.returnArea(cl_array,cellsize) #filling the list
    LPI[cl-1]=mf.LargestPatchIndex(mf,band,classes,label,numpa,cellsize,cl)
    division[cl-1]=mf.LandscapeDivisionIndex(mf,band,label,numpa,classes,cl) 
np.save(dirpath+"/PLANDorig",PLAND)
np.save(dirpath+"/LPIorig",LPI)
np.save(dirpath+"/divorig",division)

################# URBANIZATION ###################################
urb_k =0
while urb_k==0:
    bandU,urb_k=sl.urbanization(idurb, idband, band) #I urbanize the given crop
#checkcrop measure the distribution of pixels per LU
int_urb_list,totpixurb =cf.checkcrop(idurb, idband, band)
print("Original LU of the urbanized plot of land= ",int_urb_list)
print("Urbanized = ", urb_k)
print(totpixurb)

#Evaluation of the urbanized landscape
for cl in classes:
    cl_array=mf.class_selection(bandU,classes,nodata,cl)
    struct, label, numpa =mf.f_ccl(mf,cl_array,s=2)        
    PLAND_U[cl-1]=mf.cl_Proportion(mf,bandU,cl)#mf.returnArea(cl_array,cellsize)
    LPI_U[cl-1]=mf.LargestPatchIndex(mf,bandU,classes,label,numpa,cellsize,cl)
    division_U[cl-1]=mf.LandscapeDivisionIndex(mf,band,label,numpa,classes,cl)
    delta_plandU[cl-1]=float(PLAND_U[cl-1]-PLAND[cl-1])
    delta_lpiU[cl-1]=float(LPI_U[cl-1]-LPI[cl-1])
    delta_divU[cl-1]=float(division[cl-1]-division_U[cl-1]) #increasing with subdivision    
urbanF,Fmax=eva.evaluate1b(delta_lpiU, delta_divU)

if urbanF== Fmax:
    sys.exit("The urbanization didn't impact the considered index!")
else:
    print("urbanF =", urbanF)
    print("Delta PLAND: ", delta_plandU)
    print("Delta LPI: ", delta_lpiU)
    print("Delta division: ", delta_divU)    
    
#np.save(dirpath+"/PLANDurb",PLAND_U)
#np.save(dirpath+"/LPIurb",LPI_U)
#np.save(dirpath+"/divurb",division_U)

numit=0
maxit=1000 #max number of compensations 
maxINit=400 #max number of iterations of the inner cicle
fail=0 #count the "failed" compensation loops
allists=list()

allcomp=0
unicomp=0
ratio=1

#external cicle
while numit<maxit and (ratio> 0.9 or numit<100) : 
    print("Now numit= ",numit)
    F=urbanF
    bestF=urbanF    
    bestFarray=list()
    allFarray=list()
    bestFarray.append(F)
    allFarray.append(F)
    bestLU=list()
    pixcompbypar=list()
    compensationlist=list()
    band2comp=np.copy(bandU) #the matrix I'll compensate
    bestband=np.copy(bandU) #the band with the best fitness so far
    tot_pix_comp=0
    templist=np.copy(listid)
    numINit=0
    Dpland=list()
    Dlpi=list()
    Ddiv=list()
    Dpland.append(delta_plandU)
    Dlpi.append(delta_lpiU)
    Ddiv.append(delta_divU)
    while numINit<maxINit and F<Fmax:
        better=0
        k=random.randint(0,len(templist)-1) 
        randshape=templist[k] #I choose the first random crop to compensate
#        print("Now compensating parcel ", randshape)              
        tot_pixel=0
        pix_comp=0    
        for l in range(1,6): #I try the 5 LU for the given parcel (all but urban)
#            print("Compensating with LU : ", l)        
            testband,int_pixel=sl.compensation_fixed(band2comp, randshape, idband,l)
            tot_pixel+=int_pixel
            if int_pixel != 0:
                for cl in classes:
                    cl_array=mf.class_selection(testband,classes,nodata,cl)
                    struct, label, numpa =mf.f_ccl(mf,cl_array,s=2)        
                    PLAND_af[cl-1]=mf.cl_Proportion(mf,testband,cl)#mf.returnArea(cl_array,cellsize)
                    LPI_af[cl-1]=mf.LargestPatchIndex(mf,testband,classes,label,numpa,cellsize,cl)
                    division_af[cl-1]=mf.LandscapeDivisionIndex(mf,testband,label,numpa,classes,cl)
                    
                    delta_pland[cl-1]=float(PLAND_af[cl-1]-PLAND[cl-1])
                    delta_lpi[cl-1]=float(LPI_af[cl-1]-LPI[cl-1])
                    delta_div[cl-1]=float(division[cl-1]-division_af[cl-1])
                #I evaluate the landscape, according to the choosen policy 
#                F,Fmax=eva.evaluate3_relax(delta_pland,delta_lpi,delta_div,len_cl,tol)
                F,Fmax=eva.evaluate1b(delta_lpi, delta_div)
#                F,Fmax=eva.evaluate1_relax(delta_pland,tol)
                allFarray.append(F)
                
                if F==Fmax:
                    allcomp+=1
                    print("Optimal landscape has been found!")
                    pixcompbypar.append(int_pixel)
                    compensationlist.append(randshape)
                    bestLU.append(l)
                    pix_comp=int_pixel
                    tot_pix_comp+=int_pixel
                    bestFarray.append(F)
                    sortedlist=list(compensationlist.copy())
                    sortedlist.sort()
                    if sortedlist in allists:
                        print("NO!! Already in the compensation list")
                    else:
                        allists.append(sortedlist.copy())
                        unicomp+=1
                        Dpland.append(list(delta_pland))
                        Dlpi.append(list(delta_lpi))
                        Ddiv.append(list(delta_div))                       
                        np.save(dirpath+"/complist"+str(unicomp), compensationlist) #I save the not sorted one to have the good correspondance with the best LU!!!!
                        np.save(dirpath+"/bestLU"+str(unicomp), bestLU)
                        np.save(dirpath+"/Dpland"+str(unicomp),Dpland) #delta_pland #PLAND_af
                        np.save(dirpath+"/Dlpi"+str(unicomp),Dlpi) #delta_lpi #LPI_af
                        np.save(dirpath+"/Ddiv"+str(unicomp),Ddiv) #delta_coh #COH_af
                    break #if the optimum is reached I exit the loop            
                elif F>bestF:
                    better=1
#                    print("Getting better!")
                    bestF=F #I update the best fitness
                    #if the compensation is succesfull, I keep the the compensated landscape 
                    bestband=np.copy(testband) #I update the best matrix
                    bestint=int_pixel
                    pix_comp=int_pixel                  
                    bestpland=np.copy(delta_pland)
                    bestlpi=np.copy(delta_lpi)
                    bestdiv=np.copy(delta_div)
                    bestl=l                    
                bestFarray.append(bestF) #best fitness list
        tot_pix_comp+=pix_comp #pixels actually compensated         
        #after having tested all the LUs for the given parcel, I keep the more performing one
        if better ==1:
            compensationlist.append(randshape) #I keep track of the compensated crops
            bestLU.append(bestl)
            pixcompbypar.append(bestint)
            Dpland.append(list(bestpland))
#            print(bestpland[0:3])
            Dlpi.append(list(bestlpi))
            Ddiv.append(list(bestdiv))
            
            templist=np.delete(templist, np.where(templist == randshape)) # I eliminate from the temporary list the parcels already compensated
        #the matrix I'll compensate next: 
        #if the fitness has  improved, it's the matrix with the compensated parcel
        #otherwise it's still bandU (the urbanized band)
        band2comp=np.copy(bestband)
        if tot_pixel !=0:
            numINit+=1
        if numINit == maxINit:
            fail+=1
    if numINit<maxINit:
        ratio=unicomp/allcomp
    file = open(dirpath+"/First_Analysis.txt", "w")
    file.write("****Simulation has been interrupted****")
    file.write("\n List id used: \n "+str(listid_path))
    file.write("\n Simulation has been stopped at "+str(unicomp)+" unique compensations over "+str(allcomp)+" (max iterations =100),  (ratio = "+str(ratio)+")")
    file.write("\n Failed compensations: "+str(fail))
    file.write("\n\n GEOMETRIC ANALYSIS \n\n")
    file.write("\n Original landscape: \n"+"PLAND: "+ str(PLAND)+"\n"+"LPI: "+str(LPI)+"\n"+"div: "+str(division))
    file.write("\n Urbanized landscape: \n"+"PLAND: "+ str(PLAND_U)+"\n"+"LPI: "+str(LPI_U)+"\n"+"COH: "+str(division_U))
    file.write("\n\n Delta Urbanized landscape: \n"+"Delta PLAND: "+ str(delta_plandU)+"\n"+"Delta LPI: "+str(delta_lpiU)+"\n"+"COH: "+str(delta_divU))
    file.close()
    numit+=1

timestr2 = time.strftime("%d_%m_%Hh%M")
#Here I create a text file with a frist analysis of the results     
file = open(dirpath+"/First_Analysis.txt", "w")
file.write("****Simulation hasn't been interrupted****")
file.write("\n List id used: \n "+str(listid_path))
file.write("\n Simulation started at: " +str(timestr)+" and finished at " +str(timestr2) )
file.write("\n Simulation stopped at "+str(unicomp)+" unique compensations over "+str(allcomp)+" (max iterations =100),  (ratio = "+str(ratio)+")")
file.write("\n Failed compensations: "+str(fail))
file.write("\n\n GEOMETRIC ANALYSIS \n\n")
file.write("\n Original landscape: \n"+"PLAND: "+ str(PLAND)+"\n"+"LPI: "+str(LPI)+"\n"+"division: "+str(division))
file.write("\n Urbanized landscape: \n"+"PLAND: "+ str(PLAND_U)+"\n"+"LPI: "+str(LPI_U)+"\n"+"division: "+str(division_U))
file.write("\n\n Delta Urbanized landscape: \n"+"Delta PLAND: "+ str(delta_plandU)+"\n"+"Delta LPI: "+str(delta_lpiU)+"\n"+"COH: "+str(delta_divU))
file.close()