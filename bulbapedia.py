import os

import requests

from bs4 import BeautifulSoup

from utils import slugify

BULBAPEDIA_DOMAIN = 'http://bulbapedia.bulbagarden.net'
BULBAPEDIA_EGG_GROUPS_PATH = '/wiki/Egg_Group'

CACHE_PATH = '.bulba.cache'

class Bulbapedia(object):
    def __init__(self, domain=BULBAPEDIA_DOMAIN):
        self.domain = domain

        if not os.path.exists(CACHE_PATH):
            os.makedirs(CACHE_PATH)

        self.pages = {}

    def get(self, path):
        if path[0] == u'/':
            url = self.domain + path
        else:
            url = path

        # check the cache files
        cache_key = './' + CACHE_PATH + '/' + slugify(path)

        if os.path.isfile(cache_key):
            print 'Bulbapedia retrieving from cache [{}]'.format(path)
            with open(cache_key) as cached_page:
                page = cached_page.read()
        else:
            print 'Bulbapedia scraping [{}]'.format(path)
            page = requests.get(url).content
            self.pages[path] = page

            print 'Cacheing it under {}'.format(cache_key)
            with open(cache_key, 'w') as cached_page:
                cached_page.write(page)

        return BeautifulSoup(page, 'html.parser')

    def get_egg_groups(self):
        return self.get(BULBAPEDIA_EGG_GROUPS_PATH)
