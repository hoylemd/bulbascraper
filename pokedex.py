from utils import slugify

from egg_group import EggGroup


class Pokedex(object):
    def __init__(self, source=None):
        self.source = source

        if self.source is None:
            raise TypeError('Pokedex() expects a source kwarg')

        self.pokemon = {}
        self.egg_groups = {}

    def get_egg_groups(self):
        soup = self.source.get_egg_groups()

        egg_group_links = soup.select('table')[0].select('a')

        for link in egg_group_links:
            name = link.select('span')[0].string

            # TODO: remove this
            if not name == u'Bug':
                continue

            link = link.get('href')
            egg_group = EggGroup(name, link)
            self.register_egg_group(egg_group)

        return self.egg_groups

    def register_egg_group(self, egg_group):
        key = slugify(egg_group.name)
        self.egg_groups[key] = egg_group
        egg_group.pokedex = self
