#-*- coding:utf8 -*-


def playmp3(self):
        while 1:
            song_list_url = self.getsong_list_url()
            raw_song_list =requests.get(song_list_url).text
            songlistdecode = json.loads(raw_song_list)
            print songlistdecode
            for ever in songlistdecode['song']:
                play(ever['url'])
                print "%smins" % round(int(ever['length']) / 60.00, 1), '*%s*' % ever['title'], '--', ever['artist']
                time.sleep(int(ever['length']))
                stop()