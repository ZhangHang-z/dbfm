# -*- coding:utf8 -*-
import conf
import requests
import json
import subprocess
import time

p = None
def play(url):
    global p
    p = subprocess.Popen(["mpg123", url])

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
            print songlistdecode
            for ever in songlistdecode['song']:
                play(ever['url'])
                print "%smins" % round(int(ever['length']) / 60.00, 1), '*%s*' % ever['title'], '--', ever['artist']
                time.sleep(int(ever['length']))
                stop()


if __name__ == '__main__':
    a = conf.Get()
    song_list_url = a.getsong_list_url()
    playmp3(song_list_url)