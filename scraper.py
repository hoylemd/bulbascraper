from bulbapedia import Bulbapedia
from parsable import Parsable
from pokedex import Pokedex

bulbapedia = None

if __name__ == '__main__':
    bulbapedia = Bulbapedia()

    Parsable.source = bulbapedia

    pokedex = Pokedex(source=bulbapedia)

    egg_groups = pokedex.get_egg_groups()
    for name in egg_groups:
        group = egg_groups[name]
        group.parse()

    egg_groups[u'bug'].parse_pokemon()
