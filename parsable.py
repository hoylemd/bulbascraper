class Parsable(object):
    source = None

    def __init__(self, name, path):
        self.name = name
        self.path = path

    def parse(self):
        if self.source is None:
            raise Exception('Parsable cannot parse without a source or soup!')

        return self.source.get(self.path)

    def __unicode__(self):
        return u"{}: {}".format(self.name, self.path)
