#-*- coding:utf8 -*-
import requests
import sys
import json
import os
import getpass
import urllib
import subprocess
import time
import control


reload(sys)
sys.setdefaultencoding('utf8')

TOKEN_PATH = os.path.expanduser('~/.db_token.json')
header = {
    'Content-Type': 'application/x-www-form-urlencoded',
    'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64)\AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.118 Safari/537.36',
}

def unicode2utf8(data):  #has problem
    rv = []
    for item in data:
        if isinstance(item, unicode):
            item = item.encode('utf8')
        if isinstance(item, list):
            item = unicode2utf8(item)
        rv.append(item)
    return rv


def login_douban(): #this function was completed
    email = raw_input('Email: ')
    password = getpass.getpass('Password: ')
    post_data = {
        'version': 100,
        'app_name': 'radio_desktop_win',
        'email': email,
        'password': password,
    }
    return post_data


class Get(object):
      #获取token值的url
    token_url = 'http://www.douban.com/j/app/login' 
      #获取频道列表的url
    channels_url = 'http://www.douban.com/j/app/radio/channels'

    def __init__(self):
        self.header = header
        self.TOKEN_PATH = TOKEN_PATH
        
        
      #获取token, expire, user_id值    this function was completed
    def get_token(self):
	       #如果上次保存在文件中则从文件获取
        if os.path.isfile(self.TOKEN_PATH):
            f = open(self.TOKEN_PATH).read()
            TOKEN = json.loads(f)
            return TOKEN
	      #如果还未获取，获取后保存到文件
        else:
            postdata = login_douban()
            rawjson = requests.post(self.__class__.token_url, headers=self.header, data=postdata).text
            decodejson = json.loads(rawjson)
            if decodejson['r'] == 0:
                print 'Login successfully...'
                TOKEN = {
                        'token': decodejson['token'],
                        'expire': decodejson['expire'],
                        'user_id': decodejson['user_id'],
                }
                if os.system('touch %s' % TOKEN_PATH) == 0:
                    with open(TOKEN_PATH, 'w') as f:
                        f.write(json.dumps(TOKEN))
                return TOKEN
            else:
                print decodejson['err']


      #返回某频道歌曲列表url，这个url经过请求会返回一个歌曲列表json，里面包含5首歌  
    def getsong_list_url(self):
          #从control模块导入，获取频道对应id
        what_channel = control.CON()  
        channel_id = what_channel.channel()
        token = self.get_token()
        v = {
            'version': 100,
            'app_name': 'radio_desktop_win',
            'channel': channel_id,       #频道id
            'type': 's',        #报告类型
            'sid': 1,           #song id
            }        
        token.update(v)
        song_list_url = 'http://www.douban.com/j/app/radio/people?' + urllib.urlencode(token)
        return song_list_url

   
if __name__ == '__main__':
    get = Get()
    print get.get_token()
    #print get.getsong_list_url()


