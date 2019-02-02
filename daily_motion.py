from bs4 import BeautifulSoup
from logging import getLogger
import requests


session = requests.Session()
log = getLogger(__name__)

def fetch_url(url):
    req = session.get(url)
    log.info("Fetching %s", url)
    if req.status_code != 200:
        raise Exception("Unable to download: {}: status_code: {}".format(url, req.status_code))
    soup = BeautifulSoup(req.text, "html.parser")
    return soup


def get_data(url):
    soup = fetch_url(url)
    print(soup)
    pass




if __name__ == '__main__':
    url = ''
    get_data()