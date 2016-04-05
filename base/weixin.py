#coding=utf-8
import hashlib
from django.http import HttpResponse
from  django.views.generic import View
from django.core.exceptions import PermissionDenied
from django.views.decorators.csrf import csrf_protect,csrf_exempt
from bs4 import BeautifulSoup
from wechat.settings import WX_TOKEN,WX_EncodingAESKey,WX_messageCryptolevel,WX_APPID
from message.Message import Handler
from django.shortcuts import render_to_response
from django.template.loader import get_template
from WXBizMsgCrypt import  WXBizMsgCrypt

class Weixin(View):

    def __init__(self,token=WX_TOKEN,cryptolevel=WX_messageCryptolevel,appid=WX_APPID,encodingaeskey=WX_EncodingAESKey):
        self.__token = token
        self.__cryptolevel = cryptolevel.strip()
        if cryptolevel.strip() != 'plain':
            self.__crypt = WXBizMsgCrypt(token,encodingaeskey,appid)

    def post(self,request):
        if not self.checksig(request):
            raise PermissionDenied
        body = request.body
        if self.__cryptolevel != 'plain':
            signature = str(request.GET.get('signature'))
            timestamp = str(request.GET.get('timestamp'))
            nonce = str(request.GET.get('nonce'))
            ret, body = self.__crypt.DecryptMsg(request.body,signature,timestamp,nonce)
        soup = BeautifulSoup(body)
        if soup.msgtype:
            Content = {
                'ToUserName':soup.fromusername.string,
                'FromUserName':soup.tousername.string,
                'Content':soup.content.string
            }
            p = Handler(request.body)
            ret = p.handle()
            t = get_template(ret['template'])
            content = t.render(ret['Context'])
            if self.__cryptolevel != 'plain':
                content = self.__crypt.EncryptMsg(content,nonce)
            return HttpResponse(content,content_type="application/xml")
            #return render_to_response(ret['template'],ret['Context'],content_type="application/xml")
        return HttpResponse("")

    def checksig(self,request):
        signature=str(request.GET.get('signature'))
        timestamp=str(request.GET.get('timestamp'))
        nonce=str(request.GET.get('nonce'))
        tmpstr = ''.join(sorted([self.__token, timestamp, nonce]))
        tmpstr = hashlib.sha1(tmpstr).hexdigest()
        if tmpstr == signature:
            return True
        else:
            return False

    def get(self,request):
        if self.checksig(request):
            return HttpResponse(request.GET.get('echostr'))
        raise PermissionDenied

    @csrf_exempt #override
    def dispatch(self, *args, **kwargs):
        return super(Weixin, self).dispatch(*args, **kwargs)
