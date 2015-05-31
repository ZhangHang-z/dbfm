# -*- coding:utf8 -*-
import requests
import json
import subprocess
import time
import connect
import os
import re
import functools
import sys
import getch


red = '\033[31;1m %s \033[1;m'
green = '\033[32;1m %s \033[1;m'
yellow = '\033[33;1m %smins \033[1;m'
blue = '\033[34;1m %s \033[1;m'
ultramarine = '\033[36;1m<%s>\033[1;m'
pred = '\033[35;1m%s \033[1;m'

PLAY_LOG = os.path.expanduser('~/.db_playlog.txt')
PRE_INFOMATION = '正在加载中...'


p = None

def play(url):
    global p
    if os.path.isfile(PLAY_LOG):
        log = PLAY_LOG
        p = subprocess.Popen(["mpg123", '-q', url])
    else:
        if os.system('touch %s' % PLAY_LOG) == 0:
            log = PLAY_LOG
            p = subprocess.Popen(["mpg123", '-q', url])   
        else:
            raise "touch logging file failed"
    

def stop():
    global p 
    if p:
        p.terminate()
        p = None


def rate(rate):
    return '★' * int(round(int(rate)))


def info(pre):
    if callable(pre):
        Fun = pre
        @functools.wraps(Fun)
        def internal(song_url):
            print PRE_INFOMATION
            return Fun(song_url)
        return internal
    else:
        def external(Fun):
            @functools.wraps(Fun)
            def internal(song_url):
                print pre
                return Fun(song_url)
            return internal
        return external


@info('载入歌曲中....')
def playmp3(song_url):
        while 1:
            song_list_url = song_url
            raw_song_list =requests.get(song_list_url).text
            songlistdecode = json.loads(raw_song_list)
            for ever in songlistdecode['song']:
                play(ever['url'])
                kwargs = {
                    'minutes': int(ever['length']),
                    'title': ultramarine % ever['title'],
                    'artist': green % ever['artist'],
                    'rate': pred % rate(ever['rating_avg']) 
                    }
                interface_show(**kwargs)
		        """ time.sleep(int(ever['length']))   
		            这里和time_remain() 函数冲突，下面time.sleep已经执行歌曲时长，这里再执行便又会重复
		        """
                stop()


def interface_show(**kwargs):
    print ' '*10, kwargs['title'], kwargs['artist'], kwargs['rate'], time_remain(kwargs['minutes'])


def time_remain(mins):
    count = 0
    while (count < mins):
        count += 1
        n = mins - count
        time.sleep(1)
        sys.stdout.write("%d \r" % n,)
        sys.stdout.flush()
        if not n:
            return 'completed'


def main():
    a = connect.Get()
    play = playmp3(a.getsong_list_url())


if __name__ == '__main__':
    main()


#blue % '正在播放...'
#yellow % round(int(ever['length']) / 60.00, 1)

