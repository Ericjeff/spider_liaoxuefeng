#!/usr/bin/python
# -*- encoding:utf-8 -*-

import urllib
import urllib2
import threading
import time
import random
import os
from bs4 import BeautifulSoup

'''
    BeautifulSoup 是一个可以从HTML或XML文件中提取数据的Python库
'''


#封装
class article:
    def __init__(self,title,readNum,content):
        self.title = title
        self.readNum = readNum
        self.content = content



class spider_python2_7:

    def __init__(self,domain,url,headers,values):
        self.domain = domain
        self.url = url
        self.headers = headers
        self.values = values

    '''
        将页面内容下载到本地
    '''
    def parse(self,url=None):

        #编码
        data = urllib.urlencode(self.values)
        #访问目标url
        #模拟登陆
        # req = urllib2.Request(url=self.url,headers=self.headers,data=data)
        url = self.domain+url if url!=None else self.url
        print url
        req = urllib2.Request(url=url,headers=self.headers)
        #响应的内容
        resp = urllib2.urlopen(req)
        #读取内容
        html = resp.read()
        return html

    '''
        获取页面的url地址
        html：通过parse获得的内容
    '''
    def getUrls(self,html):

        soup = BeautifulSoup(html)#"html.parser")

        ul = soup.find_all("ul")
        #我们需要的信息在倒数第二个中
        lis =  ul[len(ul)-1].find_all("li")
        urls = []
        for li in lis:
            #获取链接中的url地址
            urls.append(li.find("a")["href"])
        return urls


    '''
        获取内容，并存储到文件中
        location:文件存储的位置和文件名
    '''
    def getContent(self,urls,location):

        self.exists(location)
        f = open(location+"/python2_7.html","a+")
        print "开始爬虫>>>>>>>>>>>>>"
        i = 0
        htmlheader='''
            <!DOCTYPE html>
            <html lang="en">
            <head style='text-align:center'>
                <meta charset="UTF-8">
                <title>python2.7---廖雪峰</title>
            </head>
            <body>
        '''
        htmlend = '''
            </body>
            </html>
        '''
        f.write(htmlheader)
        for url in urls:
            html = self.parse(url)
            t = self._parseContent(html)
            f.write('\n\n\n\n\n<hr><hr><hr>')
            f.write("<p style='text-align:center'>%s</p>"%t.title)
            f.write(str('\n'))
            f.write("<p style='text-align:center'>%s</p>"%t.readNum)
            f.write("<p>链接为:<a href='%s'>%s</a></p>"%(self.domain+url,self.domain+url))
            f.write(str('\n')+str('\n')+str('\n')+t.content);
            i += 1
            print i
        f.write(htmlend)
        f.close()
        print "完成爬虫>>>>>>>>>>>>>"


    '''
        getContent()方法的一部分，主要是解析html页面，提取内容
    '''
    def _parseContent(self,html):

        soup = BeautifulSoup(html)
        #我们需要的内容全部在clss=x-content的div
        content = soup.find_all("div",class_="x-content")[0]
        #标题
        title = content.find("h4")
        #阅读量
        readNumber = content.find("div",class_="x-wiki-info")
        #正文
        content = content.find("div",class_="x-main-content")
        ps = content.find_all("p")
        #正文是存在元组中的，所以需要将所有元组中的内容合并
        contents = reduce(lambda x,y:str(x)+str('\n')+str(y) if y != None else str(x),ps)
        #封装到article
        t = article(title.string,readNumber.string,contents)
        return  t


    '''
        这个方法的目的是修改 getContent()存在本地的文件中的图片的获取地址
        location:文件存储的位置和文件名和getContent()的location一样
        location_modify:这个是将图片地址修改后文件的存放位置和文件
    '''
    def modifyImagesUrl(self,location,location_modify,urls):
        self.exists(location)
        self.exists(location_modify)
        f = open(location+"/python2_7.html","r")
        soup = BeautifulSoup(f,"html.parser")
        imgs = soup.find_all("img")
        print "开始修改图片的URL>>>>>>>>>>>>>"
        for i in range(len(imgs)):
            time.sleep(random.randint(0,2))
            img = imgs[i]
            img["src"]=urls[i]
            print random.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
            print img["src"]
        print "结束修改图片的URL>>>>>>>>>>>>>"
        f1 = open(location_modify+"/python2_7_new.html","a+")
        f1.writelines(str(soup))
        f1.close()
        f.close()


    '''
       获取线上的URL
       location:文件存储的位置和文件名和getContent()的location一样 
    '''
    def getOnlineImageUrl(self,location):

        self.exists(location)
        f = open(location+"/python2_7.html","r")
        soup = BeautifulSoup(f,"html.parser")
        imgs = soup.find_all("img")
        urls = []
        print "开始获取图片的URL>>>>>>>>>>>>>"
        for img in imgs:
            time.sleep(random.randint(0,2))
            urls.append(self.domain+img["src"])
            print random.choice(['success +1','success +2','success +3','success +4'])
            print self.domain+img["src"]

        print "结束获取图片的URL>>>>>>>>>>>>>"
        f.close()
        return urls

    '''
        将图片下载到本地
        location:图片存放的位置和getContent()的location一样
        location_picture:你下好的文件的位置文
    '''
    def getImagesToLocal(self,location,location_picture):

        self.exists(location)
        self.exists(location_picture)

        f = open(location+"/python2_7.html","r")
        soup = BeautifulSoup(f,"html.parser")
        imgs = soup.find_all("img")
        print "开始下载所有图片>>>>>>>>>>>>>"
        i = 0
        for img in imgs:
            picture = self.parse(img["src"])
            f = open(location_picture+"/%d.png"%i,"ab+")
            f.write(picture)
            f.close()
            i += 1
        print "结束下载所有图片>>>>>>>>>>>>>"
        f.close()


    '''
        获取本地图片URL
        location:图片存放的位置和getContent()的location一样
    '''
    def getLocalImageURL(self,location,location_localImages):
        self.exists(location)
        f = open(location+"/python2_7.html","r")
        soup = BeautifulSoup(f,"html.parser")
        imgs = soup.find_all("img")
        urls = range(len(imgs))
        urls = map(lambda x:location_localImages+"/"+str(x)+".png",urls)
        #添加特效
        print ".....................获取本地图片地址........................."
        for url in urls:
            time.sleep(random.randint(0,2))
            print random.choice(['++++++++++','==============','~~~~~~~~~~~~~~','***********'])
            print url
        print ".....................获取本地图片地址结束........................."
        f.close()
        return urls

    def exists(self,location):
        if not os.path.exists(location):
            os.makedirs(location)