#!/usr/bin/env python 
# -*- coding: utf-8 -*- 

import requests
import sys
import json
import Queue
import threading
import time

class Zoomeye():
    def __init__(self,keyword,pagenum,thread):
        self.Search_keyword = keyword
        self.pagenum = pagenum
        self.TestIpArgs = []
        self.IPQueue = Queue.Queue()
        self.thread = thread
        self.vulnerabilitylist = []
        self.namelist = []
        self.resultlist = []
        self.mutex = threading.Lock()
        
    def reportstart(self):
        filename = str(time.strftime("%Y-%m-%d-%H-%M-%S",time.localtime(time.time())))
        self.html = open('./report/%s.html' %filename,'w')
        self.html.write("""
<html>
<head>
  <title>Lee Sin Report</title>
</head>
<body>
<h1 align="center">Lee Sin    v1.0</h1>
<p style="text-align:right">2016.9.17 by breadandham.com</p>
""")
        self.html.write('<p style="text-align:"right">Report generation date: %s</p>' %filename) 
        self.html.write('<hr style="height:1px;border:none;border-top:1px dashed #0066CC;" />')
    
    def GetIP(self):
        GetTokenUrl = 'https://api.zoomeye.org/user/login'
        userinfo ={"username": "1123302584@qq.com",
    		"password": "taoqi512512"}
        tokenrl = requests.post(GetTokenUrl,data = json.dumps(userinfo),verify=False)
        data = eval(tokenrl.text)
        Header = {'Authorization': 'JWT %s' %data['access_token']}
        page = 1
        if self.Search_keyword == None:
		    key = 'wordpress'
        else:
            key = self.Search_keyword
        while True:
            try:
                Searchurl = 'https://api.zoomeye.org/host/search?query=%s&page=%s'%(key,str(page))
                print 'Search in page :'+str(page)
                Searchre = requests.get(Searchurl,headers = Header,verify=False)
                GetData  = json.loads(Searchre.text)
                for i in GetData['matches']:
                    #print i['ip']
                    self.TestIpArgs.append(i['ip'])
                if self.pagenum != None:
                    if page < int(self.pagenum):
                        page+=1
                    else:
                        break
                else:
                    page=page+1
            except Exception,e:
                if str(e.message) == 'matches':
                    break
        for i in self.TestIpArgs:
            self.IPQueue.put(i)

    def readfile(self):
        file = open('./dict/vulnerability.txt')
        filedata = file.readlines()
        for line in filedata:
            tmp = line.split('\n')[0]
            self.vulnerabilitylist.append(tmp.split('====')[0])
            self.namelist.append(tmp.split('====')[1])

    def show(self):
        number = 0
        print 'Attack Program List: \n'
        for i in self.namelist:
            number = number+ 1
            print "\33[31m"'[+] '+str(number)+': '+i+"\033[0m"
        print '\n'
            

    def startthread(self):
        print 'Scanning IP quantity: '+str(len(self.TestIpArgs))
        print '\33[31m[+] WarningThis feature is only for reference, the need for manual testing scan results ! ! !\033[0m'
        threadlist = []
        for i in range(self.thread):
            t = threading.Thread(target=self.scan)
            t.start()
            threadlist.append(t)
        for i in threadlist:
            i.join()
        self.makereport()


    def makereport(self):
        self.html.write('<p style="text-align:"left">The target number of detected suspicious: %s</p>' %str(len(self.resultlist)))
        for line in self.resultlist:
            self.html.write(r'<li><a href="%s">%s</a>%s</li>' %(line.split('===')[0],line.split('===')[0],'     '+line.split('===')[1]))
            self.html.write('<hr style="height:1px;border:none;border-top:1px dashed #0066CC;" />')
        self.html.write('<p align="center">Wo Biao Ge Shi Hong Niu</p>')
        self.html.write('</body></html>')
        self.html.close()

    def scan(self):
        thread = threading.current_thread()
        while(1):
            try:
                ip = self.IPQueue.get(timeout = 1)
            except:
                break
            rootaddr = "http://{0}".format(ip)
            try:
                result = requests.get(rootaddr,timeout = 2)
            except:
                continue 
            for i in range(len(self.vulnerabilitylist)):
                if self.vulnerabilitylist[i]:
                    print '[+]'+thread.getName()+'\t'+rootaddr+self.vulnerabilitylist[i]
                    try:
                        R = requests.get(rootaddr+self.vulnerabilitylist[i],timeout = 3)
                        if R.status_code == 200:
                            self.mutex.acquire()
                            result = rootaddr+self.vulnerabilitylist[i]+'==='+self.namelist[i]
                            self.resultlist.append(result)
                            self.mutex.release()
                    except:
                        pass
                else:
                    break

        
