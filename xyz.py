from bs4 import BeautifulSoup
import arrow
import os
host_name = 'https://duta.in/news'

def temp():
    year = 2018
    month = 9
    file_path = '/home/duta/PycharmProjects/snippets/abc.xml'
    if not os.path.exists(file_path):
        content = """<?xml version="1.0" encoding="UTF-8"?>
                         <sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
                         <sitemap>
                         <loc>https://duta.in/sitemap.xml</loc>
                         </sitemap>
                         </sitemapindex>"""
    else:
        site_map_file = open(file_path, mode='r')
        content = site_map_file.read()
        site_map_file.close()

    soup = BeautifulSoup(content, 'xml')
    loc_tag = soup.new_tag('loc')
    loc_tag.string = host_name + '/' + str(year) + '/' + str(month) + '/' + 'sitemap-index.xml'
    lastmod_tag = soup.new_tag('lastmod')
    lastmod_tag.string = str(arrow.utcnow())
    sitemap_tag = soup.new_tag('sitemap')
    sitemap_tag.append(loc_tag)
    sitemap_tag.append(lastmod_tag)
    temp = soup.find_all('loc')
    for t in temp:
        if t.text.strip() == loc_tag.string:
            print("found dupe")
            return
    soup.sitemapindex.append(sitemap_tag)
    site_map_file = open(file_path, mode='w')
    site_map_file.write(soup.prettify())
    site_map_file.close()

if __name__ == '__main__':
    temp()