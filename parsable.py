from utils import slugify, is_link


class Parsable(object):
    source = None

    def __init__(self, name_or_anchor, path=None):
        if is_link(name_or_anchor):
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

        self.slug = slugify(name)

        self.parsed = False

    def parse(self, complete=True):
        if self.source is None:
            raise Exception('Parsable cannot parse without a source!')

        if complete:
            self.parsed = True

        return self.source.get(self.path)

    def __unicode__(self):
        return u"{}: {}".format(self.name, self.path)
