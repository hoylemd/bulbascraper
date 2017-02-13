import requests
from bs4 import BeautifulSoup

BULBAPEDIA_DOMAIN = 'http://bulbapedia.bulbagarden.net'


def get_from_bulbapedia(path):
    print 'scraping [{}]'.format(path)
    page = requests.get(BULBAPEDIA_DOMAIN + path).content
    return BeautifulSoup(page, 'html.parser')


class Parsable(object):
    def __init__(self, name, path):
        self.name = name
        self.path = path

    def parse(self):
        return get_from_bulbapedia(self.path)

    def __unicode__(self):
        return u"{}: {}".format(self.name, self.path)


class Pokemon(Parsable):
    def __init__(self, name, path):
        super(Pokemon, self).__init__(name, path)

        self.egg_groups = []
        self.gender_ratio = 0.5
        self.hatch_time_min = 0
        self.hatch_time_max = 0


class EggGroup(Parsable):
    def __init__(self, name, path):
        super(EggGroup, self).__init__(name, path)

        self.pokemon = {}

    def parse(self):
        soup = super(EggGroup, self).parse()

        pokemon_tables = soup.select('table.roundy table')

        for pokemon_row in pokemon_tables[0].select('tr')[1:]:
            link = pokemon_row.select('td:nth-of-type(3) a')[0]
            name = link.string
            path = link.get('href')
            pokemon = Pokemon(name, path)
            pokemon.egg_groups.append(self)
            self.pokemon[name] = pokemon
            print u"{}".format(pokemon)


def get_egg_groups(url):
    egg_groups = {}

    soup = get_from_bulbapedia(url)

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
    for name in egg_groups:
        group = egg_groups[name]
        group.parse()
