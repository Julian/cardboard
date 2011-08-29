from itertools import chain


__all__ = ["Event", "events"]


class Event(object):
    """
    An event container.

    """

    def __init__(self, name="", subevents=None, _parent=None, **kwsubevents):
        super(Event, self).__init__()

        if _parent is not None:
            _parent = "{.fully_qualified_name}[{!r}]".format(_parent, name)

        self.fully_qualified_name = _parent or name

        self._subevents = {}
        self.update(subevents, **kwsubevents)

    def __contains__(self, event):
        return event in self._subevents.viewvalues()

    def __eq__(self, other):
        if not isinstance(other, Event):
            return NotImplemented
        return self.name == other.name and self._subevents == other._subevents

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

    @property
    def subevents(self):
        # evading my .viewvalues __eq__ bug
        return set(self._subevents.itervalues())

    def get(self, k, d=None):
        return self._subevents.get(k, d)

    def update(self, subevents=None, **kwsubevents):
        if subevents is None:
            subevents = {}

        for k, v in chain(subevents.iteritems(), kwsubevents.iteritems()):
            self[k] = v


phase_events = {

    "beginning" : {
                   "started" : {},
                   "ended" : {},

                   "untap" : {
                              "started" : {},
                              "ended" : {},
                             },

                   "upkeep" : {
                               "started" : {},
                               "ended" : {},
                              },

                   "draw" : {
                             "started" : {},
                             "ended" : {},
                            },
                  },

    "first_main" : {
                    "started" : {},
                    "ended" : {},
                   },

    "combat" : {
                "started" : {},
                "ended" : {},

                "beginning" : {
                               "started" : {},
                               "ended" : {},
                              },

                "declare_attackers" : {
                                       "started" : {},
                                       "ended" : {},
                                      },

                "declare_blockers" : {
                                      "started" : {},
                                      "ended" : {},
                                     },

                "combat_damage" : {
                                   "started" : {},
                                   "ended" : {},
                                  },

                "end" : {
                         "started" : {},
                         "ended" : {},
                        },
               },

    "second_main" : {
                     "started" : {},
                     "ended" : {},
                    },


    "ending" : {
                   "started" : {},
                   "ended" : {},

                   "end" : {
                            "started" : {},
                            "ended" : {},
                           },

                   "cleanup" : {
                                "started" : {},
                                "ended" : {},
                               },

               },

}


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

                                     "stack" : {
                                                "entered" : {},
                                                "left" : {},
                                               },
                                    }
                         },

                "game" : {
                          "started" : {},
                          "ended" : {},

                          "turn" : {
                                    "started" : {},
                                    "ended" : {},
                                    "phase" : phase_events,
                                   },
                         },

                "player" : {
                            "conceded" : {},
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
