# SpatialModelForBiodiversityOffsetting
Genetich Algorith to simulate biodiversity offsetting

This program allows to simulate ecological compensations in a given municipality. 
We use raster images (.tiff) of the municipalities and the shape files of the plots of land in that municipality. 
We also use CESBIO maps of Land Uses, where we redifined just 6 main land uses. 
We first simulate an urbanization and then define a genetic algorithm to look for possible compensations. 
-an urbanization consists in changing the land use of a plot of land to urban one
-compensations consists in changing the LU of one or more plot of lands 
PRELIMINARY PROGRAMS
-get_idNew: given the matrix of LU and the crops, creates a matrix with IDs of plots of land 
-crop_functions: functions for the classification of plots of land
MAIN PROGRAMS
-main: main file contqining the genetic algorithm to simulate the compensation process
-simulate_landscapeOPT: contains urbanization and compensation functions
-MetricFunctions: computes the indexes
-evaluateOPT: all the functions to compute de DELTAs of the lanscape metrics indexes 
and the fitness functions related to the different policies

