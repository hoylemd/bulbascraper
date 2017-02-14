from bs4.element import Tag


def slugify(name):
    return name.lower()


def is_link(obj):
    return isinstance(obj, Tag) and obj.name == 'a' and obj['href']
