#coding=utf-8
from wechat.settings import WX_TOKEN,WX_EncodingAESKey,WX_APPID,WX_APPSECRET
import requests
from django.core.cache import cache
class WechatApi(object):
    URL_ROOT_API = 'https://api.weixin.qq.com'
    URL_GET_TOKEN = URL_ROOT_API + '/cgi-bin/token' + '?grant_type=client_credential&appid=%s&secret=%s'
    #URL_GET_DEPARTMENT = URL_ROOT_API + '/cgi-bin/department/list' + '?access_token=%s&id=%s'
    #URL_GET_DEPARTMENT_USER = URL_ROOT_API + '/cgi-bin/user/simplelist' + '?access_token=%s&department_id=%s&fetch_child=%s&status=%s'
    #URL_GET_USER_INFO = URL_ROOT_API + '/cgi-bin/user/getuserinfo' + '?access_token=%s&code=%s'
    URL_GET_WECHAT_IP = URL_ROOT_API + '/cgi-bin/getcallbackip' + '?access_token=%s'
    URL_MENU_DELETE = URL_ROOT_API + '/cgi-bin/menu/delete' +"access_token=%s"
    URL_MENU_CREATE = URL_ROOT_API + '/cgi-bin/menu/delete' +"access_token=%s"
    #URL_MESSAGE_SEND = URL_ROOT_API + '/cgi-bin/message/send' + '?access_token=%s'
    #URL_MEDIA_UPLOAD = URL_ROOT_API + '/cgi-bin/media/upload' + '?access_token=%s&type=%s'
    #URL_GET_USER_DETAIL = URL_ROOT_API + '/cgi-bin/user/get' + "?access_token=%s&userid=%s"
    URL_ROOT_AUTH = 'https://open.weixin.qq.com'
    URL_AUTHORIZE = URL_ROOT_AUTH + '/connect/oauth2/authorize' + \
                    '?appid=%s&redirect_uri=%s&response_type=code&scope=snsapi_base&state=STATE#wechat_redirect'

    def __init__(self, appid=WX_APPID, secret=WX_APPSECRET, token=WX_TOKEN, encoding_aes_key=WX_EncodingAESKey):
        """
        @:param corpid --- 企业号 orpid
        @:param corpsecret --- 企业号 corpsecret
        @:param token --- 由各自的企业任意填写，用于生成签名，请看管理员界面
        @:param EncodingAESKey --- AES秘钥的Base64，为消息体进行加密准备
        """
        self.__appid = appid
        self.__secret = secret
        self.__token = token
        self.__encoding_aes_key = encoding_aes_key
        self.__access_token = None
        #if self.__token and self.encoding_aes_key:
        #    self.wxcpt = WXBizMsgCrypt(self.token, self.encoding_aes_key, self.corpid)
        #else:
        #    self.wxcpt = None

    def get_json_from_wechat(self, url,method='get',data=None):
        """从微信接口请求数据，错误或异常会直接抛出"""
        if method.lower() == 'get':
            response = requests.get(url)
        elif method.lower() == 'post':
            response = requests.post(url=url,data=data)
        if response.status_code != 200:
            raise Exception(u'status_code is not 200')
        result = response.json()
        if 'errcode' in result and result['errcode'] != 0:
            raise Exception(u'Wechat Error! %s %s' % (result['errcode'], result['errmsg']))
        return result

    def get_access_token(self):
        """获取access_token，利用django cache进行缓存，缓存时间为过期时间7200秒减掉100秒"""
        token_cache_key = self.__appid + '_access_token'
        self.__access_token = cache.get(token_cache_key, None)
        if self.__access_token is None:
            url = self.URL_GET_TOKEN % (self.__appid, self.__secret)
            result = self.get_json_from_wechat(url)
            self.__access_token = result["access_token"]
            cache.set(token_cache_key, self.__access_token, result['expires_in'] - 100)
        return self.__access_token

    def get_authorize_url(self, redirect_uri):
        return self.URL_AUTHORIZE % (self.__appid, redirect_uri)

    def delete_menu(self):
        access_token = self.get_access_token()
        url = self.URL_MENU_DELETE % access_token
        return self.get_json_from_wechat(url)
    
    def create_menu(self,data):
        access_token = self.get_access_token()
        url = self.URL_MENU_CREATE % access_token
        return self.get_json_from_wechat(url,"post",data)

    #def first_verify(self, msg_signature, timestamp, nonce, echostr):
    #    """
    #    回调模式开启的验证
    #    @:param msg_signature: weixin crypt signature
    #    @:param timestamp: timestamp
    #    @:param nonce: random number
    #    @:param echostr: the plaintext after crypt
    #    @:return decode string and return echostr which is original string
    #    """
    #    echos = urllib.unquote(echostr)
    #    # call function in WXBizMsgCrypt
    #    ret, result = self.wxcpt.VerifyURL(msg_signature, timestamp, nonce, echos)
    #    return result

    #def decrypt_data(self, data, sig, time, nonce):
    #    """对数据解密"""
    #    ret, result = self.wxcpt.DecryptMsg(data, sig, time, nonce)
    #    return result

    #def upload_media(self, media_path, media_name=None, media_type='image'):
    #    """上传多媒体文件
    #    @:param media form-data中媒体文件标识，有filename、filelength、content-type等信息，文件的open对象
    #    @:param m_type 文件类型，分别有图片（image）、语音（voice）、视频（video），普通文件(file)
    #    @:return 请求成功的return格式{
    #                                     "type": "image",
    #                                     "media_id": "1G6nrLmr5EC3MMb_-zK1dDdzmd0p7cNliYu9V5w7o8K0",
    #                                     "created_at": "1380000000"
    #                                 }
    #    """
    #    if not self.access_token:
    #        self.get_access_token()
    #    media_name = media_name or media_path.split('/')[-1]
    #    url = self.URL_MEDIA_UPLOAD % (self.access_token, media_type)
    #    with open(media_path, 'rb') as f:
    #        response = requests.post(url, files={media_name: f})
    #        result = response.json()
    #        if 'errcode' in result and result['errcode'] != 0:
    #            raise Exception(u'Wechat Error! %s %s' % (result['errcode'], result['errmsg']))
    #        return result

    def get_wechat_ip(self):
        """获取微信服务器的ip段"""
        if not self.__access_token:
            self.get_access_token()
        result = self.get_json_from_wechat(self.URL_GET_WECHAT_IP % self.__access_token)
        return result['ip_list']


