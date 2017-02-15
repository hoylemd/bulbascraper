from parsable import Parsable


class Pokemon(Parsable):
    pokedex = None

    def __init__(self, name, path=None):
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
        self.egg_groups = None
        self.hatch_time_min = None
        self.hatch_time_max = None
        self.gender_ratio = None

    def parse_egg_groups(self, cell):
        if cell.span.string != u'Egg Group':
            raise Exception("Failed to parse Egg Group from {}'s page. "
                            "Expected u'Egg Group', received '{}'"
                            .format(self.name, cell.span.string))

        links = cell.table.find_all('a')

        # verify that the egg groups exist
        self.egg_groups = self.pokedex.discover_egg_groups(links)

        return self.egg_groups

    def parse_hatch_time(self, cell):
        pass

    def parse_breeding(self):
        cells = self.breeding_section.table.tr.find_all('td', recursive=False)
        egg_group_cell = cells[0]
        hatch_time_cell = cells[1]

        self.parse_egg_groups(egg_group_cell)
        self.parse_hatch_time(hatch_time_cell)

    def parse(self):
        soup = super(Pokemon, self).parse(complete=False)

        content = soup.find(id='mw-content-text')
        sidebar = content.find_all('table', recursive=False)[1]
        sections = sidebar.find_all('tr', recursive=False)

        self.header_section = sections[0]

        # pokemon with separate ability and type sections
        if len(sections) == 13:
            self.type_section = sections[1]
            self.ability_section = sections[2]
            offset_sections = sections[3:]
        # pokemon with combined ability and type sections
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

        self.parsed = True

    @property
    def egg_groups_string(self):
        return u', '.join(group.name for _, group in self.egg_groups.items())

    @property
    def breeding_summary(self):
        return u"{} ({})".format(self.name, self.egg_groups_string)
