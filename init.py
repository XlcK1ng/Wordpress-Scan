import argparse
from random import randint

HEADERS = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36",
           "X-Forwarded-For": '%s:%s:%s:%s' % (randint(1, 255),
               randint(1, 255), randint(1, 255), randint(1, 255)),
           "Content-Type": "application/x-www-form-urlencoded",
           "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
           "Connection": "keep-alive"}

def GetParameter():
	parser = argparse.ArgumentParser(prog = 'Wordpress scan',usage = 'scan.py [options]',add_help = False)
	parser.add_argument('-u',dest = 'url',help = 'Enter the url is detected')
	parser.add_argument('-h',action = 'help',help = 'Output help')
	parser.add_argument('-b',dest = 'brute',action = 'store_true',default = False,help = 'Are you trying to brute force')
	parser.add_argument('-n',dest = 'uname',help = 'Specifies Username')
	parser.add_argument('-d',dest =  'pwd',help  = 'Password dictionary')
	parser.add_argument('--bt',dest = 'bthreads',type = int, default = 2,help = 'Blasting login password of the number of threads')
	parser.add_argument('--pt',dest = 'pthreads',type = int, default = 2,help = 'Number of Thread Checker Plugin')
	args = parser.parse_args()
	return args.__dict__