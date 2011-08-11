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
            _parent = ".".join([_parent.fully_qualified_name, name])

        self.fully_qualified_name = _parent or name

        all_events = chain(subevents.iteritems(), kwsubevents.iteritems())
        events = ((k, Event(k, v, _parent=self)) for k, v in all_events)
        self._subevents = subevents.__class__(events)

    def __contains__(self, event):
        return event in self._subevents.viewvalues()

    def __getattr__(self, attr):
        try:
            return self._subevents[attr]
        except KeyError:
            return object.__getattribute__(self, attr)

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
        return self.fully_qualified_name.rpartition(".")[2]

    @property
    def subevent_names(self):
        return self._subevents.viewkeys()


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
