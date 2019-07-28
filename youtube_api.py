import logging
from os.path import isdir, isfile, join as path_join
from os import makedirs
from httplib2 import ssl

from urllib.request import urlopen
from urllib.parse import quote
from bs4 import BeautifulSoup

from pafy import new as PAFY
import subprocess as sp

class YoutubeGAPI():
    """ Ghetto version of YoutubeAPI (web scraping instead of Google API calls) """
    log = logging.getLogger('YoutubeGAPI')
    def __init__(self, config=None):
        self.thumbnail_url = config.get('thumbnail_url', 'https://i.ytimg.com/vi/VIDEOID/default.jpg')
        self.search_url    = config.get('search_url', 'https://www.youtube.com/results?search_query=')
        self.verifySSL     = config.get('verifySSL', False)
        self.maxResults    = config.get('maxResults', 50)
        self.download_dir  = config.get('download_dir', 'downloads')
        self.FFMPEG_BIN    = config.get('ffmpeg_binary')
        if self.FFMPEG_BIN == '':
            self.FFMPEG_BIN = None
        self.SSLcontext    = None
        if self.verifySSL is False:    
            self.SSLcontext = ssl._create_unverified_context()
        self.log.debug("""YoutubeGAPI parameters:
            config['thumbnail_url'] = %s
            config['search_url'] = %s
            config['verifySSL'] = %s
            config['maxResults'] = %s
            config['download_dir'] = %s""" % (self.thumbnail_url,self.search_url,self.verifySSL,self.maxResults,self.download_dir) )
        self.validate_config()

    def search(self, input, maxResults=None, media_type='audio'):
        if maxResults is None:
            maxResults = self.maxResults
        SSLcontext = None;
        self.log.debug('search(%s, maxResults=%s, media_type=%s)' % (input,maxResults, media_type) )
        results = {}
        # results[VIDEOID]["title"]
        # results[VIDEOID]["published"]
        # results[VIDEOID]["description"]
        # results[VIDEOID]["img"]
        response = urlopen(self.search_url + quote(input), context=self.SSLcontext)
        html = response.read()
        soup = BeautifulSoup(html, 'html.parser')
        for vid in soup.findAll(attrs={'class':'yt-uix-tile-link'}):
            if not self._isAdUrl(vid['href']):
                id = vid['href'].replace('/watch?v=','')
                if len(id) > 15:
                    continue
                title = vid['title']
                thumbnail_url = self.thumbnail_url.replace('VIDEOID', id)
                results[id] = {}
                results[id]['title'] = title
                results[id]['img'] = thumbnail_url
                print(id, title, thumbnail_url)
        return results

    def _isAdUrl(self, url):
        adUrls = [
            'https://googleads.g.doubleclick.net/',
            'https://googleadservices.com/',
            'https://www.googleadservices.com/'
        ]
        for adUrl in adUrls:
            if url.startswith(adUrl):
                return True
        return False

    def download(self, id):
        url = 'https://www.youtube.com/watch?v=' + id
        video = PAFY(url)
        bestaudio = video.getbestaudio()
        title = bestaudio.title.replace(' ', '_')
        dlpath = self.get_dlpath(title)
        if dlpath == 'exists':
            return '{"status": "Download already exists"}'
        else:
            bestaudio.download(filepath=dlpath)
            result = self.convert_to_mp3(dlpath, title, bitrate=bestaudio.bitrate)
            return '{"status":"%s"}' % result
    
    def get_dlpath(self, title):
        dlpath = path_join(self.download_dir, title + '.mp3')
        if isfile(dlpath):
            return "exists"
        else:
            return dlpath

    def validate_config(self):
        if not isdir(self.download_dir):
            self.log.debug('Creating missing download directory: %s' % self.download_dir)
            try:
                makedirs(self.download_dir)
            except Exception as e:
                log.error('Error creating download directory (%s). ' % self.download_dir, e)
        else:
            self.log.debug('Download directory exists: %s' % self.download_dir)


#####################################################
    def convert_to_mp3(self, path, filename, bitrate='192k'):
        """
        Converts a input file to mp3
        command: ffmpeg -n -i input.m4a -acodec libmp3lame -ab 128k output.mp3
        """
        codec = "libmp3lame"
        mp3_filename = filename + ".mp3"
        command = [self.FFMPEG_BIN,
                   "-n",
                   "-i", path,
                   "-acodec", codec,
                   "-ab", bitrate,
                   mp3_filename
                   ]
        return self._convert(command)

    def _convert(self, command):
        """
        @param:
            command: command for conversion
        """
        try:
            proc = sp.Popen(command, stdout=sp.PIPE, bufsize=10**8)
            proc.wait()
            if proc.returncode:
                err = "\n".join(["Audio conversion: %s\n" % cmd,
                "WARNING: this command returned an error:",
                err.decode('utf8')])
                raise IOError(err)
                return err
            del proc
        except IOError as e:
            self.log.error('{0}'.format(e), exc_info=True)
            return '{0}'.format(e)

if __name__ == '__main__':
    from config import youtube_apikey
    yt = YoutubeGAPI(key=youtube_apikey)
    r = yt.search('python')
    print(r)
