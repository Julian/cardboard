import functools

from cardboard import exceptions


__all__ = ["Ability", "spell", "activated", "triggered", "static"]


class _AbilityNotImplemented(object):
    def __call__(self):
        raise exceptions.NotImplemented("Ability is not implemented.")

    def __repr__(self):
        return "<Ability Not Implemented>"


class Ability(object):

    TYPES = frozenset({"spell", "activated", "triggered", "static"})
    NotImplemented = _AbilityNotImplemented()

    def __init__(self, action, description, type):
        super(Ability, self).__init__()

        self.action = action
        self.description = description
        self.type = type

    def __call__(self):
        self.action()

    def __repr__(self):
        elipsis = " ... " if len(self.description) > 40 else ""
        type = self.type.title()
        return "<{} Ability: {.description:.40}{}>".format(type, self, elipsis)

    def __str__(self):
        return self.description

    @classmethod
    def spell(cls, description):
        return functools.partial(cls, description=description, type="spell")

    @classmethod
    def activated(cls, cost, description):
        @functools.wraps(cls)
        def activated_ability(action):
            a = cls(action=action, description=description, type="activated")
            a.cost = cost
            return a
        return activated_ability

    @classmethod
    def triggered(cls, description, **event_params):
        @functools.wraps(cls)
        def triggered_ability(action):
            a = cls(action=action, description=description, type="triggered")
            a.trigger = event_params
            return a
        return triggered_ability

    @classmethod
    def static(cls, description):
        return functools.partial(cls, description=description, type="static")


spell = Ability.spell
activated = Ability.activated
triggered = Ability.triggered
static = Ability.static
