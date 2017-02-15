from slugify import slugify as _slugify
from bs4.element import Tag


def slugify(name):
    return _slugify(unicode(name))


def is_link(obj):
    return isinstance(obj, Tag) and obj.name == 'a' and obj['href']
