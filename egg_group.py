from parsable import Parsable
from pokemon import Pokemon


class EggGroup(Parsable):
    def __init__(self, name, path=None):
        super(EggGroup, self).__init__(name, path)

        self.pokemon = {}

    def parse(self):
        soup = super(EggGroup, self).parse(complete=False)

        content = soup.find(id='mw-content-text')
        pokemon_tables = content.find_all('table', recursive=False)[1:3]

        just_this_group = pokemon_tables[0]
        this_and_other_group = pokemon_tables[1]

        rows = just_this_group.table.find_all('tr')[1:]  # skip heading row
        rows += this_and_other_group.table.find_all('tr')[1:]
        for pokemon_row in rows:
            link = pokemon_row.find_all('td', recursive=False)[2].a
            pokemon = Pokemon(link, egg_group=self)
            self.pokemon[pokemon.slug] = pokemon

        self.parsed = True

    def parse_pokemon(self, specifics=None):
        mons = specifics or self.pokemon
        for mon in mons:
            pokemon = self.pokemon[mon]
            pokemon.parse()
