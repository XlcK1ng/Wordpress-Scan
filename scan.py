from init import *
from GeneralScan import *
from PluginCheck import *

if __name__ == '__main__':
 	Arguments =  GetParameter()
 	scan =  WordPress_Scan(Arguments)
 	plugins =  PluginCheck(Arguments['url'])
 	scan.Server_Scan()
	scan.VersionScan()
	scan.ThemesScan()
	scan.AuthorScan()
	plugins.scan()
	scan.LoadPlugin()
	if (Arguments['brute']):
		scan.Brute_Force()

		

