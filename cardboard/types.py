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
        return self.name

    def __repr__(self):
        return "<Type: {.name}>".format(self)

    @property
    def is_permanent(self):
        return self in PERMANENTS

artifact = Type("Artifact")
creature = Type("Creature")
enchantment = Type("Enchantment")
land = Type("Land")
planeswalker = Type("Planeswalker")

instant = Type("Instant")
sorcery = Type("Sorcery")

PERMANENTS = {artifact, creature, enchantment, land, planeswalker}
NONPERMANENTS = {instant, sorcery}
TYPES = PERMANENTS | NONPERMANENTS
