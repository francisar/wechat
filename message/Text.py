#coding=utf-8
from base.function import switch
#from wechat.common.ldapapi import LdapApi
#import reply_data
class Texthandler(object):
	__iplist = ('ldap.francis.com',)
	__command = ''
	__args =  ''
	__result = None
	#_ldapapi = None
	def __init__(self,text_msg):
		self.__text_msg=text_msg
		self.__check_command()
		#return ""
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
				#self.__Content = self.__soup.content.string
				#print  self.__MsgType+self.__ToUserName+self.__FromUserName+self.__CreateTime+self.__Content
				self.__result = reply_data.help_text
				#print self.__result
				break
			if case('adduser'):
				#print self.__MsgType
				#return self.__image()
				username = self.__args.split(' ',1)[0]
				#print username
				api = LdapApi(username,self.__iplist)
				ret = api.call({'action': 'adduser'})
				self.__result = self.__ldap_error(ret["ret"])
				break
			if case('deluser'):
				#print self.__MsgType
				username = self.__args.split(' ',1)[0]
				api = LdapApi(username,self.__iplist)
				ret = api.call({'action': 'deluser'})
				self.__result = self.__ldap_error(ret["ret"])
				break
			if case('setpasswd'):
				#print self.__MsgType
				args = self.__args.split(' ',1)
				if len(args)<2:
					self.__result = reply_data.help_text
				else:
					username = args[0]
					password = args[1]
					api = LdapApi(username,self.__iplist)
					ret = api.call({'action': 'setpasswd','passwd':password})
					self.__result = self.__ldap_error(ret["ret"])
				break
			if case('vpnon'):
				username = self.__args.split(' ',1)[0]
				api = LdapApi(username,self.__iplist)
				ret = api.call({'action': 'vpnon'})
				self.__result = self.__ldap_error(ret["ret"])
				break
			if case('link'):
				#print self.__MsgType
				return self.__link()
				break
			if case():
				#print self.__MsgType
				self.__result = reply_data.help_text
				break
		return self.__result
	def __ldap_error(self,ret):
		for case in switch(ret):
			if case(0):
				return "success"
				break
			if case(1):
				if self.__command == "adduser":
					return "用户已存在"
				else :
					return "用户不存在"
				break
			if case(1000):
				return "操作失败"
				break
	def handle(self):
		return self.__do_command()