#!/usr/bin/env python
import argparse
import datetime
import json
from BeautifulSoup import BeautifulStoneSoup


class ShowNotes(object):
    song_template = unicode("""<li>({time}) <a href="{url}">{title} by {artist} from {album}</a> ({license})</li>""")
    announcements = {
        "first": u"That was {title} by {artist} from the album {album}.",
        "second": u"Before that, {title} by {artist} from {album}.",
        "middle": u"{title} by {artist} from {album}.",
        "last": u"And starting off the show. {title} by {artist} from the album {album}."
    }
    cuesheet_template = """  TRACK {tracknumber} AUDIO
    TITLE "{title}"
    PERFORMER "{artist}"
    INDEX 01 {time}"""
    cuesheet_header = """
REM GENRE "Metal"
REM DATE "2012"
PERFORMER "Open Metalcast"
TITLE "Open Metalcast Episode XXX"
FILE "open_metalcast_XXX.{extension}"
"""

    def __init__(self, filename, audacity_file):
        """ Initialize the shownotes piece
        :param filename: playlist JSON file
        :type filename: string
        :param audacity_file: File to get audacity timings
        :type audacity_file: string

        note:: aud_timing will contain the audacity track name and time code
        """
        with open(filename, 'rt') as f:
            self.playlist = json.load(f)
        self.aud_timing = {}
        self.find_timing(audacity_file)

    def format_timing(self, hour, minute, second):

        time = ''
        if int(hour) > 0:
            time = '{}:{}:{}'.format(hour, minute, second)
        else:
            time = '{}:{}'.format(minute, second)
        return time

    def find_timing(self, audacity_file):
        """ Finds the Audacity timings in the Audacity file.

        :param audacity_file: Audacity file to find timings
        :type audacity_file: string
        """

        with open(audacity_file, 'rt') as aup_file:
            bs = BeautifulStoneSoup(aup_file)
            tracks = bs.findAll('wavetrack')
            for track in tracks:
                wavestart = track.findAll('waveclip')
                secs = int(float(wavestart[0]['offset']))
                timestamp = str(datetime.timedelta(seconds=secs))
                self.aud_timing[track['name']] = timestamp

    def create_shownotes(self):
        """ Create the show notes from a template
        :rtype: string
        """

        for i in self.playlist:
            tmp_timing = self.aud_timing[i['audacity']]
            hour, minute, second = tmp_timing.split(':')
            i['time'] = self.format_timing(hour, minute, second)

            yield self.song_template.format(**i)

    def create_cuesheet(self):
        """ Creates a cuesheet based on the playlist and audacity timings """

        num_tracks = 0
        for i in self.playlist:

            num_tracks = num_tracks + 1
            i['tracknumber'] = num_tracks

            tmp_timing = self.aud_timing[i['audacity']]
            hour, minute, second = tmp_timing.split(':')
            i['time'] = "{}:{}".format(
                    self.format_timing(hour, minute, second),
                    '00')

            yield self.cuesheet_template.format(**i)

    def create_announcement(self):
        """ Generate a TTS friendly announcement
        Reverses the playlist to read from bottom-up.
        """

        num_tracks = 0
        self.playlist.reverse()
        for track in self.playlist:
            num_tracks = num_tracks + 1
            position = 'middle'
            if num_tracks == 1:
                position = 'first'
            elif num_tracks == 2:
                position = 'second'
            elif num_tracks == len(self.playlist):
                position = 'last'
            yield self.announcements[position].format(**track)
        self.playlist.reverse()


def configure():
    """ Command-line arguments """
    parser = argparse.ArgumentParser(description='Shownotes Application')
    parser.add_argument('--audacity', '-a',
            action='store',
            required=True,
            help='audacity file')
    parser.add_argument('--json', '-j',
            action='store',
            required=True,
            help='json playlist file')
    parser.add_argument('--cue', '-c',
            action='store_true',
            help='Generate a cuesheet')
    args = parser.parse_args()
    return args


def main():
    args = configure()
    show = ShowNotes(args.json, args.audacity)
    print '\n'.join([note for note in show.create_shownotes()])
    print
    print '\n'.join([ann for ann in show.create_announcement()])

    if 'cue' in args:
        for extension in ['mp3', 'ogg']:
            filename = 'cuesheet_{extension}.cue'.format(extension=extension)
            with open(filename, 'wt') as f:
                f.write(show.cuesheet_header.format(\
                        extension=extension))
                f.write('\n'.join([track for track in show.create_cuesheet()]))

if __name__ == '__main__':
    main()
