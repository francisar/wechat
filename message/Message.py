#coding=utf-8

#from django.core.exceptions import PermissionDenied
from bs4 import BeautifulSoup
from base.function import switch
from message.Text import Texthandler
import time

class Handler(object):

    def __init__(self,body):
        self.__soup=BeautifulSoup(body)
        self.__MsgType=self.__soup.msgtype.string
        self.__ToUserName=self.__soup.tousername.string
        self.__FromUserName=self.__soup.fromusername.string
        self.__CreateTime=self.__soup.createtime.string
        self.__MsgId=int(self.__soup.msgid.string)

    def handle(self):
        for case in switch(self.__MsgType):
            if case('text'):
                self.__Content = self.__soup.content.string
                return self.__text()
                break
            if case('image'):
                return self.__image()
                break
            if case('voice'):
                return self.__voice()
                break
            if case('video'):
                return self.__video()
                break
            if case('location'):
                return self.__location()
                break
            if case('link'):
                return self.__link()
                break

    def __text(self):
        text_handler=Texthandler(self.__Content)
        ret = text_handler.handle()
        Content = {
                                'ToUserName':self.__FromUserName,
                                'FromUserName':self.__ToUserName,
                                'CreateTime':time.time(),
                                'Content':str(ret)
                        }
        return {'template':'reply_text.xml','Context':Content}

    def __image(self):
        return ""

    def __voice(self):
        return ""

    def __video(self):
        return ""

    def __location(self):
        return ""

    def __link(self):
        return ""
