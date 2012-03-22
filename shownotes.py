#!/usr/bin/env python
import json
import argparse
import datetime
from BeautifulSoup import BeautifulStoneSoup

class ShowNotes(object):
    def __init__(self,filename):
        self.file = open(filename, 'rt')
        self.playlist = json.load(self.file)
        self.file.close
        self.song_template = """<li>({time}) <a href="{url}">{title} by {artist} from {album}</a> ({license})</li>"""
        self.announcements = {
                "first":"That was {title} by {artist} from {album}.",
                "second":"Before that, {title} by {artist} from {album}.",
                "middle":"{title} by {artist} from {album}.",
                "last":"And starting off the show. {title} by {artist} from the album {album}."
                }
        self.aud_timing = {}

    def find_timing(self, audacity_file):
        aup_file = open(audacity_file, 'rt')
        bs = BeautifulStoneSoup(aup_file)
        tracks = bs.findAll('wavetrack')
        for track in tracks:
            wavestart = track.findAll('waveclip')
            secs = int(float(wavestart[0]['offset']))
            timestamp = str(datetime.timedelta(seconds=secs))
            self.aud_timing[track['name']] = timestamp

    def create_shownotes(self):
        for i in self.playlist:
            tmp_timing = self.aud_timing[i['audacity']]
            hour, minute, second = tmp_timing.split(':')
            if int(hour) > 0:
                i['time'] = '{}:{}:{}'.format(hour, minute, second)
            else:
                i['time'] = '{}:{}'.format(minute, second)

            print self.song_template.format(**i)

    def create_announcement(self):
        num_tracks = 0
        self.playlist.reverse()
        for i in self.playlist:
            num_tracks = num_tracks + 1
            position = 'middle'
            if num_tracks == 1:
                position = 'first'
            elif num_tracks == 2:
                position = 'second'
            elif num_tracks == len(self.playlist):
                position = 'last'
            print self.announcements[position].format(**i)
        self.playlist.reverse()

def configure():
    parser = argparse.ArgumentParser(description='Shownotes Application')
    parser.add_argument('--audacity', '-a', 
            action='store',
            required=True,
            help='audacity file')
    parser.add_argument('--json', '-j', 
            action='store',
            required=True,
            help='json playlist file')

    args = parser.parse_args()

    return args

def main():
    args = configure()
    print args
    show = ShowNotes(args.json)
    show.find_timing(args.audacity)
    show.create_shownotes()
    show.create_announcement()

if __name__ == '__main__':
    main()

