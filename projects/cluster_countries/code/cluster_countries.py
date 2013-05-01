#!/bin/python 

# usage: python cluster_countries.py ../../data/WorldBank/clean_WDI_GDF_Data.csv 

import os 
import sys 

## BEGIN CONFIGURATION ## 
clean_data = False #True 
## END CONFIGURATION ## 

## clearn and convert the data 
if clean_data: 
	command = 'python ../../../preprocessing/clean_all_data.py ../../../data/WorldBank/WDI_GDF_Data.csv'
	os.system(command)


inputfile = sys.argv[1]
if len(sys.argv) > 2: 
	outfile = sys.argv[2]
else: 
	outfile = '../data/country_feature.txt'

## generate features for clustering 
#command = 'python feature_generation.py ../../../data/WorldBank/clean_WDI_GDF_Data.csv '
command = 'python feature_generation.py ' + inputfile + ' ' + outfile 
os.system(command)

## cluster data 
command = 'python ../../../data-mining-tools/clustering/agglo-var-clustering.py 0.05 ../data/country_feature.txt ../data/'
os.system(command)