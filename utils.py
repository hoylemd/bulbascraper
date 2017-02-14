import requests
from bs4 import BeautifulSoup


def slugify(name):
    return name.lower()


class Bulbapedia(object):
    def __init__(self, domain):
        self.domain = domain
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
