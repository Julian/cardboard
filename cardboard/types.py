ARTIFACT = u"Artifact"
CREATURE = u"Creature"
ENCHANTMENT = u"Enchantment"
LAND = u"Land"
PLANESWALKER = u"Planeswalker"

INSTANT = u"Instant"
SORCERY = u"Sorcery"

PERMANENTS = frozenset({ARTIFACT, CREATURE, ENCHANTMENT, LAND, PLANESWALKER})
NONPERMANENTS = frozenset({INSTANT, SORCERY})
TYPES = PERMANENTS | NONPERMANENTS

SUPERTYPES = frozenset({"Basic", "Legendary", "Ongoing", "Snow", "World"})


def is_permanent(type):
    return type in PERMANENTS
