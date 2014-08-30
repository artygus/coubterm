import os
import sys
import urllib2
import json

class CoubApi:
    HOT_URL = 'http://coub.com/api/v1/timeline/hot.json?page=1&per_page=15'
    NEWEST_URL = 'http://coub.com/api/v1/timeline/explore/newest.json?page=1&per_page=15'
    COUB_URL = 'http://coub.com/coubs/%s.json'
    
    def __prepare_data(self, coub):
        tpl = coub['file_versions']['web']['template']
        video_url = tpl.replace('%{version}', 'med').replace('%{type}', 'mp4')
        channel = coub['user'] if 'user' in coub else coub['channel']
        
        return {
            'permalink': coub['permalink'],
            'likes': coub['likes_count'],
            'views': coub['views_count'],
            'channel_permalink': self.__ellipsis(channel['permalink'], 16),
            'title': self.__ellipsis(coub['title'], 16),
            'video_url':  video_url
        }


    def __ellipsis(self, s, l):
        return s[:l-2] + (s[l-2:] and '..') 


    def get_hot(self):
        try:
            resp = urllib2.urlopen(self.HOT_URL)
            r_data = json.load(resp)
            p_data = []
        
            for c in r_data['coubs']:
                p_data.append(self.__prepare_data(c))
            
            return p_data
        except:
            print sys.exc_info()
            return False


    def get_newest(self):
        try:
            resp = urllib2.urlopen(self.NEWEST_URL)
            r_data = json.load(resp)
            # from StringIO import StringIO
            # with open(os.getenv('HOME') + '/Downloads/newest.json', 'r') as f: resp = f.read()
            # r_data = json.load(StringIO(resp))
            p_data = []
        
            for c in r_data['coubs']:
                p_data.append(self.__prepare_data(c))
            
            return p_data
        except:
            print sys.exc_info()
            return False
        
    
    def get_coub(self, permalink):
        try:
            resp = urllib2.urlopen(self.COUB_URL % permalink)
            r_data = json.load(resp)
            
            return self.__prepare_data(r_data)
        except:
            print sys.exc_info()
            return False
        