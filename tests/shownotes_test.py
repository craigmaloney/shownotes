#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
from shownotes import ShowNotes

class ShowNotesTest(unittest.TestCase):
    """ Test the Shownotes to see if they work """

    def setUp(self):
        pass

    def test_load_ascii_shownotes(self):
        path = 'tests/test_files'
        aud_file = '/'.join([path, 'open_metalcast_043.aup'])
        json_file = '/'.join([path, 'playlist_043.json'])
        shownotes = ShowNotes(json_file, aud_file)
        notes = '\n'.join([note for note in shownotes.create_shownotes()])
        self.assertIn('Katatonia by 108 Not from 108 Not', notes)
        self.assertIn('Repent by Severed Fifth from Liberate', notes)
        self.assertIn('How To Get Signed To Sumerian Records (Redux) by Spiral Mountain from (Single)', notes)

    def test_load_non_ascii_shownotes(self):
        path = 'tests/test_files'
        aud_file = '/'.join([path, 'open_metalcast_instrumetalcast_005.aup'])
        json_file = '/'.join([path, 'playlist_instr_005.json'])
        shownotes = ShowNotes(json_file, aud_file)
        notes = '\n'.join([note for note in shownotes.create_shownotes()])
        self.assertIn(u"The Ground of All Being by Zarathustra from Yūgen", notes)

    def test_load_ascii_announce(self):
        path = 'tests/test_files'
        aud_file = '/'.join([path, 'open_metalcast_043.aup'])
        json_file = '/'.join([path, 'playlist_043.json'])
        shownotes = ShowNotes(json_file, aud_file)
        announce = '\n'.join([ann for ann in shownotes.create_announcement()])
        self.assertIn('Katatonia by 108 Not from the album 108 Not', announce)
        self.assertIn('Repent by Severed Fifth from Liberate', announce)
        self.assertIn('How To Get Signed To Sumerian Records (Redux) by Spiral Mountain from the album (Single)', announce)

    def test_load_non_ascii_announce(self):
        path = 'tests/test_files'
        aud_file = '/'.join([path, 'open_metalcast_instrumetalcast_005.aup'])
        json_file = '/'.join([path, 'playlist_instr_005.json'])
        shownotes = ShowNotes(json_file, aud_file)
        announce = '\n'.join([ann for ann in shownotes.create_announcement()])
        self.assertIn(u"The Ground of All Being by Zarathustra from Yūgen", announce)
