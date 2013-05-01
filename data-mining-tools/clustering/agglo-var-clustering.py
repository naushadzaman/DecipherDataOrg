import re
import sys 
import math
import fileinput

## agglomerative-variant-clustering -- agglo-var

# usage: 
# python agglo-var-clustering.py threshold feature_file output_dir 
# python ../../../data-mining-tools/clustering/agglo-var-clustering.py 0.2 ../data/country_feature.txt ../data/


#### CONFIGURATION #### 
# define the threshold 
threshold = float(sys.argv[1]) #0.4

# if the number of clusters are less than max_k then break 
max_k = 20 

# ignore the outliers or not
cluster_individuals = False # False, ignore outliers 
feature_separator = ','
feature_file = sys.argv[2]
output_folder = sys.argv[3]

#### CONFIGURATION #### 

debug = 1


def cosine_distance(a, b): 
	sa = set(a)
	sb = set(b)
	c = sa.intersection(sb)
	
	nom = len(c)
	den = math.sqrt(len(sa)) * math.sqrt(len(sb))
	#print len(sa), len(sb), len(c)
	dist = nom*1.0/den 
	if debug >= 2:
		print dist 
	return dist 



# this method expects two lists, each with same size. ith index row_text contains the ith line rows and ith index cluster2entities_text contains the ith line entities. 
def cluster_rows(cluster_output, row_text, id, threshold): 
	clusters = {} 
	total_rows = len(row_text)
	cluster_no = 0 
	id2cluster = {} 
	already_considered = []
	for i in range(0, total_rows): 
		max_dist = 0 
		max_j = 0 
		#for j in range(i+1, no_of_cluster): 
		for j in range(0, total_rows): 
			if i == j: 
				continue
			#print i, j 
			dist = cosine_distance(row_text[i], row_text[j])
			if dist > max_dist: 
				if not j in already_considered: 
					max_dist = dist 
					max_j = j 
		if max_dist > threshold: 
			if debug >= 2: 
				print i, max_j, max_dist 
				#print 'i', i, 'ac', already_considered
			if i in already_considered:
				cluster_id = id2cluster[str(i)]
				clusters[cluster_id] = clusters[cluster_id] + ' ' + id[max_j]
				id2cluster[str(max_j)] = cluster_id
				already_considered.append(max_j)
			else:
				cluster_id = cluster_no
				clusters[cluster_id] = id[i] + ' ' + id[max_j] 
				id2cluster[str(i)] = cluster_id 
				already_considered.append(i)
				id2cluster[str(max_j)] = cluster_id 
				already_considered.append(max_j)
				cluster_no += 1 
	if cluster_individuals == True: 
		# keep the rest of the clusters as it is
		for i in range(0, total_rows): 
			if i in already_considered: 
				continue 
			else: 
				cluster_id = cluster_no 
				clusters[cluster_id] = id[i]
				id2cluster[str(i)] = cluster_id 
				already_considered.append(i)
				cluster_no += 1 
	
			
	total_entities = 0 
	for i in range(0, cluster_no): 
		if debug >= 2: 
			print i, len(row_text[i]), row_text[i]
		str_q = str(i) + '\t' + clusters[i]
		cluster_output.write(str_q + '\n') 
		
	print 'total cluster', cluster_no, 'total entities', total_entities 
			
	
def process_feature(feature_file): 
	row_text = []
	id = [] 
	for line in fileinput.input(feature_file): 
		line = line.strip() 
		if line == '': 
			continue
		words = line.split(feature_separator)
		#print words
		feature_list = words[1:]
		row_text.append(feature_list)
		id.append(words[0])
		
	return row_text, id 



row_text, id = process_feature(feature_file) 

cluster_output = open(output_folder+'output_clusters'+'-'+str(threshold)+'.txt', 'w')
cluster_rows(cluster_output, row_text, id, threshold) 
cluster_output.close()
