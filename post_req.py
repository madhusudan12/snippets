import requests
from bs4 import BeautifulSoup

def main():
    url = 'https://duta.in/news/sitemap-index.xml'
    content = requests.get(url)
    soup = BeautifulSoup(content.text, 'xml')
    sitemap_indexs = soup.find_all('loc')
    for loc in sitemap_indexs[1:]:
        cont = requests.get(loc.text.strip())
        soup_temp = BeautifulSoup(cont.text, 'xml')
        sitemaps = soup_temp.find_all('sitemap')
        for sitemap in sitemaps:
            print(sitemap.prettify())




main()