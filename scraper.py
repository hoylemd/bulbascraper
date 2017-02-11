import requests
from BeautifulSoup import BeautifulSoup


def scrape_page(url):
    print 'scraping [{}]'.format(url)
    page = requests.get(url)
    soup = BeautifulSoup(page.content)
    print soup.prettify()

BULBAPEDIA_EGG_GROUPS_URL = 'http://bulbapedia.bulbagarden.net/wiki/Egg_Group'

if __name__ == '__main__':
    scrape_page(BULBAPEDIA_EGG_GROUPS_URL)
