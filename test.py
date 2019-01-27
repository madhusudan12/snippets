from __future__ import print_function
from bs4 import BeautifulSoup
from urllib import urlopen
from sample import leagues_urls,cups_urls,empty_urls
import sys


def fetch_url(url):
    file = urlopen(url)
    soup = BeautifulSoup(file,'html.parser')
    return soup


def get_data(url):
    print(url)
    soup = fetch_url(url)
    table1=soup.find('table',{'class':'Table2__table-fixed'})
    table2=soup.find('table',{'class':'Table2__table-scroll'})
    team_list=[]
    table1_th = table1.find('thead')
    if table1_th != None:
        team_list.append(table1_th.text)
    table1_tds=table1.find_all('td',{'class':'Table2__td'})
    for td in table1_tds:
        temp=td.find('abbr')
        if temp == None:
            team_list.append(td.text)
        else:
            #team=td.find('span',{'class':'hide-mobile'})
            #team_list.append(team.text)
            team_list.append(temp.text)
    row_number=0
    table2_trs=table2.find_all('tr',{'class':'Table2__tr'})
    out=[]
    for tr in table2_trs:
        score_data=[]
        tds=tr.find_all('td')
        if tds==[]:
            tds=tr.find_all('th')
        for td in tds:
            score_data.append(td.text)
        out.append(u"{:<12}\t{:>4}\t{:>4}\t{:>4}".format(team_list[row_number],
                                                         score_data[0],
                                                         score_data[-2],
                                                         score_data[-1]))
        row_number+=1

    for row in out:
        print(row)
    pass

for url in cups_urls:
    get_data(cups_urls[url])

for url in leagues_urls:
    get_data(leagues_urls[url])