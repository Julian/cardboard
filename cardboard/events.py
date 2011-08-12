from collections import OrderedDict
from itertools import chain


__all__ = ["Event", "events", "phases"]


class Event(object):
    """
    An event container.

    To create ordered sections of an event tree, passing in an OrderedDict is
    supported.

        >>> from collections import OrderedDict
        >>> o = OrderedDict([("foo", {}), ("bar", {})])
        >>> e = Event("Foo", subevents=o)
        This

        >>> list(e)
        [<Event: Foo.foo>, <Event: Foo.bar>]

    """

    def __init__(self, name="", subevents=None, _parent=None, **kwsubevents):
        super(Event, self).__init__()

        if subevents is None:
            subevents = {}

        if _parent is not None:
            _parent = "{.fully_qualified_name}['{}']".format(_parent, name)

        self.fully_qualified_name = _parent or name

        self._subevents = subevents.__class__()

        for k, v in chain(subevents.iteritems(), kwsubevents.iteritems()):
            self[k] = v

    def __contains__(self, event):
        return event in self._subevents.viewvalues()

    def __eq__(self, other):
        return (isinstance(other, Event) and self.name == other.name and
                self._subevents == other._subevents)

    def __getitem__(self, k):
        return self._subevents[k]

    def __setitem__(self, k, v):
        self._subevents[k] = Event(k, v, _parent=self)

    def __iter__(self):
        return iter(self._subevents.viewvalues())

    def __len__(self):
        return len(self._subevents)

    def __str__(self):
        return self.name

    def __repr__(self):
        return "<Event: {.fully_qualified_name}>".format(self)

    @property
    def name(self):
        return self.fully_qualified_name.rstrip("']").rpartition("['")[2]

    @property
    def subevent_names(self):
        return self._subevents.viewkeys()

    def get(self, k):
        return self._subevents.get(k)


phases = OrderedDict([

                      ("beginning", OrderedDict([
                                                 ("untap", {}),
                                                 ("draw", {}),
                                                 ("upkeep", {}),
                                                 ])),

                      ("first_main", {}),

                      ("combat", OrderedDict([
                                              ("beginning", {}),
                                              ("declare_attackers", {}),
                                              ("declare_blockers", {}),
                                              ("combat_damage", {}),
                                              ("end", {}),
                                             ])),

                      ("second_main", {}),

                      ("ending", OrderedDict([
                                              ("end", {}),
                                              ("cleanup", {}),
                                             ])),
                     ])


events = Event("all",

               {"card" : {
                          "cast" : {},
                          "countered" : {},
                          "tapped" : {},
                          "untapped" : {},

                          "zones" : {

                                     "exile" : {
                                                 "entered" : {},
                                                 "left" : {},
                                                 },

                                     "battlefield" : {
                                                     "entered" : {},
                                                     "left" : {},
                                                 },

                                     "graveyard" : {
                                                     "entered" : {},
                                                     "left" : {},
                                                     },

                                     "hand" : {
                                                 "entered" : {},
                                                 "left" : {},
                                             },

                                     "library" : {
                                                 "entered" : {},
                                                 "left" : {},
                                                 },
                                    }
                         },

                "game" : {
                          "started" : {},
                          "ended" : {},
                          "phases" : phases,

                          "turn" : {
                                    "changed" : {},
                                   },

                         },

                "player" : {
                            "died" : {},
                            "draw" : {},

                            "life" : {
                                      "gained" : {},
                                      "lost" : {},
                                     },

                            "mana" : {
                                      "black" : {
                                                 "added" : {},
                                                 "removed" : {},
                                                },

                                      "green" : {
                                                 "added" : {},
                                                 "removed" : {},
                                                },

                                      "red" : {
                                               "added" : {},
                                               "removed" : {},
                                              },

                                      "blue" : {
                                                "added" : {},
                                                "removed" : {},
                                               },

                                      "white" : {
                                                 "added" : {},
                                                 "removed" : {},
                                                },

                                      "colorless" : {
                                                     "added" : {},
                                                     "removed" : {},
                                                    },
                                     },

                           },
               })
