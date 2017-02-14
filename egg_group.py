from utils import slugify

from parsable import Parsable
from pokemon import Pokemon


class EggGroup(Parsable):
    def __init__(self, name, path=None):
        super(EggGroup, self).__init__(name, path)

        self.pokedex = None

        self.pokemon = {}

    def parse(self):
        soup = super(EggGroup, self).parse()

        pokemon_tables = soup.select('table.roundy table')

        for pokemon_row in pokemon_tables[0].select('tr')[1:]:
            link = pokemon_row.select('td:nth-of-type(3) a')[0]
            pokemon = Pokemon(link)
            pokemon.egg_groups.append(self)
            self.pokemon[slugify(pokemon.name)] = pokemon

    def parse_pokemon(self, specifics=None):
        mons = specifics or self.pokemon
        for mon in mons:
            pokemon = self.pokemon[mon]
            pokemon.parse()
