import unittest

import mock

from cardboard import phases as p
from cardboard.events import events
from cardboard.frontend.testing import TestingFrontend
from cardboard.tests.util import GameTestCase


class TestPhase(unittest.TestCase):
    def test_init(self):
        h = p.Phase("Foo", [1, 2, 3])

        self.assertEqual(h.name, "Foo")
        self.assertEqual(h.steps, [1, 2, 3])

    def test_iter(self):
        h = p.Phase("Foo", [1, 2, 3])
        self.assertEqual(list(h), [1, 2, 3])

    def test_getitem(self):
        h = p.Phase("Foo", [1, 2, 3])

        self.assertEqual(h[0], 1)
        self.assertEqual(h[1], 2)
        self.assertEqual(h[2], 3)

    def test_len(self):
        h = p.Phase("Foo", [1, 2, 3])
        self.assertEqual(len(h), 3)

    def test_repr_str(self):
        h = p.Phase("foo_bar", [1, 2, 3])
        self.assertEqual(repr(h), "<Phase: Foo Bar>")
        self.assertEqual(str(h), "Foo Bar")


class TestPhaseMechanics(GameTestCase):
    def test_untap(self):
        """
        The untap step should perform the actions in :ref:`untap-step`.

        """

        self.game.start()

        own = [mock.Mock() for _ in range(4)]
        not_own = [mock.Mock() for _ in range(4)]

        # TODO: Just double check that this is how the final implementation is
        phasing = mock.Mock()
        phasing.description = "Phasing"

        own[0].abilities = own[1].abilities = []
        not_own[0].abilities = not_own[1].abilities = []

        own[2].abilities = own[3].abilities = [phasing]
        own[2].is_phased_in = False

        not_own[2].abilities = not_own[3].abilities = [phasing]
        not_own[2].is_phased_in = False

        for n, o in zip(own, not_own):
            n.types = o.types = {"Enchantment"}

        for o in own:
            o.controller = self.game.turn.active_player

        self.game.battlefield.update(own, not_own)

        p.untap(self.game)

        # all phased-in permanents with phasing that the active player controls
        # phase out, and all phased-out permanents controlled when they phased
        # out phase in

        self.assertTrue(own[2].phase_in.called)
        self.assertTrue(own[3].phase_out.called)

        self.assertFalse(not_own[2].phase_in.called)
        self.assertFalse(not_own[3].phase_out.called)

        # the active player determines which permanents he controls will untap
        # Then he untaps them all simultaneously. 

        for o in own:
            o.untap.assert_called_once_with()

        for o in not_own:
            self.assertFalse(o.untap.called)

        self.assertTriggered([
            events["game"]["turn"]["phase"]["beginning"]["untap"]["started"],
            events["game"]["turn"]["phase"]["beginning"]["untap"]["ended"],
        ])

        # XXX: Normally all untap. but effects can keep some from untapping.

    def test_upkeep(self):
        """
        The upkeep step should perform the actions in :ref:`upkeep-step`.

        """

        self.game.start()
        self.game.grant_priority = mock.Mock()

        p.upkeep(self.game)
        self.assertTrue(self.game.grant_priority.called)

        self.assertTriggered([
            events["game"]["turn"]["phase"]["beginning"]["upkeep"]["started"],
            events["game"]["turn"]["phase"]["beginning"]["upkeep"]["ended"],
        ])

    def test_draw(self):
        """
        The draw step should perform the actions in :ref:`draw-step`.

        """

        self.game.start()
        self.game.turn.active_player.draw = mock.Mock()
        self.game.grant_priority = mock.Mock()

        p.draw(self.game)

        self.assertTrue(self.game.turn.active_player.draw.called)
        self.assertTrue(self.game.grant_priority.called)

        self.assertTriggered([
            events["game"]["turn"]["phase"]["beginning"]["draw"]["started"],
            events["game"]["turn"]["phase"]["beginning"]["draw"]["ended"],
        ])

    def test_main(self):
        """
        The main phase should perform the actions in :ref:`main-phase`.

        """

        self.game.start()
        self.game.grant_priority = mock.Mock()

        p.first_main.steps[0](self.game)
        self.assertTrue(self.game.grant_priority.called)

        self.assertTriggered([
            events["game"]["turn"]["phase"]["first_main"]["started"],
            events["game"]["turn"]["phase"]["first_main"]["ended"],
        ])

        self.resetEvents()
        self.game.grant_priority = mock.Mock()

        p.second_main.steps[0](self.game)
        self.assertTrue(self.game.grant_priority.called)

        self.assertTriggered([
            events["game"]["turn"]["phase"]["second_main"]["started"],
            events["game"]["turn"]["phase"]["second_main"]["ended"],
        ])

    def test_end(self):
        """
        The end step should perform the actions in :ref:`end-step`.

        """

        self.game.start()
        self.game.grant_priority = mock.Mock()

        p.end(self.game)
        self.assertTrue(self.game.grant_priority.called)

        self.assertTriggered([
            events["game"]["turn"]["phase"]["ending"]["end"]["started"],
            events["game"]["turn"]["phase"]["ending"]["end"]["ended"],
        ])

    def test_cleanup(self):
        """
        The cleanup step should perform the actions in :ref:`cleanup-step`.

        """

        self.game.start()

        player = self.game.turn.active_player
        player.frontend = TestingFrontend(player)
        player.draw(3)

        discard = list(player.hand)[:-7]

        with player.frontend.select.cards.will_return(*discard):
            p.cleanup(self.game)

        for card in discard:
            self.assertIn(card, player.graveyard)

        # XXX: remove all damage

        self.assertTriggered([
            events["game"]["turn"]["phase"]["ending"]["cleanup"]["started"],
            events["game"]["turn"]["phase"]["ending"]["cleanup"]["ended"],
        ])
