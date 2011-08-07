from collections import OrderedDict
import itertools


__all__ = ["Event", "events", "phases"]


class Event(object):
    """
    An event container.

    To create ordered sections of the event tree, passing in an OrderedDict is
    supported.

        >>> from collections import OrderedDict
        >>> o = OrderedDict([("foo", {}), ("bar", {})])
        >>> e = Event("Foo", subevents=o)

        >>> list(e)
        [Event('foo'), Event('bar')]

    """

    def __init__(self, name="", subevents=None, **kwsubevents):
        super(Event, self).__init__()

        if subevents is None:
            subevents = {}

        self.name = str(name)

        e = itertools.chain(subevents.iteritems(), kwsubevents.iteritems())
        self._subevents = subevents.__class__((k, Event(k, v)) for k, v in e)

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
        return "Event('{.name}')".format(self)

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
                          "removed_from_game" : {},

                          "field" : {
                                     "entered" : {},
                                     "left" : {},
                                    },

                          "graveyard" : {
                                         "entered" : {},
                                         "left" : {},
                                        },
                         },

                "game" : {
                          "started" : {},
                          "ended" : {},
                          "phases" : phases,
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
