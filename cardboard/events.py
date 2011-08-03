import itertools


class Event(object):
    def __init__(self, name):
        super(Event, self).__init__()
        self.name = str(name)

    def __repr__(self):
        return "<Event: {}>".format(self.name)

events = {e : Event(e) for e in [
                                 "game started",
                                 "game over",

                                 "life lost",
                                 "life gained",
                                 "player died",

                                 "phase changed",
                                 "turn changed",

                                 "card drawn",
                                 "card not drawn",
                                 "card discarded",
                                 "card not discarded",
                                 "library shuffled",

                                 "card entered play",
                                 "card left play",
                                 "card added to graveyard",
                                 "card removed from game",
                                 "card changed controller",
                                 "card tapped",
                                 "card untapped",

                                 "card morphed",
                                 "card cycled",

                                 "counter added",
                                 "counter removed",

                                 "mana added to pool",
                                 "mana left pool",

                                 "land played",

                                 "damage dealt",
                                 "damage received",

                                 ]}
