# this script extracts tweets for any search query 

# detail about search https://dev.twitter.com/docs/using-search
# usage: extract_tweet_for_a_query.py query 
# usage: extract_tweet_for_a_query.py shabag

import urllib 
import json 
import sys 

def extract_tweet_for_a_query(query):
	response = urllib.urlopen("http://search.twitter.com/search.json?q=" + query + "&rpp=100")
	results = json.load(response)["results"]
	i = 0 
	for i in range(len(results)): 
		print results[i]["iso_language_code"] + '\t' + results[i]["from_user"] + "\t" + results[i]["text"].encode('utf-8') + "\t" + results[i]["created_at"]
	

query = sys.argv[1]
extract_tweet_for_a_query(query)
