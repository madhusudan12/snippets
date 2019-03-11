# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import requests


data = requests.get('https://duta.in/news/2017/8/sitemap-index.xml')

soup = BeautifulSoup(data.text, 'xml')
p=soup.find_all('sitemap')
for t in p:
    print(t)
