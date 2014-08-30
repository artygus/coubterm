#!/usr/bin/env python 

import os
import readline
import sys
from collections import OrderedDict

import api
from completer import Completer

VERSION = 0, 0, 1

API = api.CoubApi()
COUBS = OrderedDict()

__permalinks = []
__autocomplete_dict = {
    "play": __permalinks,
    "get": {
        "coub": __permalinks,
        "hot": None,
        "newest": None
    },
    "next": None,
    "quit": None
}
__last_played = None


def __mplay(url):
    os.system('mplayer -vo caca -quiet -cache 8192 -prefer-ipv4 -msglevel all=1 -loop 0 -fixed-vo %s' % url)


def __play(permalink):
    global __last_played
    print 'playing %s' % COUBS[permalink]['video_url']
    __last_played = permalink
    __mplay(COUBS[permalink]['video_url'])


def __push_coub(coub):
    COUBS[coub['permalink']] = coub
    __permalinks.append(coub['permalink'])


def __print_coubs_data(coubs):
    headers = ["Permalink", "Title", "Channel", "Views", "Likes"]
    row_width = 16
    row_format = u" {:>%i} |" % row_width * (len(headers) + 1)

    print row_format.format("", *headers)
    print " " * (row_width + 2) + "|" + ("-" * (row_width + 2) + "|") * len(headers)

    for row in coubs:
        print row_format.format("", *[row['permalink'], row['title'], row['channel_permalink'], row['views'], row['likes']])


def play(permalink):
    if permalink in COUBS:
        __play(permalink)
    else:
        print 'getting coub..'
        c = API.get_coub(permalink)
    
        if not c:
            print 'failed to get coub %s' % permalink
        else:
            __push_coub(c)
            __play(c['permalink'])


def get_hot():
    print 'getting hot..'
    hot = API.get_hot()

    if not hot:
        print 'failed to get hot coubs'
    else:
        [__push_coub(c) for c in hot]
        __print_coubs_data(hot)


def get_newest():
    print 'getting newest..'
    newest = API.get_newest()

    if not newest:
        print 'failed to get newest coubs'
    else:
        [__push_coub(c) for c in newest]
        __print_coubs_data(newest)


def play_next():
    if __last_played:
        keys = COUBS.keys()
        i = keys.index(__last_played)
        if i < len(COUBS) - 1:
            play(COUBS[keys[i + 1]]['permalink'])
        else:
            play(COUBS[keys[0]]['permalink'])
    elif len(COUBS) > 0:
        play(COUBS.itervalues().next()['permalink'])
    else:
        print 'nothing to play, get some coubs using get command'


if __name__ == '__main__':
    readline.set_completer(Completer(__autocomplete_dict).complete)
    if sys.platform == 'darwin':
        readline.parse_and_bind('bind ^I rl_complete')
    else:
        readline.parse_and_bind('tab: complete')
        
    print """
Howdy!
Start with \"get newest\" command and \"play\" some something, e.g. \"play 2vf1v\". To quit player screen press \"q\".
Btw, autocomplete activated.
"""

    while True:
        x = raw_input('> ')
    
        if x.startswith('get hot'):
            get_hot()
        elif x.startswith('get newest'):
            get_newest()
        elif x.startswith('next'):
            play_next()
        elif x.startswith('get coub ') or x.startswith('play '):
            play(x.split()[-1])
        elif x == 'q' or x == 'quit':
            exit()
        else:
            print 'command is not recognized, try again'
