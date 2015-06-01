# -*- coding:utf8 -*-
import requests
import json


class CON(object):
    channels_url = 'http://www.douban.com/j/app/radio/channels'
   
      #获取频道列表  
    def get_channels(self):
        self.channel_list = [{
            u'name': u'红心兆赫',
            u'channel_id': -3, 
            }]
        rawjson = requests.get(self.__class__.channels_url,).text
        data = json.loads(rawjson)['channels']
        self.channel_list += data
        return self.channel_list

      #输出频道名称和频道id
    def channel(self):
        channel_dict = self.get_channels()
        for cid in channel_dict:
            print cid['name'].encode('utf-8'), cid['channel_id']
        channel_number = raw_input('**请输入id 选择频道: ')
        return channel_number



if __name__ == '__main__':
    a = CON()
    #print a.get_channels()
    print a.channel()