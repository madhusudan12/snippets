from __future__ import unicode_literals
import youtube_dl
from bs4 import BeautifulSoup
import requests


# url='https://twitter.com/i/status/1078938674727796736'
# data=requests.get(url)
#
# soup=BeautifulSoup(data.text,'html.parser')
# print(soup.prettify())


def download_video():
    ydl_opts = {}
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download(['https://video.twimg.com/amplify_video/1013908058899005440/pl/5wNSjKYuhZLWkd15.m3u8?tag=3'])

#download_video()



def google_search(string):
    result=requests.get('https://www.google.com/search?q='+string+'&oq='+string)
    soup=BeautifulSoup(result.text,'html.parser')
    print(soup.prettify())
    pass

google_search('MadhusudanChowdary')


