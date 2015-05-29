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
        #p = os.system('mpg123 %s' % url)
        p = subprocess.Popen(["mpg123", url])
    else:
        if os.system('touch %s' % PLAY_LOG) == 0:
            log = PLAY_LOG
            #p = os.system('mpg123 %s' % url)
            p = subprocess.Popen(["mpg123", url])
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
                    'minutes': yellow % round(int(ever['length']) / 60.00, 1),
                    'title': ultramarine % ever['title'],
                    'artist': green % ever['artist'],
                    'rate': pred % rate(ever['rating_avg']) 
                    }
                interface_show(**kwargs)
                time.sleep(int(ever['length']))
                stop()


def interface_show(**kwargs):
    print blue % '正在播放...', kwargs['title'], kwargs['artist'], kwargs['minutes'], kwargs['rate']


if __name__ == '__main__':
    a = connect.Get()
    playmp3(a.getsong_list_url())


'''('%s %s %s %s %s' % (blue % '正在播放...', kwargs['title'], 
                            kwargs['artist'], kwargs['minutes'], kwargs['rate']) )'''