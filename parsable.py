from bs4.element import Tag


class Parsable(object):
    source = None

    def __init__(self, name_or_anchor, path=None):
        if isinstance(name_or_anchor, Tag) and name_or_anchor.name == 'a':
            name = name_or_anchor.string
            path = name_or_anchor['href']
        elif isinstance(name_or_anchor, basestring):
            name = name_or_anchor
        else:
            raise TypeError('Parsable expects a string or <a> tag. {} given'
                            .format(name_or_anchor))

        if path is None:
            raise TypeError('Parsable passed a name but no path.')

        self.name = name
        self.path = path

    def parse(self):
        if self.source is None:
            raise Exception('Parsable cannot parse without a source or soup!')

        return self.source.get(self.path)

    def __unicode__(self):
        return u"{}: {}".format(self.name, self.path)
