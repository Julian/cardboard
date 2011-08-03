import unittest

import panglery

from cardboard.events import events as e
import cardboard.core as c

class TestPlayerState(unittest.TestCase):
    def setUp(self):
        p = panglery.Pangler()
        self.p1 = c.Player(deck=range(8), event_handler=p, life=1)
        self.p2 = c.Player(deck=range(8), event_handler=p, life=2)
        self.p3 = c.Player(deck=range(8), event_handler=p, life=3)
        self.s = c.State(players=[self.p1, self.p2, self.p3], event_handler=p)

    def test_game_over(self):
        self.assertFalse(self.s.game_over)
        self.p1.life -= 1
        self.assertFalse(self.s.game_over)
        self.p2.life -= 2
        self.assertTrue(self.s.game_over)

    def test_advance(self):
        self.assertIs(self.s.turn, self.p1)

        self.assertEqual(self.s.phase, "beginning")
        self.assertEqual(self.s.subphase, "untap")

        for phase, subphase in [("beginning", "draw"),
                                ("beginning", "upkeep"),
                                ("first main", None),
                                ("combat", "beginning"),
                                ("combat", "declare attackers"),
                                ("combat", "declare blockers"),
                                ("combat", "combat damage"),
                                ("combat", "end"),
                                ("second main", None),
                                ("ending", "end"),
                                ("ending", "cleanup")]:

            self.s.advance()
            self.assertEqual(self.s.phase, phase)
            self.assertEqual(self.s.subphase, subphase)

        self.s.advance()

        self.assertIs(self.s.turn, self.p2)

        self.assertEqual(self.s.phase, "beginning")
        self.assertEqual(self.s.subphase, "untap")

    def test_draw(self):
        self.p1.draw()
        self.assertEqual(self.p1.hand, set(range(8)))


class TestStatee(unittest.TestCase):
    def setUp(self):
        self.pangler = panglery.Pangler()
        self.p1 = c.Player(deck=range(8), event_handler=self.pangler, life=1)
        self.p2 = c.Player(deck=range(8), event_handler=self.pangler, life=2)
        self.p3 = c.Player(deck=range(8), event_handler=self.pangler, life=3)
        self.s = c.State(players=[self.p1, self.p2, self.p3],
                         event_handler=self.pangler)

        self._listening = []
        self.heard = []

    def listen_for(self, **kwargs):
        self._listening.append(kwargs)

        @self.pangler.subscribe(**kwargs)
        def got_event(pangler):
            self.heard.append(kwargs)

    def assertHeard(self, **kwargs):
        if kwargs not in self._listening:
            self.fail("Wasn't listening for {}".format(kwargs))
        return self.assertIn(kwargs, self.heard)

    def assertNotHeard(self, **kwargs):
        if kwargs not in self._listening:
            self.fail("Wasn't listening for {}".format(kwargs))
        return self.assertNotIn(kwargs, self.heard)

    def test_game_over(self):
        self.listen_for(event=e["player died"], player=self.p1)
        self.listen_for(event=e["player died"], player=self.p2)
        self.listen_for(event=e["game over"])

        self.p2.life -= 1
        self.assertNotHeard(event=e["player died"], player=self.p2)
        self.assertNotHeard(event=e["game over"])

        self.p2.life -= 1
        self.assertHeard(event=e["player died"], player=self.p2)
        self.assertNotHeard(event=e["game over"])

        self.p1.life -= 1
        self.assertHeard(event=e["player died"], player=self.p1)
        self.assertHeard(event=e["game over"])

    def test_life_changed(self):
        self.listen_for(event=e["life gained"])
        self.listen_for(event=e["life lost"])

        self.p1.life += 2
        self.assertHeard(event=e["life gained"])

        self.p2.life -= 1
        self.assertHeard(event=e["life lost"])

    def test_card_drawn(self):
        self.listen_for(event=e["card drawn"], player=self.p1)
        self.listen_for(event=e["life lost"], player=self.p1)

        self.p1.draw()
        self.assertHeard(event=e["card drawn"], player=self.p1)

        self.heard = []
        self.p1.draw()
        self.assertNotHeard(event=e["card drawn"], player=self.p1)
        self.assertHeard(event=e["life lost"], player=self.p1)

    def test_move_to_graveyard(self):
        card = object()
        self.listen_for(event=e["card added to graveyard"], card=card)
        self.p1.move_to_graveyard(card)
        self.assertHeard(event=e["card added to graveyard"], card=card)
