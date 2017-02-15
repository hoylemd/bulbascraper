from utils import is_link
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

    def discover_egg_group(self, clue):
        """
            Clue can be an <a> tag, slug, or instance
            returns EggGroup object or None if it can't be found
        """
        if is_link(clue):
            egg_group = EggGroup(clue)
        elif isinstance(clue, EggGroup):
            egg_group = clue
        elif isinstance(clue, basestring):
            egg_group = self.egg_groups[clue]
        else:
            raise TypeError('invalid clue passed to `discover_egg_group`: '
                            '{}'.format(clue))

        if egg_group.slug not in self.egg_groups:
            self.egg_groups[egg_group.slug] = egg_group

        return self.egg_groups[egg_group.slug]

    def discover_egg_groups(self, clues=None):
        returned_groups = {}

        if clues is None:
            soup = self.source.get_egg_groups()
            clues = soup.table.find_all('a')

        for clue in clues:
            group = self.discover_egg_group(clue)
            returned_groups[group.slug] = group

        return returned_groups

    def parse_egg_groups(self, specifics=None):
        groups = specifics or self.egg_groups
        for group in groups:
            group = self.egg_groups[group]
            group.parse()
