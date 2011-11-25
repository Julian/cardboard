import jinja2

from cardboard.db import Session
from cardboard.db.models import Set


TEMPLATE_DIR = "."


def write_coverage(cards):
    env = jinja2.Environment(loader=jinja2.FileSystemLoader(TEMPLATE_DIR))
    template = env.get_template("index.html")

    with open("card_coverage.html", "w") as cc_file:
        cc_file.write(template.render(cards=[
            {"name" : "Island"},
            {"name" : "Swamp"},
            {"name" : "Multani, Maro-Sorcerer"},
        ]))


def check_coverage(*sets):
    if not sets:
        s = Session()
        sets = s.query(Set)

    for set in sets:
        cover = u"".join(u"."  if c.name in cards else u"F" for c in set.cards)
        yield u"\n".join([set.name, u"=" * len(set.name), u"", cover, u"\n"])
