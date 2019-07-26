from apiclient.discovery import build #pip install google-api-python-client
from apiclient.errors import HttpError #pip install google-api-python-client
from oauth2client.tools import argparser #pip install oauth2client
from httplib2 import Http
from html import unescape
from datetime import datetime

class YoutubeAPI():
    def __init__(self, key=None, service='youtube', version='v3', verifySSL=False):
        self.key     = key # DEVELOPER_KEY = "REPLACE_ME"
        self.service = service # YOUTUBE_API_SERVICE_NAME = "youtube"
        self.version = version # YOUTUBE_API_VERSION = "v3"
        self.http    = Http(disable_ssl_certificate_validation=not verifySSL)
        self.api     = build(self.service, self.version, http=self.http, developerKey=self.key)

    def search(self, input, maxResults=50, media_type='audio'):
        results = {}
        search_results = self.api.search().list(q=input, type=media_type, part='id,snippet', maxResults=maxResults).execute()
        for result in search_results.get('items', []):
            if result['id']['kind'] == 'youtube#video':
                results[result['id']['videoId']] = {}
                results[result['id']['videoId']]['title'] = unescape(result['snippet']['title'])
                publishedAt = datetime.strptime(result['snippet']['publishedAt'], '%Y-%m-%dT%H:%M:%S.%fZ')
                results[result['id']['videoId']]['published'] = datetime.strftime(publishedAt, '%D')
                results[result['id']['videoId']]['description'] = unescape(result['snippet']['description'])
                results[result['id']['videoId']]['img'] = {}
                results[result['id']['videoId']]['img']['url'] = result['snippet']['thumbnails']['default']['url']
                results[result['id']['videoId']]['img']['width'] = result['snippet']['thumbnails']['default']['width']
                results[result['id']['videoId']]['img']['height'] = result['snippet']['thumbnails']['default']['height']
        return results

if __name__ == '__main__':
    from config import youtube_apikey
    yt = YoutubeAPI(key=youtube_apikey)
    r = yt.search('python')
    print(r)
