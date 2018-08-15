#!/usr/bin/env python
# coding: utf-8
import re
import urllib2

from bs4 import BeautifulSoup

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