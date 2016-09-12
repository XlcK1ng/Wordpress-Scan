#!/usr/bin/env python 
# -*- coding: utf-8 -*- 

import os
from lib.__init__ import *
from lib.GeneralScan import *
from lib.PluginCheck import *


def main():
	Arguments = GetParameter()
 	scan =  WordPress_Scan(Arguments)
 	plugins =  PluginCheck(Arguments['url'])
	if Arguments['exp'] == True:
		plugins.show()
		return 
 	print "Scan URL: http://" +format(Arguments['url'])
	print "Start Vulnerability......\n"
	scan.Connect_Test()
 	scan.Server_Scan()
	scan.VersionScan()
	scan.ThemesScan()
	scan.AuthorScan()
	print ""
	plugins.scan()
	scan.LoadPlugin()
	if Arguments['brute']:
		scan.Brute_Force()

if __name__ == '__main__':
	main()
	
 	

		

