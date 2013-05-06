# this program outputs twitter streams with language code, user name, tweet, creation time in a tab seperated output 
# usage: python twitterstream.py

# initial skelaton taken from: https://class.coursera.org/datasci-001

#The steps below will help you set up your twitter account to be able to access the live 1% stream.
# 
#●      Create a twitter account if you do not already have one.
#●      Go to https://dev.twitter.com/apps and log in with your twitter credentials.
#●      Click "create an application"
#●      Fill out the form and agree to the terms. Put in a dummy website if you don't have one you want to use.
#●      On the next page, scroll down and click "Create my access token"
#●      Copy your "Consumer key" and your "Consumer secret" into twitterstream.py
#●      Click "Create my access token." You can Read more about Oauth authorization.
#●      Open twitterstream.py and set the variables corresponding to the consumer key, consumer secret, access token, and access secret.
# 
#access_token_key = "<Enter your access token key here>"
#access_token_secret = "<Enter your access token secret here>"
# 
#consumer_key = "<Enter consumer key>"
#consumer_secret = "<Enter consumer secret>"
# 


import json 
import oauth2 as oauth
import urllib2 as urllib

access_token_key = "ENTER YOURS"
access_token_secret = "ENTER YOURS"

consumer_key = "ENTER YOURS"
consumer_secret = "ENTER YOURS"

_debug = 0

oauth_token    = oauth.Token(key=access_token_key, secret=access_token_secret)
oauth_consumer = oauth.Consumer(key=consumer_key, secret=consumer_secret)

signature_method_hmac_sha1 = oauth.SignatureMethod_HMAC_SHA1()

http_method = "GET"


http_handler  = urllib.HTTPHandler(debuglevel=_debug)
https_handler = urllib.HTTPSHandler(debuglevel=_debug)

'''
Construct, sign, and open a twitter request
using the hard-coded credentials above.
'''
def twitterreq(url, method, parameters):
  req = oauth.Request.from_consumer_and_token(oauth_consumer,
                                             token=oauth_token,
                                             http_method=http_method,
                                             http_url=url, 
                                             parameters=parameters)

  req.sign_request(signature_method_hmac_sha1, oauth_consumer, oauth_token)

  headers = req.to_header()

  if http_method == "POST":
    encoded_post_data = req.to_postdata()
  else:
    encoded_post_data = None
    url = req.to_url()

  opener = urllib.OpenerDirector()
  opener.add_handler(http_handler)
  opener.add_handler(https_handler)

  response = opener.open(url, encoded_post_data)

  return response

def extract_tweet_from_stream(line): 
	try: 
		response = json.loads(line)
		#print response.keys()
		encoded_string = response["text"].encode('utf-8')
		return response["lang"] + '\t' + response["user"]["screen_name"] + '\t' + encoded_string + '\t' + response["created_at"] 
	except: 
		return ''

def fetchsamples():
	url = "https://stream.twitter.com/1/statuses/sample.json"
	parameters = []
	response = twitterreq(url, "GET", parameters)
	for line in response:
		#print line.strip()
		result = extract_tweet_from_stream(line.strip())
		if result != '': 
			print result 

if __name__ == '__main__':
  fetchsamples()
