#!/usr/bin/env python
# coding: utf-8
import re
import urllib2

import requests as r

from bs4 import BeautifulSoup


# Your genius API auth code goes here
AUTH_CODE = ''

class GeniusFetcher(object):

    def LyricsForSong(self, searchQuery):
        url = 'https://api.genius.com/search?q=' + searchQuery
        header = {'Authorization': 'Bearer ' + AUTH_CODE}
        data = r.get(url, headers=header).json()
        # should check for status of header here

        # grab first result
        url = data['response']['hits'][0]['result']['url']
        print('Resolved to URL ' + url)

        # load that url's html into memory (need to change user agent to avoid 403 error)
        req = urllib2.Request(url, headers={'User-Agent': "Magic Browser"})
        con = urllib2.urlopen(req)
        html = con.read()

        # grab html between lyric tags
        html_doc = html
        lyrics = ''
        start = False
        soup = BeautifulSoup(html_doc, 'html.parser')
        for node in soup.findAll("div", {"class": "song_body-lyrics"}):
            lyrics += ''.join(node.findAll(text=True))

        matches = re.findall(r'sse\\n(.+?)/sse', repr(lyrics.lower()))

        # TODO exception here
        s = matches[0]

        return s

    # SanitizeLyrics sanitizes the raw lyrics returned from LyricsForSong
    def SanitizeLyrics(self, lyrics):
        # TODO clean this up - probably better regexes you could run here with a whitelist of what you care about
        sanit = lyrics.replace("\\n", " ").replace('\\u201d', "").replace('\\u201c', "").replace(
            "\\u2019", "").replace(",", "").replace("?", "").replace(".", "").replace("!", "").replace('"', '')

        # TODO smash this into a single regex?
        # brackets
        sanit = re.sub(r'\[.*?\]', '', sanit)
        # parens
        sanit = re.sub(r'\(.*?\)', '', sanit)
        # curlys
        sanit = re.sub(r'\{.*?\}', '', sanit)

        sanit=sanit.replace('\\', "")

        # remove extra spaces
        sanit = ' '.join(sanit.split())

        
        #TODO remove: i, the, and, 

        # TODO nouns only?

        return sanit.split(' ')