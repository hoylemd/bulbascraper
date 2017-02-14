from egg_group import EggGroup


class DuplicateEggGroupException(BaseException):
    def __init__(self, egg_group):
        self.egg_group = egg_group

        self.message = (u"Egg group '{}' already instantiated."
                        .format(egg_group.name))

    def __unicode__(self):
        return self.message

    def __str__(self):
        return self.message


class Pokedex(object):
    def __init__(self, source=None):
        self.source = source

        if self.source is None:
            raise TypeError('Pokedex() expects a source kwarg')

        self.pokemon = {}
        self.egg_groups = {}

    def discover_egg_groups(self, links=None):
        returned_groups = {}

        if links is None:
            soup = self.source.get_egg_groups()
            links = soup.table.find_all('a')
            returned_groups = None  # means we'll return the whole set

        for link in links:
            egg_group = EggGroup(link)
            try:
                self.register_egg_group(egg_group)
                if returned_groups is not None:
                    returned_groups[egg_group.slug] = egg_group
            except DuplicateEggGroupException as sadness:
                print sadness

        return returned_groups if returned_groups is None else self.egg_groups

    def register_egg_group(self, egg_group):
        if egg_group.slug in self.egg_groups:
            raise DuplicateEggGroupException(egg_group)

        self.egg_groups[egg_group.slug] = egg_group
        egg_group.pokedex = self

    def parse_egg_groups(self, specifics=None):
        groups = specifics or self.egg_groups
        for group in groups:
            group = self.egg_groups[group]
            group.parse()
