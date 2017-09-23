#!/usr/bin/python
# -*- encoding:utf-8 -*-

import threading
import time
import random
import spider


'''
    启动类
'''
class launch:

    def __init__(self,download_dir,online_dir,local_dir,picture_dir):
        self.download_dir = download_dir
        self.online_dir = online_dir
        self.local_dir = local_dir
        self.picture_dir = picture_dir
        self._start()

    def _start(self):
        domain = "https://www.liaoxuefeng.com"
        url = "https://www.liaoxuefeng.com/wiki/001374738125095c955c1e6d8bb493182103fac9270762a000/"
        user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:2.0.1) Gecko/20100101 Firefox/4.0.1"
        headers = {"User_agent":user_agent}
        values = {}#{"input1":"xxxxx","input2":"xxxxx","__EVENTTARGET":"btnLogin","__EVENTARGUMENT":""}

        #创建爬虫对象
        self.spider = spider.spider_python2_7(domain,url,headers,values)
        spider = self.spider
        #解析首页面
        html = spider.parse()
        #获取要爬取的URL
        urls = spider.getUrls(html)
        #通过遍历URL，将爬取的内容放到G:/zz文件夹下
        #spider.getContent(urls,self.download_dir)


    #处理线上的
    def _onlin_thread(self,spider,download_dir,online_dir):

        print "thread %s running!!!!"%threading.current_thread().name
        #获取图片线上地址
        urls = spider.getOnlineImageUrl(download_dir)

        #将文件中的img的地址转化为线上地址
        spider.modifyImagesUrl(download_dir,online_dir,urls)


    #处理本地的
    def _local_thread(self,spider,download_dir,local_dir,picture_dir):

        print "thread %s running!!!!"%threading.current_thread().name

        #将图片下载到本地
        spider.getImagesToLocal(download_dir,picture_dir)

        #获取本地图片的地址
        urls_l = spider.getLocalImageURL(download_dir,picture_dir)
        #将文件中的img的地址转化为本地地址
        spider.modifyImagesUrl(download_dir,local_dir,urls_l)


    '''
        多线程
    '''
    def start_thread(self):

        #创建连个线程
        online = threading.Thread(target=self._onlin_thread,name="online",args=(self.spider,self.download_dir,self.online_dir))
        local = threading.Thread(target=self._local_thread,name="local",args=(self.spider,self.download_dir,self.local_dir,self.picture_dir))

        #开始
        print "........................开始执行爬虫.........................."
        online.start()
        local.start()
        online.join()
        local.join()
        print "........................爬虫执行结束.........................."


    '''
        单线程
    '''
    def start(self):

        #获取图片线上地址
        urls = self.spider.getOnlineImageUrl(self.download_dir)

        #将文件中的img的地址转化为线上地址
        self.spider.modifyImagesUrl(self.download_dir,self.online_dir,urls)

        #将图片下载到本地
        self.spider.getImagesToLocal(self.download_dir,self.picture_dir)

        #获取本地图片的地址
        urls_l = self.spider.getLocalImageURL(self.download_dir,self.picture_dir)

        #将文件中的img的地址转化为本地地址
        self.spider.modifyImagesUrl(self.download_dir,self.local_dir,urls_l)


def start():
    #文件存放的目录
    #解析并下载到本地的文件的目录,元文件的目录
    download_dir = "G:/zz/"
    #将源文件中的图片地址改为线上的地址后存放的目录
    online_dir = download_dir+"/onlin_modify/"
    #将源文件中的图片地址改为线上的地址后存放的目录
    local_dir = download_dir+"/local_modify/"
    #本地图片的位置
    picture_dir =download_dir+"/picture/"

    spider = launch(download_dir,online_dir,local_dir,picture_dir)
    #spider.start_thread()
    spider.start()

start()