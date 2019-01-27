from __future__ import print_function
from bs4 import BeautifulSoup
from urllib import urlopen
import requests
from json import load
import arrow
import urlparse

SOFASCORE_URL = "http://www.sofascore.com"

base_url = "https://www.sofascore.com"


def get_leauge_data():
    json_url = "https://www.sofascore.com/event/count/by-categories/football//json?timezone=5&_=154529362"

    data = requests.get(json_url)
    leauge_data = data.json()
    return leauge_data


def get_leauge_countries():
    url = "https://www.sofascore.com/esi/categories/football?_=154529362"

    web_source = requests.get(url)
    soup = BeautifulSoup(web_source.text, "html.parser")
    country_list = soup.find_all('li')
    data = dict()
    for li in country_list:
        data_id = int(li.a['data-id'])
        data[data_id] = {'name': li.a.text.strip()}
        data[data_id]['link'] = li.a['href']
    return data


def get_individual_leauges_info(data):
    individual_leagues = []
    for leauge in data:
        if 'live' in data[leauge]:
            url = base_url + data[leauge]['link'] + '/' + str(arrow.utcnow().format('YYYY-MM-DD')) + '/json'
            web_source = urlopen(url)
            d = load(web_source)
            individual_leagues.append(d)
    return individual_leagues


def get_data():
    data = get_leauge_countries()
    leauges = get_leauge_data()
    for leauge in leauges:
        data[int(leauge)]['all'] = leauges[leauge]['all']
        data[int(leauge)]['live'] = leauges[leauge]['live']
    all_leagues_data = get_individual_leauges_info(data)
    return all_leagues_data


d = get_data()
for i in d:
    tn = i['sportItem']['tournaments']
    for t in tn:
        for m in t['events']:
            print(arrow.get(m['startTimestamp']).format('YYYY-MM-DD'))

print(arrow.utcnow().format('YYYY-MM-DD'))

# def fetch_url(url):
#     req = session.get(url)
#     log.info("Fetching %s", url)
#     if req.status_code != 200:
#         raise Exception("Unable to download: {}: status_code: {}".format(url, req.status_code))
#     soup = BeautifulSoup(req.text, "html.parser")
#     return soup



# def get_table_data():
#     url = "http://www.espn.in/soccer/table/_/league/eng.2"
#     data = requests.get(url)
#     soup = BeautifulSoup(data.text, 'html.parser')
#     soup_data = soup.prettify()
#     data = soup.findChildren('table',
#                              class_="Table2__right-aligned Table2__table-fixed Table2__Table--fixed--left Table2__table")
#     columns = soup.find_all('td', class_='v-top')
#     # print(columns[0].prettify())
#     table_data=[]
#     country_list=columns[0].find_all('span',class_='hide-mobile')
#     for country in country_list:
#         table_data.append([str(country.text)])
#
#     odd_rows_list=columns[1].find_all('tr',class_='filled Table2__tr Table2__tr--sm Table2__even')
#     even_rows_list=columns[1].find_all('tr',class_='Table2__tr Table2__tr--sm Table2__even')
#     row_number=0
#     for list in even_rows_list:
#         values=list.find_all('td',class_='Table2__td')
#         values_list=[]
#         for val in values:
#             values_list.append(int(val.text))
#         table_data[row_number].append(values_list)
#
#
#
# get_table_data()
#


#
# def fetch_url(url):
#     req = session.get(url)
#     log.info("Fetching %s", url)
#     if req.status_code != 200:
#         raise Exception("Unable to download: {}: status_code: {}".format(url, req.status_code))
#     soup = BeautifulSoup(req.text, "html.parser")
#     return soup
#


# def get_table_data():
#     url = "http://www.espn.in/soccer/table/_/league/eng.2"
#     data = requests.get(url)
#     soup = BeautifulSoup(data.text, 'html.parser')
#     soup_data = soup.prettify()
#     data = soup.findChildren('table',
#                              class_="Table2__right-aligned Table2__table-fixed Table2__Table--fixed--left Table2__table")
#     columns = soup.find_all('td', class_='v-top')
#     # print(columns[0].prettify())
#     table_data=[]
#     country_list=columns[0].find_all('span',class_='hide-mobile')
#     for country in country_list:
#         table_data.append([str(country.text)])
#
#     odd_rows_list=columns[1].find_all('tr',class_='filled Table2__tr Table2__tr--sm Table2__even')
#     even_rows_list=columns[1].find_all('tr',class_='Table2__tr Table2__tr--sm Table2__even')
#     row_number=0
#     for li in even_rows_list:
#         values=li.find_all('td',class_='Table2__td')
#         values_list=[]
#         for val in values:
#             values_list.append(str(val.text))
#         table_data[row_number].append(values_list[0])
#         table_data[row_number].append(values_list[-2])
#         table_data[row_number].append(values_list[-1])
#         row_number+=2
#     row_number=1
#     for li in odd_rows_list:
#         values_=li.find_all('td',class_='Table2_td')
#         values_list=[]
#         for val in values:
#             values_list.append(str(val.text))
#         table_data[row_number].append(values_list[0])
#         table_data[row_number].append(values_list[-2])
#         table_data[row_number].append(values_list[-1])
#         row_number+=2
#     for row in table_data:
#         print(row)
#
#
#
# get_table_data()


# d=dict()
# d[10]={'name':'india'}
# d[20]={'name':'england'}
# d[10]['all']=2
# d[20]['live']=3
