#-*- coding:utf8 -*-
import requests
import sys
import json
import os
import getpass
import urllib

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
    token_url = 'http://www.douban.com/j/app/login'
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

    #获取频道列表  not complete
    def get_channels(self):
        self.channel_list = [{
            u'name': u'红心兆赫',
            u'channel_id': -3, 
        }]
        rawjson = requests.get(self.__class__.channels_url,).text
        data = json.loads(rawjson)['channels']
        self.channel_list += data
        return self.channel_list
    

    def get_song_list(self):
        token = self.get_token()
        v = {
            'version': 100,
            'app_name': 'radio_desktop_win',
            'channel': 4, 
            'type': 'e',
            'sid': 1}
        token.update(v)
        print urllib.urlencode(token)
        print
        song_url = 'http://www.douban.com/j/app/radio/people?' + urllib.urlencode(token)
        raw =requests.get(song_url, headers=token).text
        return json.loads(raw)
        
if __name__ == '__main__':
    get = Get()
    print get.get_token()
    #print get.get_channels()
    print get.get_song_list()
