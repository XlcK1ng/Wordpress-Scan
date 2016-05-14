import requests
import re
import time 
import threading
import os
import sys
from multiprocessing import Queue, Process
from multiprocessing.sharedctypes import Value
from __future__ import division


class WordPress_Scan():

	def VersionScan(self):
		self.Version_Path =  "http://{0}".format(self.url)+'/readme.html'
		self.Version_Page = requests.get(self.Version_Path)
		self.Version_Page.encoding='utf-8'
		if(self.Version_Page.status_code == 200):
			self.Version_text = self.Version_Page.text
			#print self.Version_text
			self.reg = r'<br />(.+?)\n</h1>'
			self.RegEx = re.compile(self.reg,re.S)
			self.Version = re.findall(self.RegEx,self.Version_text)
			#for line in self.Version:
				#print "Wordpress Version:%s" %line.encode("utf-8")
			if(len(self.Version)>0):
				print "Wordpress Version:%s" %self.Version[0].encode("utf-8")
	def ThemesScan(self):
		ThemesPath = "http://{0}".format(self.url)
		self.URL_Page = requests.get(ThemesPath)
		if(self.URL_Page.status_code == 200):
			URL_Page_text = self.URL_Page.text
			reg = r'/wp-content/themes/(.*?)/'
			RegEx = re.compile(reg)
			themes = re.findall(RegEx,URL_Page_text)
			if(len(themes)>0):
				print "Wordpress Themes:%s" %themes[0]

	def Server_Scan(self):
		Server_Path = "http://{0}".format(self.url)
		self.ReServer = requests.get(Server_Path)
		if(self.ReServer.status_code == 200):
			print "Wordpress Server Info:%s" %self.ReServer.headers['server']