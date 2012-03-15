#!/usr/env python

import json

file = open('playlist.json', 'rt')
playlist = json.load(file)
file.close
