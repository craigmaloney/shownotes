#!/usr/bin/env python

import argparse
from shownotes import ShowNotes

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
