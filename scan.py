#!/usr/bin/env python 
# -*- coding: utf-8 -*- 

import os
from lib.__init__ import *
from lib.GeneralScan import *
from lib.PluginCheck import *
from lib.ZoomeyeScan import *


def zeye(Arguments):
	z = Zoomeye(Arguments['keyword'],Arguments['page'],Arguments['zoomeyethread'])
	print "[*] Connect Zoomeye ..."
	z.GetIP()
	z.reportstart()
	z.readfile()
	print "[*] Start Scan ..."
	z.startthread()

def main():
	Arguments = GetParameter()
	if Arguments['version']:
		print '[*] Lee Sin v1.0  Author: Superbread'
		return
	elif Arguments['zoomeye']:
		zeye(Arguments)
		return
	elif Arguments['exp']:
		z = Zoomeye(Arguments['keyword'],Arguments['page'],Arguments['zoomeyethread'])
		z.readfile()
		z.show()
		return
	elif Arguments['url'] == None:
		print '[*] ERROR : unrecognized arguments'
		return 
	scan =  WordPress_Scan(Arguments)
 	plugins =  PluginCheck(Arguments['url'])
	print "[*] Scan URL: http://" +format(Arguments['url'])
	print "[*] Start Vulnerability......\n"
	scan.Connect_Test()
 	scan.Server_Scan()
	scan.VersionScan()
	scan.ThemesScan()
	scan.AuthorScan()
	print ""
	plugins.scan()
	if Arguments['pluginlist']:
		scan.LoadPlugin()
	if Arguments['brute']:
		scan.Brute_Force()
	

if __name__ == '__main__':
	main()
	
 	

		

