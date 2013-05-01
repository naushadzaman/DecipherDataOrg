#!/bin/python 

## this program converts the raw data to features for data mining algorithms 

import re 
import sys 
import fileinput

debug = 1 

## BEGIN CONFIGURATION ## 
country_code = 0 #1 
indicator_code = 3 
cols_to_consider = [2012]
index_to_consider = [] 
## END CONFIGURATION ## 

## extracts the file name from an absolute path 
def extract_name(filename):
	parts = re.split('/', filename)
	length = len(parts)
	return parts[length-1]


def feature_generation(inputfile, outputfile): 
	countries = [] 
	indicators = [] 
	country2feature = {} 
	values = {} 
	outfile = open(outputfile, 'w')
	for line in fileinput.input(inputfile): 
		if debug >= 3: 
			print line 
		if line.strip() == '': 
			continue		
		words = line.split(',')
		country = words[country_code].strip() 
		indicator = words[indicator_code].strip()  
		if country == 'Country Code' or country == 'Country Name': 
			for i in range(0, len(cols_to_consider)): 
				for index in range(0, len(words)): 
					if words[index].strip() == str(cols_to_consider[i]): 
						index_to_consider.append(index)
						break 
			if debug >= 2: 
				print index_to_consider
		
		if not country in countries:
			countries.append(country)
		if not indicator in indicators: 
			indicators.append(indicator)
		
		index = country + '-' + indicator 
		
		for i in range(0, len(index_to_consider)): 
			if debug >= 2: 
				print index, words[index_to_consider[i]]
			value = words[index_to_consider[i]].strip()
			if value == '': 
				value = '0' 
			if index in values: 
				values[index] += ',' + value 
			else: 
				values[index] = value 
	for c in countries: 
		feature = c 
		if c == 'Country Code' or c == 'Country Name': 
			continue
		for ind in indicators: 
			if ind == 'Indicator Code': 
				continue
			index = c + '-' + ind
			feature += ',' + values[index]
		if debug >= 2: 
			print feature.split(',') , '\n'
		country2feature[c] = feature.split(',')
		outfile.write(feature + '\n')
	
	outfile.close()
	return country2feature, countries 
	
inputfile = sys.argv[1]
if len(sys.argv) > 2: 
	outfile = sys.argv[2]
else: 
	outfile = '../data/country_feature_input.txt'
country2feature, countries = feature_generation(inputfile, outfile) 