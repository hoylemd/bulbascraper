from bulbapedia import Bulbapedia
from parsable import Parsable
from pokedex import Pokedex
from pokemon import Pokemon

bulbapedia = None

if __name__ == '__main__':
    bulbapedia = Bulbapedia()

    Parsable.source = bulbapedia

    pokedex = Pokedex(source=bulbapedia)
    Pokemon.pokedex = pokedex

    pokedex.get_egg_groups()
    pokedex.parse_egg_groups(specifics=['bug'])

    pokedex.egg_groups[u'bug'].parse_pokemon(specifics=['nincada', 'metapod'])
