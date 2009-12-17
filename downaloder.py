import os
import re
import sys
import shutil
import os.path
import getpass
import urllib as u
import pprint as pp
import urllib2 as u2
import urlparse as up
import BeautifulSoup as bs
import htmlentitydefs as hdefs

import ffa
import ffnet
import ficwad
import output
import fictionalley

class FanficLoader:
	'''A controller class which handles the interaction between various specific downloaders and writers'''
	booksDirectory = "books"
	
	def __init__(self, adapter, writerClass):
		self.adapter = adapter
		self.writerClass = writerClass
		
	def download(self):
		urls = self.adapter.extractIndividualUrls()
		self.writer = self.writerClass(self.booksDirectory, self.adapter.getStoryName(), self.adapter.getAuthorName())
		
		i = 0
		for u,n in urls:
			print('Downloading chapter %d/%d' % (i, len(urls)))
			i = i+1
			text = self.adapter.getText(u)
			self.writer.writeChapter(n, text)
		
		self.writer.finalise()
	

if __name__ == '__main__':
	(url, format) = sys.argv[1:]
	
	if type(url) is unicode:
		print('URL is unicode')
		url = url.encode('latin1')
	
	adapter = None
	writerClass = None
	
	if url.find('fanficauthors') != -1:
		adapter = ffa.FFA(url)
	elif url.find('fictionalley') != -1:
		adapter = fictionalley.FictionAlley(url)
		print >> sys.stderr, "FictionAlley adapter is broken, try to find this fic on fanfiction.net or fanficauthors"
		sys.exit(0)
	elif url.find('ficwad') != -1:
		adapter = ficwad.FicWad(url)
	elif url.find('fanfiction.net') != -1:
		adapter = ffnet.FFNet(url)
	else:
		print >> sys.stderr, "Oi! I can haz not appropriate adapter for URL %s!" % url
		sys.exit(1)

	if format == 'epub':
		writerClass = output.EPubFanficWriter
	elif format == 'html':
		writerClass = output.HTMLWriter
	
	if adapter.requiresLogin(url):
		print("Meow, URL %s requires you to haz been logged in! Please can I haz this datas?" % url)
		sys.stdout.write("Can I haz ur login? ")
		login = sys.stdin.readline().strip()
		password = getpass.getpass(prompt='Can I haz ur password? ')
		print("Login: `%s`, Password: `%s`" % (login, password))
		
		adapter.setLogin(login)
		adapter.setPassword(password)
		
	
	loader = FanficLoader(adapter, writerClass)
	loader.download()
	