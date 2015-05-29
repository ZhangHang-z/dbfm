# -*- coding:utf8 -*-
import requests
import json
import subprocess
import time
import connect
import os
import re

red = '\033[31;1m %s \033[1;m'
green = '\033[32;1m %s \033[1;m'
yellow = '\033[33;1m %smins \033[1;m'
blue = '\033[34;1m %s \033[1;m'
ultramarine = '\033[36;1m *%s* \033[1;m'

PLAY_LOG = os.path.expanduser('~/.db_playlog.txt')


p = None

def play(url):
    global p
    if os.path.isfile(PLAY_LOG):
        log = PLAY_LOG
        p = subprocess.Popen(["mpg123", url, '>>', log])
    else:
        if os.system('touch %s' % PLAY_LOG) == 0:
            log = PLAY_LOG
            p = subprocess.Popen(["mpg123", url, '>>', log])
        else:
            raise "touch logging file failed"
    
def stop():
    global p 
    if p:
        p.terminate()
        p = None


def playmp3(song_url):
        while 1:
            song_list_url = song_url
            raw_song_list =requests.get(song_list_url).text
            songlistdecode = json.loads(raw_song_list)
            for ever in songlistdecode['song']:
                play(ever['url'])
                print blue % '正在播放 ...' 
                print yellow % round(int(ever['length']) / 60.00, 1), ultramarine % ever['title'], green % ever['artist']
                time.sleep(int(ever['length']))
                stop()


if __name__ == '__main__':
    a = connect.Get()
    playmp3(a.getsong_list_url())

