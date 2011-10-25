# -*- coding: utf-8 -*-
MANA_COSTS = dict(zip(
    (str(c) for c in range(20)),
    [unichr(0x24EA)] + [unichr(i) for i in range(0x2460, 0x2474)]
))
MANA_COSTS.update(W=u"Ⓦ", U=u"Ⓤ", B=u"Ⓑ", R=u"Ⓡ", G=u"Ⓖ")


def type_line(card):
    types = " ".join(sorted(card.types))

    if card.subtypes:
        subtypes = u", ".join(card.subtypes)
        return u"{} — {}".format(types, subtypes)
    else:
        return types


def unicost(mana_cost):
    for c in mana_cost:
        yield MANA_COSTS.get(c, c)
