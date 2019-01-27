from __future__ import print_function
from bs4 import BeautifulSoup
from urllib import urlopen
from sample import leagues_urls, cups_urls, empty_urls



team_map={


}


def fetch_url(url):
    file = urlopen(url)
    soup = BeautifulSoup(file, 'html.parser')
    return soup


def get_data(url):
    print(url)
    soup = fetch_url(url)
    table1 = soup.find('table', {'class': 'Table2__table-fixed'})
    table2 = soup.find('table', {'class': 'Table2__table-scroll'})
    heading=soup.find('h1',{'class':'headline__h1'})
    title="".join(('*',heading.text,'*'))
    team_list = []
    table1_th = table1.find('thead')
    if table1_th is not None:
        team_list.append('Team')
    table1_tds = table1.find_all('td', {'class': 'Table2__td'})
    for td in table1_tds:
        team_name = td.find('abbr')
        if team_name is None:
            team_list.append(td.text)
        else:
            if team_name.text.strip() == '' or len(team_name.text.strip()) > 4:
                team=td.find('span',{'class':'hide-mobile'})
                abbr_name = team_map.get(team.text)
                if abbr_name is None:
                    team_list.append(team.text[:4])
                else:
                    team_list.append(abbr_name)
            else:
                team_list.append(team_name.text)
    row_number = 0
    table2_trs = table2.find_all('tr', {'class': 'Table2__tr'})
    out = []
    out.append(title)
    for tr in table2_trs:
        score_data = []
        tds = tr.find_all('td')
        if tds == []:
            tds = tr.find_all('th')
        for td in tds:
            score_data.append(td.text)
        out.append(u"{:>7}\t{:>2}\t{:>3}\t{:>2}".format(team_list[row_number],
                                                         score_data[0],
                                                         score_data[-2],
                                                         score_data[-1]))
        row_number = row_number + 1
    for row in out:
        print(row)
    return out





def test():
    # for url in cups_urls:
    #     get_data(cups_urls[url])
    # for url in leagues_urls:
    #     get_data(leagues_urls[url])
    url= 'http://www.espn.in/soccer/table/_/league/caf.champions'
    get_data(url)

test()

