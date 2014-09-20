#!/usr/bin/env python2
# -*- coding: utf-8 -*-
# Coded by Sam (info@sam3.se)
# http://0xdeadcode.se

import StringIO, urllib, signal, os, inspect, optparse
from random import randint
from time import sleep

try:
	import requests
except:
	print 'Could not find the library requests (Python 2.x)\nPlease install it and try again.'
	quit()

try:
	from bs4 import BeautifulSoup
except:
	print 'Could not find the library BeautifulSoup4 (Python 2.x)\nPlease install it and try again.'
	quit()


def getuseragent():
    	ulist = []
    	ufile = open('useragent_list.txt', 'r')
    	for u in ufile.readlines():
        	ulist.append(u.strip('\n'))
    	return ulist
    
try:
    	useragentlist = getuseragent()
    	print '[+] Successfully loaded %i user agent(s)' % len(useragentlist)
except:
    	print '[!] Something went terribly wrong when loading the user agent list. Does the file exist?'
    	quit()

urls, links, subdomains = [[]] * 3

def start_query(query, useragentlist, page):
	global delay
    	headers = {'User-Agent': useragentlist[(randint(1, len(useragentlist)))-1]}  
	domain_list = ['.se', '.com']
	links = []
	for page in xrange(1, 10):
        	r = requests.get('http://www.google.com/search?q=%s&safe=on&start=%i' % ( query, page), timeout = 5)
        	html_container = BeautifulSoup(r.text)
        	links += fix_links(html_container.find_all('a'))
		if delay:
			sleep(1)
	if links:
        	return links
        else:
        	pass
    
def fix_links(linkdata):
    	links = []
    	for link in linkdata:
        	try:
            		l = str(link).strip('\n').split('href=')[1].split('/url?q=')[1].split('"')[0]
            		try:
              		  	l = l.split('&amp;sa')[0]
            		except:
                		pass
	            	if l.find('webcache.googleusercontent.com') == -1:
        	        	l = urllib.unquote(l).decode('utf8')
                		links.append(str(l))
                		pass
            		else:
                		pass
        	except:
            		pass
    	return links

def strip(urls, queryurl):
	returnquery = []
	if len(urls) == 0:
		pass
	else:
		for url in urls:
			returnquery.append(url.split(queryurl)[0].split('//')[1] + queryurl)
		return list(set(returnquery))

##################
def handler(signum, frame): # http://stackoverflow.com/questions/1112343/how-do-i-capture-sigint-in-python
	global subdomains
	if subdomains:
		subdomains = sorted(list(set(subdomains)))
		print '\n\nFound %d subdomains:\n' % len(subdomains)
		for s in subdomains:
        		print s		

	print '\nAlright, alright! Quitting...'
	quit()

signal.signal(signal.SIGINT, handler)

###################

print 'Google subdomain scraper by Sam\n\nGooglesub will use google dorks to find subdomains without accessing the target domain.'
filename = os.path.split(inspect.getfile(inspect.currentframe()))
parser = optparse.OptionParser('Usage: Usage: %s <args>' 
				'\n\nExample: python %s -u google.com -d -q 5'  % (filename[1], filename[1]))
parser.add_option('-u', dest='queryurl', type='string', help='Research target')
parser.add_option('-d', dest='delay', action='store_true', help='Adds delay to the script to avoid getting captcha (optional)')
parser.add_option('-q', dest='queries', type='int', help='How many queries the script should do. Recommended: 6')
(options, args) = parser.parse_args()
queryurl = options.queryurl
delay = options.delay
queries = options.queries
if queryurl == None or queries == None:
	print parser.print_help()
	quit()

query = 'site:' + queryurl
unique = []
if delay:
	print 'Estimated completion time: %d seconds' % (2*int(queries)*10)
print 'Kill it with ctrl+c or let it finish.\nQuerying Google for \'%s\'.\nNow please wait while I invade google...' % query
for num in xrange(0, int(queries)):
	print 'Executing query %s of %s' % (str(num+1), str(queries))
	links = start_query(query, useragentlist, num)
	if links:
		subdomains += strip(links, queryurl)
	else:
		pass
	if subdomains:
		for s in subdomains:
			if s in unique:
				pass
			else:
				query += '+-site:%s' % s
				unique.append(s)
	if delay:
		sleep(2)	

subdomains = sorted(list(set(subdomains)))
print '\n##########################################\nFound %d subdomains on %s\n' % (len(subdomains), queryurl )
for s in subdomains:
	print s
print '\n##########################################\nDone. Quitting...\n'
