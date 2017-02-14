from parsable import Parsable
from pokemon import Pokemon


class EggGroup(Parsable):
    def __init__(self, name, path=None):
        super(EggGroup, self).__init__(name, path)

        self.pokemon = {}

    def parse(self):
        soup = super(EggGroup, self).parse(complete=False)

        pokemon_tables = soup.select('table.roundy table')

        for pokemon_row in pokemon_tables[0].select('tr')[1:]:
            # TODO fix this
            link = pokemon_row.select('td:nth-of-type(3) a')[0]
            pokemon = Pokemon(link, egg_group=self)
            self.pokemon[pokemon.slug] = pokemon

        self.parsed = True

    def parse_pokemon(self, specifics=None):
        mons = specifics or self.pokemon
        for mon in mons:
            pokemon = self.pokemon[mon]
            pokemon.parse()
