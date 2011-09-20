# -*- coding: utf-8 -*-
MANA_COSTS = dict(zip(
    (str(c) for c in range(20)),
    [unichr(0x24EA)] + [unichr(i) for i in range(0x2460, 0x2474)]
))
MANA_COSTS.update(W=u"Ⓦ", U=u"Ⓤ", B=u"Ⓑ", R=u"Ⓡ", G=u"Ⓖ")


def convert_ability_costs(abilities):
    pass


def type_line(card):
    if card.subtypes:
        subtypes = u", ".join(card.subtypes)
        return u"{.type} — {}".format(card, subtypes)
    else:
        return card.type


def unicost(mana_cost):
    for c in mana_cost:
        yield MANA_COSTS.get(c, c)
