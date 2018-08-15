#!/usr/bin/env python
# coding: utf-8
import sys

from collections import Counter

# TODO - use clilyrics.classname?
from fetcher_genius import GeniusFetcher
from fetcher_azlyrics import AZLyricsFetcher


def create_fetcher(type):
    """ returns a fetcher (e.g. via RapGenius, AZLyric, etc.) capable of retrieving lyrics and
    sanitizing them."""
    if type == "Genius":
        return GeniusFetcher()
    if type == "AZLyrics":
        return AZLyricsFetcher()
    raise ValueError('Unrecognized fetcher type provided: ' + type)


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

