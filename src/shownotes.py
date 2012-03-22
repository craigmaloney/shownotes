#!/usr/bin/env python
import argparse
import datetime
import json
from BeautifulSoup import BeautifulStoneSoup


class ShowNotes(object):
    song_template = """<li>({time}) <a href="{url}">{title} by {artist} from {album}</a> ({license})</li>"""
    announcements = {
        "first":"That was {title} by {artist} from {album}.",
        "second":"Before that, {title} by {artist} from {album}.",
        "middle":"{title} by {artist} from {album}.",
        "last":"And starting off the show. {title} by {artist} from the album {album}."
    }

    def __init__(self, filename, audacity_file):
        """Docstrings!!!!!

        wtf is aud_timing?

        """
        with open(filename, 'rt') as f:
            self.playlist = json.load(f)
        self.aud_timing = {}
        self.find_timing(audacity_file)

    def find_timing(self, audacity_file):
        with open(audacity_file, 'rt') as aup_file:
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

            yield self.song_template.format(**i)

    def create_announcement(self):
        """I wouldn't print from here. What if you want to log, or email

        Generate the data, but then let someone else handle the view

        """
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
            yield self.announcements[position].format(**i)
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
    show = ShowNotes(args.json, args.audacity)
    print '\n'.join([note for note in show.create_shownotes()])
    print '\n'.join([ann for ann in show.create_announcement()])

if __name__ == '__main__':
    main()
