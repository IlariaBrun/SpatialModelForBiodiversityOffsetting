# SpatialModelForBiodiversityOffsetting
Genetich Algorith to simulate biodiversity offsetting

This program allows to simulate ecological compensations in a given municipality. 
We use raster images of the municipalities and the shape files of the plots of land in that municipality. 
We also use CESBIO maps of Land Uses, where we redifined just 6 main land uses. 


We first simulate an urbanization and then define a genetic algorithm to look for possible compensations. 
-an urbanization consists in changing the land use of a plot of land to urban one
-compensations consists in changing the LU of one or more plot of lands 

Directories: 
COMMUNES : directory containing original raster files, the matrix files (saved as numpy arrays), crops shapes etc...
communes also contains CROPSBYLU (crops classified by main LU) and CROPSBYSIZE (same size, same or different shape)
RESULTS: directory where qll


PRELIMINARY PROGRAMS
-get_id: given the matrix of LU and the crops, creates a matrix with crops ID 
-class_crops: 
class crops of a given town according to heir main LU (>85%)
select crops of the same size and same or different shape
-crop_functions: functions for the crop classification
-readcroplist: for a given array of crops, it prints some info

MAIN PROGRAMS
-Main: main file contqining the genetic algorithm to define a compensation
-simulate_landscapeOPT: contains urbanization and compensation functions
-MetricFunctions: computes the indexes

-evaluateOPT: all the functions to compute de DELTAs of the lanscape metrics indexes 
	and the fitness functions related to the different policies

