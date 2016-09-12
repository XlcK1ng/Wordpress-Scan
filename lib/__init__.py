import argparse
from random import randint

HEADERS = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36",
           "X-Forwarded-For": '%s:%s:%s:%s' % (randint(1, 255),
               randint(1, 255), randint(1, 255), randint(1, 255)),
           "Content-Type": "application/x-www-form-urlencoded",
           "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
           "Connection": "keep-alive"}

		

def GetParameter():

	print '''
 _    _                  _ ______                            _____                    
| |  | |                | || ___ \                          /  ___|                   
| |  | |  ___   _ __  __| || |_/ /_ __  ___  ___  ___       \ `--.   ___  __ _  _ __  
| |/\| | / _ \ | '__|/ _` ||  __/| '__|/ _ \/ __|/ __|       `--. \ / __|/ _` || '_ \ 
\  /\  /| (_) || |  | (_| || |   | |  |  __/\__ \\__ \      /\__/ /| (__| (_| || | | |
 \/  \/  \___/ |_|   \__,_|\_|   |_|   \___||___/|___/      \____/  \___|\__,_||_| |_|

'''
	parser = argparse.ArgumentParser(prog = 'Wordpress scan',usage = 'scan.py [options]',add_help = False)

	parser.add_argument('-u',dest = 'url',help = 'Enter the URL to be detected example:baidu.com')

	parser.add_argument('-h',action = 'help',help = 'export help')

	parser.add_argument('-b',dest = 'brute',action = 'store_true',default = False,help = 'Are you trying to brute force')
	
	parser.add_argument('-n',dest = 'uname',help = 'Specifies Username')
	
	parser.add_argument('-d',dest =  'pwd',help  = 'Password dictionary')

	
	parser.add_argument('--bt',dest = 'bthreads',type = int, default = 2,help = 'Blasting login password of the number of threads')
	
	parser.add_argument('--pt',dest = 'pthreads',type = int, default = 2,help = 'Number of Thread Checker Plugin')
	
	parser.add_argument('--show',dest = 'exp',action = 'store_true',default = False,help = 'Shows the attack program that can be used')
	
	args = parser.parse_args()
	return args.__dict__