class Type(object):
    def __init__(self, name):
        super(Type, self).__init__()
        self.name = str(name)

    def __eq__(self, other):
        if not isinstance(other, Type):
            return NotImplemented
        return self.name == other.name

    def __hash__(self):
        return hash(self.name)

    def __str__(self):
        return str(self.name)

    def __unicode__(self):
        return unicode(self.name)

    def __repr__(self):
        return "<Type: {.name}>".format(self)

    @property
    def is_permanent(self):
        return self in PERMANENTS

ARTIFACT = Type("Artifact")
CREATURE = Type("Creature")
ENCHANTMENT = Type("Enchantment")
LAND = Type("Land")
PLANESWALKER = Type("Planeswalker")

INSTANT = Type("Instant")
SORCERY = Type("Sorcery")

PERMANENTS = {ARTIFACT, CREATURE, ENCHANTMENT, LAND, PLANESWALKER}
NONPERMANENTS = {INSTANT, SORCERY}
TYPES = PERMANENTS | NONPERMANENTS
