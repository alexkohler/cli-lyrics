#!/usr/bin/env python
# coding: utf-8
import re
import json
import urllib2
import sys
import string

import requests as r
from collections import Counter

# TODO figure this out
#from clilyrics import Fetcher
from bs4 import BeautifulSoup


def create_fetcher(type):
    """ returns a fetcher (e.g. via RapGenius, AZLyric, etc.) capable of retrieving lyrics and
    sanitizing them."""
    if type == "Genius":
        return GeniusFetcher()
    if type == "AZLyrics":
        return AZLyricsFetcher()
    raise ValueError('Unrecognized fetcher type provided: ' + type)


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

class AZLyricsFetcher(object):

    def LyricsForSong(self, searchQuery):
        url = 'https://search.azlyrics.com/search.php?q=' + str(searchQuery.replace(' ', '+'))
        # header = {'Authorization': 'Bearer ' + AUTH_CODE}
        # data = r.get(url)
        # should check for status of header here

        req = urllib2.Request(url, headers={'User-Agent': "Magic Browser"})
        con = urllib2.urlopen(req)
        html = con.read()

        soup = BeautifulSoup(html, 'html.parser')
        n = soup.find("div", {"class": "container main-page"})
        links = n.findAll('a')
        # find first song result
        songResultURL=''
        for link in links:
                if "/lyrics/" in str(link['href']):
                    songResultURL=link['href']
                    break
        
        req = urllib2.Request(songResultURL, headers={'User-Agent': "Magic Browser"})
        con = urllib2.urlopen(req)
        html = con.read()
        split = html.split('<!-- Usage of azlyrics.com content by any third-party lyrics provider is prohibited by our licensing agreement. Sorry about that. -->',1)
        split_html = split[1]
        split = split_html.split('</div>',1)
        lyrics = split[0]  

        return lyrics

        # grab first result
        #url = data['response']['hits'][0]['result']['url']
        #print(n)

    def SanitizeLyrics(self, lyrics):
        lyrics = lyrics.replace("\n", " ").replace("\r","").replace('\\u201d', "").replace('\\u201c', "").replace(
            "\\u2019", "").replace(",", "").replace("?", "").replace(".", "").replace("!", "").replace('"', '').replace("<br>","").replace("&quot;","")
        # TODO clean up regexes to only remove what they need to
        lyrics = lyrics.decode('unicode_escape').encode('ascii','ignore')
        # remove extra spaces
        lyrics = ' '.join(lyrics.split())
        # print lyrics
        # lyrics = re.sub('(<.*?>)',"",lyrics)
        # replace common html punctuation, some important sequences/punctuation may be missing
        lyrics = re.sub('&#34;|&#x22;|&ldquo;|&#147;|&#x93;|&rdquo;|&#148;|&#x94',"",lyrics)
        return lyrics.split(' ')
        # return lyrics


def main(argv):
    # My code here
    if len(sys.argv) != 2:
        print("Please enter a single search query ")
        exit()

    searchQuery = sys.argv[1]
    searchQuery.replace(" ", "%20")

    # flags for max number of words

    # pint

    if not searchQuery:
        print("no search query provided")

    # https://docs.genius.com/#/response-format-h1

    # TODO should probably call this statically - https://pythonspot.com/factory-method/
    f = create_fetcher("AZLyrics")

    raw_lyrics = f.LyricsForSong(searchQuery)
    sanitized_lyrics = f.SanitizeLyrics(raw_lyrics)

    print(sanitized_lyrics)
    # print(Counter(sanitized_lyrics))

    print(str(len(Counter(sanitized_lyrics))) + " unique words")

    # remove bracket

    # print(lyrics.strip()

if __name__ == "__main__":
    main(sys.argv)


# sanitize lyrics
