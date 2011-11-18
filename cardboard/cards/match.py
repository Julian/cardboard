from cardboard import types


class Match(object):
    def __init__(self, fn=None, **predicates):
        super(Match, self).__init__()

        if fn:
            if predicates:
                attr_match = _attr_match(**predicates)

                def _fn(obj, *args, **kwargs):
                    return fn(obj, *args, **kwargs) and attr_match(obj)

                self._fn = _fn
            else:
                self._fn = fn
        elif predicates:
            self._fn = _attr_match(**predicates)
        else:
            raise ValueError("Either a function or predicates are required.")

    def __call__(self, *args, **kwargs):
        return self._fn(*args, **kwargs)

    def __and__(self, other):
        return Match(
            lambda *args, **kw : self._fn(*args, **kw) and other(*args, **kw)
        )

    def __invert__(self):
        return Match(lambda *args, **kw : not self._fn(*args, **kw))

    def __or__(self, other):
        return Match(
            lambda *args, **kw : self._fn(*args, **kw) or other(*args, **kw)
        )


def _attr_match(**predicates):
    def attr_match(obj):
        return all(getattr(obj, k) == v for k, v in predicates.iteritems())
    return attr_match


def _check_factory(characteristic):
    def has_characteristics(*characteristics):
        characteristics = set(characteristics)

        def _has(obj):
            return characteristics <= getattr(obj, characteristic)

        return Match(_has)
    return has_characteristics


has_colors = Match(_check_factory("colors"))
has_types = Match(_check_factory("types"))
has_subtypes = Match(_check_factory("subtypes"))
has_supertypes = Match(_check_factory("supertypes"))

is_white = Match(has_colors("W"))
is_blue = Match(has_colors("U"))
is_black = Match(has_colors("B"))
is_red = Match(has_colors("R"))
is_green = Match(has_colors("G"))
is_colorless = Match(lambda o : not o.colors)

is_artifact = Match(has_types(types.artifact))
is_creature = Match(has_types(types.creature))
is_enchantment = Match(has_types(types.enchantment))
is_instant = Match(has_types(types.instant))
is_land = Match(has_types(types.land))
is_planeswalker = Match(has_types(types.planeswalker))
is_sorcery = Match(has_types(types.sorcery))

is_basic_land = is_land & has_supertypes(u"Basic")
is_nonbasic_land = is_land & ~has_supertypes(u"Basic")

is_permanent = Match(lambda obj : obj.types & types.permanents)
