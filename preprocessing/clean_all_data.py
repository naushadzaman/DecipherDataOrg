#!/bin/python 

## usage: for performing all tasks 
##  python clean_all_data.py 

## usage: to convert the scientific format data to float data 
##	python clean_all_data.py float 

## usage: to propagate the missing data from the last year's data 
##	python clean_all_data.py prop

	
	
import re 
import sys 
import pickle
import fileinput 



ignore_country_list = ["Arab World","Caribbean small states","East Asia & Pacific (all income levels)","East Asia & Pacific (developing only)","Euro area","Europe & Central Asia (all income levels)","Europe & Central Asia (developing only)","European Union","Heavily indebted poor countries (HIPC)","High income","High income: nonOECD","High income: OECD","Latin America & Caribbean (all income levels)","Latin America & Caribbean (developing only)","Least developed countries: UN classification","Low & middle income","Low income","Lower middle income","Middle East & North Africa (all income levels)","Middle East & North Africa (developing only)","Middle income","North America","Not classified","OECD members","Other small states","Pacific island small states","Small states",'Sub-Saharan Africa (all income levels)','Sub-Saharan Africa (developing only)','Upper middle income','Central African Republic'] #'World', "South Asia"

#outfile = open('clean_'+file, 'w') 

## extracts the file name from an absolute path 
def extract_name(filename):
	parts = re.split('/', filename)
	length = len(parts)
	return parts[length-1]

file = sys.argv[1] #dir + '/WDI_GDF_Data.csv'
dir = re.sub(extract_name(file), '', file)# '../data/WorldBank'

def is_number(s):
	try:
		float(s)
		return True
	except ValueError:
		return False
	
	
def convert_data_to_float(file):
	outfile = open(dir + 'float_'+extract_name(file), 'w') 
	print_data = '' 
	splitter = ','
	for line in open(file): 
		if line.strip() == '': 
			continue 
		words = line.split(',')
		str_foo = '' 
		start_punc = False 
		for i in range(0, len(words)): 
			words[i] = re.sub('\r\n', '', words[i])
			#print words[i], is_number(words[i]) 
			if re.match('"', words[i]): 
				punctuation = ' -'
				start_punc = True 
			elif re.search('"', words[i]): 
				start_punc = False 
				punctuation = splitter + ' '
			elif start_punc == True: 
				punctuation = ' -'
			else: 
				punctuation = splitter + ' '
			## if its the header line 
			if is_number(words[i]) and not re.search('Country Name,Country Code,Indicator Name,Indicator Code', line): 
				str_foo += str('%.4f' % float(words[i])) + punctuation 
			else: 
				str_foo += words[i] + punctuation 
		str_foo = str_foo.strip().strip(splitter)
		##print str_foo, len(str_foo.split(splitter))  
		outfile.write(str_foo + '\n')
	outfile.close()	


def propagate_the_data(file): 
	float_file = dir + 'float_'+extract_name(file)
	propagate_file = open(dir + 'clean_'+extract_name(file), 'w') 
	for line in fileinput.input(float_file):
		##print line.strip() 
		last = '' 
		if line.strip() == '': 
			continue 
		words = line.split(',')
		str_foo = ','.join(words[:4]) + ', '
		for i in range(4, len(words)): 
			words[i] = words[i].strip()
			if words[i] == '': 
				words[i] = last 
			else: 
				last = words[i]
			str_foo += words[i] + ', '
		str_foo = str_foo.strip().strip(',')
		##print str_foo 
		country = words[0]
		if not country in ignore_country_list: 
			propagate_file.write(str_foo+'\n')
	propagate_file.close()


def write_binary(file): 
	clean_file = dir + 'clean_'+extract_name(file)
	data = open(clean_file).read()
	pkl = open(dir+'binary_'+extract_name(file), 'w')
	pickle.dump(data, pkl)
	pkl.close()
	
	
	
if len(sys.argv) > 2: 
	mode = sys.argv[2]

	if mode == 'float': 
		convert_data_to_float(file) 
	elif mode == 'prop':
		propagate_the_data(file)
	elif mode == 'write': 
		write_binary(file)

else: 
	convert_data_to_float(file) 
	propagate_the_data(file)
	write_binary(file)
	