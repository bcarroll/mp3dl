from flask import jsonify
import requests
import json
import logging

from time import time

from os import mkdir
from os import stat
from os.path import abspath
from os.path import dirname
from os.path import join as path_join
from os.path import isfile
from os.path import isdir

from app import config

lists = {
    "TopSongs": "https://rss.itunes.apple.com/api/v1/us/apple-music/top-songs/all/200/explicit.json",
    "HeavyMetal": "https://rss.itunes.apple.com/api/v1/us/apple-music/hot-tracks/heavy-metal/100/explicit.json",
    "Country": "https://rss.itunes.apple.com/api/v1/us/apple-music/hot-tracks/country/100/explicit.json",
}


def getSongList(list='TopSongs'):
    if list in lists.keys():
        return getFeed(list, lists[list])
    else:
        return jsonify('No feed is configured for %s' % list)

def getFeed(name, url):
    feed_threshold = 60*24 # minutes before feed is considered old (default: 24 hours)
    feedDir = path_join(config['download_dir'], '..', 'app', 'feeds')
    feedFile = path_join(feedDir, name)
    if not isdir(feedDir):
        mkdir(feedDir)
    if not isfile(feedFile):
        downloadFeed(name, url, feedFile)
    feed_mod_time = stat(feedFile).st_mtime
    
    # Time in minutes since last modification of file
    last_time = (time() - (time() - (feed_threshold * 60)) ) / 60
    if (last_time < feed_mod_time):
        print("%s feed is old... updating" % name)
    else:
        print("%s feed does not need updating" % name)

def downloadFeed(name, url, feedFile):
    print('Downloading %s feed from %s' % (name,url))
    print('Feed location: %s' % feedFile)

if __name__ == '__main__':
    songList = getSongList()
    print(songList)
    