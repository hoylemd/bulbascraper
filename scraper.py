import requests
from bs4 import BeautifulSoup


def scrape_page(url):
    print 'scraping [{}]'.format(url)
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    print soup.select('title')

BULBAPEDIA_EGG_GROUPS_URL = 'http://bulbapedia.bulbagarden.net/wiki/Egg_Group'

if __name__ == '__main__':
    scrape_page(BULBAPEDIA_EGG_GROUPS_URL)
