#!/usr/bin/env python
# coding: utf-8
import re
import requests as r
import json
import urllib2
import sys
from bs4 import BeautifulSoup

authCode = '' #Your genius API auth code goes here
if len(sys.argv) != 2:
	print("Please enter a single search query ")
	exit()

searchQuery = sys.argv[1]
searchQuery.replace(" ", "%20")

#https://docs.genius.com/#/response-format-h1

url = 'https://api.genius.com/search?q=' + searchQuery
header = {'Authorization': 'Bearer ' + authCode}
data = r.get(url, headers=header).json()
# should check for status of header here

# grab first result
url = data['response']['hits'][0]['result']['url']
print('Resolved to URL ' + url)

# load that url's html into memory (need to change user agent to avoid 403 error) 
req = urllib2.Request(url, headers={'User-Agent' : "Magic Browser"}) 
con = urllib2.urlopen( req )
html =  con.read()

# grab html between lyric tags
html_doc = html
soup = BeautifulSoup(html_doc, 'html.parser')
for node in soup.findAll('lyrics'):
    print ''.join(node.findAll(text=True))

