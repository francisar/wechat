#!/usr/bin/python
# -*- coding:utf-8 -*-

import sys
import ConfigParser
import time
import socket

class Config:

    def __init__(self, path='config.ini'):
        self.path = path
        self.cf = ConfigParser.ConfigParser()
        self.cf.read(self.path)

    def get(self, field, key):
        try:
            result = self.cf.get(field, key)
        except:
            result = ""
        return result

    def set(self, filed, key, value):
        try:
            self.cf.set(filed, key, value)
            self.cf.write(open(self.path,'w'))
        except:
            return False
        return True


def read_config(config_file_path, field, key):
    cf = ConfigParser.ConfigParser()
    try:
        cf.read(config_file_path)
        result = cf.get(field, key)
    except:
        sys.exit(1)
    return result


def write_config(config_file_path, field, key, value):
    cf = ConfigParser.ConfigParser()
    try:
        cf.read(config_file_path)
        cf.set(field, key, value)
        cf.write(open(config_file_path,'w'))
    except:
        sys.exit(1)
    return True


class switch(object):
    def __init__(self,value):
        self.__value = value
        self.__fall = False
    def __iter__(self):
        yield self.__match
        raise StopIteration
    def __match(self,*args):
        if self.__fall or not args:
            return True
        elif self.__value in args:
            self.__value = True
            return True 
        else:
            return False


def get_now():
    return time.strftime('%Y-%m-%dT%H:%M:%S',time.localtime(time.time()))

def datetime_timestamps(timestring):
    return time.mktime(time.strptime(timestring,'%Y-%m-%dT%H:%M'))

