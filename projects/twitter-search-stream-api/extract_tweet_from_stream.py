# this script extracts tweets for any search query 

# detail about search https://dev.twitter.com/docs/using-search
# $ python twitterstream.py > tweets.txt
# $ cat tweets.txt | head -20 > 20tweets.txt 
# $ extract_tweet_from_stream.py 20tweets.txt 

# usage: extract_tweet_from_stream.py input_file 

import fileinput
import json 
import sys 

input_file = sys.argv[1]

def extract_tweet_from_stream(line): 
	try: 
		response = json.loads(line)
		#print response.keys()
		encoded_string = response["text"].encode('utf-8')
		return response["user"]["screen_name"] + '\t' + encoded_string + '\t' + response["created_at"] 
	except: 
		return ''

	
def extract_tweet_from_stream_file(input_file):
	for line in fileinput.input(input_file): 
		if line.strip() == '': 
			continue
		output = extract_tweet_from_stream(line)
		if output != '': 
			print output 
		

extract_tweet_from_stream_file(input_file)
