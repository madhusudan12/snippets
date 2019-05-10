from bs4 import BeautifulSoup
import requests

web_url = r'https://www.mlb.com/scores/2019-05-12'
get_web = requests.get(web_url).text
soup = BeautifulSoup(get_web,"html.parser")
score = soup.find_all('div',class_='container')
print(score)
print(len(score))