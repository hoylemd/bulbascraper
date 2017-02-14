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

        self._soup = None

    def parse(self):
        if self._soup is None:
            self._soup = get_from_bulbapedia(self.path)

        return self._soup

    def __unicode__(self):
        return u"{}: {}".format(self.name, self.path)


class Pokemon(Parsable):
    def __init__(self, name, path):
        super(Pokemon, self).__init__(name, path)

        self.header_section = None
        self.type_section = None
        self.ability_section = None
        self.gender_catch_section = None
        self.breeding_section = None
        self.physiology_section = None
        self.mega_section = None
        self.pokedex_section = None
        self.exp_section = None
        self.ev_yield_section = None
        self.appearance_section = None
        self.colour_and_friendship_section = None
        self.links_section = None

        # breeding info
        self.egg_groups = []
        self.hatch_time_min = 0
        self.hatch_time_max = 0

        self.gender_ratio = 0.5

    def parse_egg_groups(self, cell):
        if cell.span.string != u'Egg Group':
            raise Exception("failed to parse Egg Group from {}'s page. "
                            "Expected u'Egg Group', received '{}'"
                            .format(self.name, cell.span.string))

        links = cell.table.find_all('a')
        for link in links:
            name = link.string
            path = link['href']
            print u"{}: {}".format(name, path)

    def parse_hatch_time(self, cell):
        pass

    def parse_breeding(self):
        cells = self.breeding_section.table.tr.find_all('td', recursive=False)
        egg_group_cell = cells[0]
        hatch_time_cell = cells[1]

        self.parse_egg_groups(egg_group_cell)
        self.parse_hatch_time(hatch_time_cell)

    def parse(self):
        soup = super(Pokemon, self).parse()

        content = soup.find(id='mw-content-text')
        sidebar = content.find_all('table', recursive=False)[1]
        sections = sidebar.find_all('tr', recursive=False)

        self.header_section = sections[0]

        if len(sections) == 13:
            self.type_section = sections[1]
            self.ability_section = sections[2]
            offset_sections = sections[3:]
        else:
            cells = sections[1].find_all('td', recursive=False)
            self.type_section = cells[0]
            self.ability_section = cells[1]
            offset_sections = sections[2:]

        self.gender_catch_section = offset_sections[0]
        self.breeding_section = offset_sections[1]
        self.physiology_section = offset_sections[3]
        self.mega_section = offset_sections[3]
        self.pokedex_section = offset_sections[4]
        self.exp_section = offset_sections[5]
        self.ev_yield_section = offset_sections[6]
        self.appearance_section = offset_sections[7]
        self.colour_and_friendship_section = offset_sections[8]
        self.links_section = offset_sections[9]

        self.parse_breeding()


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
            path = link['href']
            pokemon = Pokemon(name, path)
            pokemon.egg_groups.append(self)
            self.pokemon[name] = pokemon

    def parse_pokemon(self):
        for mon in self.pokemon:
            pokemon = self.pokemon[mon]
            pokemon.parse()


def get_egg_groups(url):
    egg_groups = {}

    soup = get_from_bulbapedia(url)

    egg_group_links = soup.select('table')[0].select('a')

    for link in egg_group_links:
        name = link.select('span')[0].string

        # TODO: remove this
        if not name == u'Bug':
            continue

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

    egg_groups[u'Bug'].parse_pokemon()
