from cardboard import types


def _type_check_factory(type):
    def has_types(*types):
        types = set(types)

        def _has_types(obj):
            return types <= getattr(obj, type)

        return _has_types

    def lacks_types(*types):
        types = set(types)

        def _lacks_types(obj):
            return not types & getattr(obj, type)

        return _lacks_types

    return has_types, lacks_types


def _type_check(*types): return has_types(*types), lacks_types(*types)


has_types, lacks_types = _type_check_factory("types")
has_subtypes, lacks_subtypes = _type_check_factory("subtypes")
has_supertypes, lacks_supertypes = _type_check_factory("supertypes")

is_artifact, is_not_artifact = _type_check(types.artifact)
is_creature, is_not_creature = _type_check(types.creature)
is_enchantment, is_not_enchantment = _type_check(types.enchantment)
is_instant, is_not_instant = _type_check(types.instant)
is_land, is_not_land = _type_check(types.land)
is_planeswalker, is_not_planeswalker = _type_check(types.planeswalker)
is_sorcery, is_not_sorcery = _type_check(types.sorcery)

def is_basic_land(obj): return is_land(obj) and has_supertypes(u"Basic")(obj)
def is_nonbasic_land(ob): return is_land(ob) and lacks_supertypes(u"Basic")(ob)

def is_permanent(obj): return obj.types & types.permanents
def is_nonpermanent(obj): return obj.types & types.nonpermanents
