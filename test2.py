# -*- coding: utf-8 -*-
from __future__ import print_function
from bs4 import BeautifulSoup
from urllib import urlopen
from sample import leagues_urls,cups_urls,empty_urls

def fetch_url(url):
    file = urlopen(url)
    soup = BeautifulSoup(file,'html.parser')
    return soup


def get_data(url):
    print(url)
    soup = fetch_url(url)
    league_name=soup.find('h1', {'class':'headline__h1 dib'})
    print(league_name.text)


for url in leagues_urls:
    get_data(leagues_urls[url])