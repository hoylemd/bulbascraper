import requests
from bs4 import BeautifulSoup


BULBAPEDIA_DOMAIN = 'http://bulbapedia.bulbagarden.net'


class EggGroup(object):
    def __init__(self, name, path):
        self.name = name
        self.path = path

    def __str__(self):
        return "{}: {}".format(self.name, self.path)


def get_from_bulbapedia(path):
    print 'scraping [{}]'.format(path)
    return requests.get(BULBAPEDIA_DOMAIN + path).content


def get_egg_groups(url):
    egg_groups = {}

    page = get_from_bulbapedia(url)
    soup = BeautifulSoup(page, 'html.parser')

    egg_group_links = soup.select('table')[0].select('a')

    for link in egg_group_links:
        name = link.select('span')[0].string
        link = link.get('href')
        egg_group = EggGroup(name, link)
        egg_groups[name] = egg_group

    return egg_groups


BULBAPEDIA_EGG_GROUPS_URL = '/wiki/Egg_Group'

if __name__ == '__main__':
    egg_groups = get_egg_groups(BULBAPEDIA_EGG_GROUPS_URL)
    for egg_group in egg_groups:
        print egg_groups[egg_group]
