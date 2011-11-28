import mock

from cardboard import ability as c, exceptions
from cardboard.tests.util import GameTestCase


class TestAbility(GameTestCase):
    def test_repr_str(self):
        a = c.Ability(description="Does foo.", action=None, type="static")
        self.assertEqual(repr(a), "<Static Ability: Does foo.>")
        self.assertEqual(str(a), "Does foo.")

        a = c.Ability(description="f" * 100, action=None, type="spell")
        self.assertEqual(repr(a), "<Spell Ability: {} ... >".format("f" * 40))
        self.assertEqual(str(a), "f" * 100)

    def test_init(self):
        types = "spell", "activated", "triggered", "static"
        noop = lambda card : None

        a = [c.Ability(description="foo", action=noop, type=t) for t in types]

        self.assertEqual(a[0].action, noop)
        self.assertEqual(a[0].description, "foo")

        self.assertEqual(a[0].type, "spell")
        self.assertEqual(a[1].type, "activated")
        self.assertEqual(a[2].type, "triggered")
        self.assertEqual(a[3].type, "static")

    def test_call(self):
        m = mock.Mock()
        a = c.Ability(description="", action=m, type="spell")
        a()
        m.assert_called_once_with()

    def test_abilities(self):
        m = mock.Mock()

        a = c.Ability.spell(description="Foo")(m)
        self.assertEqual(a.action, m)
        self.assertEqual(a.description, "Foo")
        self.assertEqual(a.type, "spell")

        a = c.Ability.activated(cost="2BB", description="Foo")(m)
        self.assertEqual(a.action, m)
        self.assertEqual(a.description, "Foo")
        self.assertEqual(a.type, "activated")
        self.assertEqual(a.cost, "2BB")

        a = c.Ability.triggered(event="Bar", condition=3, description="Foo")(m)
        self.assertEqual(a.action, m)
        self.assertEqual(a.description, "Foo")
        self.assertEqual(a.type, "triggered")
        self.assertEqual(a.trigger, {"event" : "Bar", "condition" : 3})

        a = c.Ability.static(description="Foo")(m)
        self.assertEqual(a.action, m)
        self.assertEqual(a.description, "Foo")
        self.assertEqual(a.type, "static")

    def test_not_implemented(self):
        n = c.Ability.NotImplemented
        self.assertEqual(repr(n), "<Ability Not Implemented>")
        with self.assertRaises(exceptions.NotImplemented):
            n()
