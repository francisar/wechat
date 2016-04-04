#coding=utf-8
from base.function import switch

class Texthandler(object):

    __iplist = ('ldap.francis.com',)
    __command = ''
    __args =  ''
    __result = None
    def __init__(self,text_msg):
        self.__text_msg=text_msg
        self.__check_command()

    def __check_command(self):
        split_temp=self.__text_msg.split(' ',1)
        if len(split_temp)<2:
            self.__command="help"
        else:
            self.__command=split_temp[0]
            self.__args=split_temp[1]
    def __do_command(self):
        for case in switch(self.__command):
            if case('help'):
                break
            if case():
                break
        return self.__result

    def handle(self):
        return self.__do_command()