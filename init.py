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
	parser.add_argument('-u',dest = 'url',help = 'input url')
	parser.add_argument('-h',action = 'help',help = 'output help')
	parser.add_argument('-b',dest = 'brute',action = 'store_true',default = False,help = 'brute force')
	parser.add_argument('-n',dest = 'uname',help = 'username')
	parser.add_argument('-d',dest =  'pwd',help  = 'password.txt')
	parser.add_argument('-p',dest = 'proccess',type = int,default = 2,help = 'proccess num')
	parser.add_argument('-t',dest = 'threads',type = int, default = 2,help = 'threads num')
	args = parser.parse_args()
	return args.__dict__