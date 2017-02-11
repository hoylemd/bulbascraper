import requests
from bs4 import BeautifulSoup

egg_groups = {}

BULBAPEDIA_DOMAIN = 'http://bulbapedia.bulbagarden.net'


class EggGroup(object):
    def __init__(self, name, path):
        self.name = name
        self.path = path

    def __str__(self):
        return "{}: {}".format(self.name, self.path)


def get_from_bulbapedia(path):
    return requests.get(BULBAPEDIA_DOMAIN + path).content


def scrape_page(url):
    print 'scraping [{}]'.format(url)
    page = get_from_bulbapedia(url)
    soup = BeautifulSoup(page, 'html.parser')
    print soup.select('title')

    egg_group_links = soup.select('table')[0].select('a')

    for link in egg_group_links:
        name = link.select('span')[0].string
        link = link.get('href')
        egg_group = EggGroup(name, link)
        egg_groups[name] = egg_group
        print egg_group


BULBAPEDIA_EGG_GROUPS_URL = '/wiki/Egg_Group'

if __name__ == '__main__':
    scrape_page(BULBAPEDIA_EGG_GROUPS_URL)
