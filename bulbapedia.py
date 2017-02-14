import requests
from bs4 import BeautifulSoup

BULBAPEDIA_DOMAIN = 'http://bulbapedia.bulbagarden.net'
BULBAPEDIA_EGG_GROUPS_PATH = '/wiki/Egg_Group'


class Bulbapedia(object):
    def __init__(self, domain=BULBAPEDIA_DOMAIN):
        self.domain = domain
        # IDEA: have a local cache of the pages
        self.pages = {}

    def get(self, path):

        if path[0] == u'/':
            path = self.domain + path

        if path in self.pages:
            print 'Bulbapedia retrieving from cache [{}]'.format(path)
            page = self.pages[path]
        else:
            print 'Bulbapedia scraping [{}]'.format(path)
            page = requests.get(path).content
            self.pages[path] = page

        return BeautifulSoup(page, 'html.parser')

    def get_egg_groups(self):
        return self.get(BULBAPEDIA_EGG_GROUPS_PATH)
