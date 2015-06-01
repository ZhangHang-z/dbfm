# -*- coding:utf8 -*-
import requests
import json
import subprocess
import time
import os
import re
import functools
import sys
import connect
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

def player(url):
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
                player(ever['url'])
                kwargs = {
                    'minutes': int(ever['length']),
                    'title': ultramarine % ever['title'],
                    'artist': green % ever['artist'],
                    'rate': pred % rate(ever['rating_avg']),
                    'publish': ever['public_time'],
                    }
                interface_show(**kwargs)
                """ >>> time.sleep(int(ever['length']))   
		            这里和time_remain() 函数冲突，下面time.sleep已经执行歌曲时长，这里再执行便又会重复
                """
                stop()


def interface_show(**kwargs):
    print kwargs['title'], kwargs['artist'], kwargs['publish'], kwargs['rate'], time_remaining(kwargs['minutes'])
    


def time_remaining(mins):
    count = 0
    #ex_length = len(str(mins))
    #sys.stdout.write(' ' * len(str(mins)))
    while (count < mins):
        count += 1
        n = mins - count
        length = len(str(n))
        time.sleep(1)
        sys.stdout.write(str(n) + "\b"*length)
        sys.stdout.flush()
        if not n:
            return 'completed'


def main():
    get = connect.Get()
    playmp3(get.getsong_list_url())


if __name__ == '__main__':
    main()



