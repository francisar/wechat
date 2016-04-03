#coding=utf-8
import hashlib
from django.http import HttpResponse,HttpResponseRedirect
from  django.views.generic import View
from django.core.exceptions import PermissionDenied
from django.views.decorators.csrf import csrf_protect,csrf_exempt
from bs4 import BeautifulSoup
import httplib
import json
from cloudworkstation_weixin.message.Message import Handler
from django.shortcuts import render_to_response
class Weixin(View):
	__token = ''
	def __init__(self,token='asfe9faefa'):
		self.__token=token
		#print token
	def post(self,request):
		#print 'here'
		if not self.checksig(request):
			raise PermissionDenied
		soup = BeautifulSoup(request.body)
		#print request.body
		#if True:
		if soup.msgtype:
			Content = {
				'ToUserName':soup.fromusername.string,
				'FromUserName':soup.tousername.string,
				'Content':soup.content.string
			}
			p = Handler(request.body)
			ret = p.handle()
			#Content = {
			#	'ToUserName':'wer',
			#	'FromUserName':'qe',
			#	'CreateTime':time.time(),
			#	'Content':'qwer'
			#}
			#print Content
			#print ret
			return render_to_response(ret['template'],ret['Context'],content_type="application/xml")
		# do something here ...
		# and return the specified content for the request user.
		return HttpResponse('')
	def checksig(self,request):
		signature=str(request.GET.get('signature'))
                timestamp=str(request.GET.get('timestamp'))
                nonce=str(request.GET.get('nonce'))
		#print signature
		#print sorted([self.__token, timestamp, nonce])
		tmpstr = ''.join(sorted([self.__token, timestamp, nonce]))
		#print tmpstr
		tmpstr = hashlib.sha1(tmpstr).hexdigest()
		#print tmpstr
		if tmpstr == signature:
			return True
		else:
			return False
	def get(self,request):
		if self.checksig(request):
			return HttpResponse(request.GET.get('echostr'))
		raise PermissionDenied
 
	#def send_request(self, host, path, method, port=443, params={}):
	#	client = httplib.HTTPSConnection(host, port)
	#	path = '?'.join([path, urllib.urlencode(params)])
	#	client.request(method, path)
	#	res = client.getresponse()
	#	if not res.status == 200:
	#		return False, res.status
 	#	return True, json.loads(res.read())
	#def dispatch(self,request):
	#	print 'dispatch'
	#def as_view(self):
	#	print 'as_view'
	@csrf_exempt #override
    	def dispatch(self, *args, **kwargs):
        	return super(Weixin, self).dispatch(*args, **kwargs)
