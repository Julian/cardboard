"""
Implements the turn structure mechanics (phases and steps).

.. seealso::
    The :ref:`turn-structure` section of the :ref:`comprehensive-rules`.

"""

from collections import namedtuple

from cardboard.events import events
from cardboard.cards import match


phase_events = events["game"]["turn"]["phase"]


def untap(game):
    """
    Perform the :ref:`untap-step`.

    What Happens
    ------------

    1. The active player's phased-in permanents phase out, and vice versa.
    2. The active player's permanents that can be untapped are untapped.
    3. No players get priority.

    """

    # XXX: Technically the rules say all this is "simultaneous".
    #      At some point that will probably matter, and we will need some tests
    #      and an implementation of that.

    game.events.trigger(event=phase_events["beginning"]["untap"]["started"])

    for permanent in game.turn.active_player.battlefield:
        if match.phases(permanent):
            if permanent.is_phased_in:
                permanent.phase_out()
            else:
                permanent.phase_in()

        if permanent.is_tapped:
            # XXX: Check if the permanent says it can be untapped.
            permanent.untap()

    # XXX: Again, technically abilities can't activate / resolve here, they
    #      should be deferred until the upkeep.

    game.events.trigger(event=phase_events["beginning"]["untap"]["ended"])


def upkeep(game):
    """
    Perform the :ref:`upkeep-step`.

    What Happens
    ------------

    1. Abilities trigger.
    2. The active player gets priority.

    """

    game.events.trigger(event=phase_events["beginning"]["upkeep"]["started"])
    game.grant_priority()
    game.events.trigger(event=phase_events["beginning"]["upkeep"]["ended"])


def draw(game):
    """
    Perform the :ref:`draw-step`.

    What Happens
    ------------

    1. The active player draws a card.
    2. Abilities trigger.
    3. The active player gets priority.

    """

    game.turn.active_player.draw()
    game.events.trigger(event=phase_events["beginning"]["draw"]["started"])
    game.grant_priority()
    game.events.trigger(event=phase_events["beginning"]["draw"]["ended"])


def _main(game):
    """
    Perform the :ref:`main-phase`.

    """

    game.grant_priority()


def first_main(game):
    game.events.trigger(event=phase_events["first_main"]["started"])
    _main(game)
    game.events.trigger(event=phase_events["first_main"]["ended"])


def beginning_of_combat(game):
    """
    Perform the :ref:`beginning-combat-step`.

    """

    game.events.trigger(event=phase_events["combat"]["beginning"]["started"])
    game.grant_priority()
    game.events.trigger(event=phase_events["combat"]["beginning"]["ended"])


def declare_attackers(game):
    """
    Perform the :ref:`declare-attackers-step`.

    """

    game.events.trigger(
        event=phase_events["combat"]["declare_attackers"]["started"]
    )

    possible_attackers = {c for c in game.battlefield if c.can_attack}

    targets = game.turn.active_player.opponents

    for opponent in targets:
        targets |= {card for card in opponent.battlefield
                    if card.type == "Planeswalker"}

    # attackers = game.turn.active_player.frontend.select.cards(
    #     game.battlefield, how_many=None
    # )
    # attacks = {
    #    k : game.turn.active_player.frontend.select.combined(attackers)
    #    for k in attackers
    # }

    # for card in attacks:
    #     card.tap()

    game.grant_priority()
    game.events.trigger(
        event=phase_events["combat"]["declare_attackers"]["ended"]
    )


def declare_blockers(game):
    """
    Perform the :ref:`declare-blockers-step`.

    """

    game.events.trigger(
        event=phase_events["combat"]["declare_blockers"]["started"]
    )

    game.events.trigger(
        event=phase_events["combat"]["declare_blockers"]["ended"]
    )


def combat_damage(game):
    """
    Perform the :ref:`combat-damage-step`.

    """

    game.events.trigger(
        event=phase_events["combat"]["combat_damage"]["started"]
    )

    game.events.trigger(
        event=phase_events["combat"]["combat_damage"]["ended"]
    )


def end_of_combat(game):
    """
    Perform the :ref:`end-combat-step`.

    """

    game.events.trigger(event=phase_events["combat"]["end"]["started"])
    game.events.trigger(event=phase_events["combat"]["end"]["ended"])


def second_main(game):
    game.events.trigger(event=phase_events["second_main"]["started"])
    _main(game)
    game.events.trigger(event=phase_events["second_main"]["ended"])


def end(game):
    """
    Perform the :ref:`end-step`.

    What Happens
    ------------

    1. Abilities that trigger at the end of turn will be executed
    2. The active player gets priority.

    """

    game.events.trigger(event=phase_events["ending"]["end"]["started"])
    game.grant_priority()
    game.events.trigger(event=phase_events["ending"]["end"]["ended"])


def cleanup(game):
    """
    Perform the :ref:`cleanup-step`.

    """

    # 1. Hand size is trimmed to the max hand size (usually 7)
    # 2. XXX: All damage is removed and end of turn effects end.
    # 3. No players get priority # XXX: except for the exception in rule 514.3a

    game.events.trigger(event=phase_events["ending"]["cleanup"]["started"])

    player = game.turn.active_player
    discard = len(player.hand) - player.hand_size

    if discard > 0:
        selection = player.frontend.select.cards(
            zone=player.hand, how_many=discard,
        )

        for card in selection:
            card.owner.graveyard.move(card)

    game.events.trigger(event=phase_events["ending"]["cleanup"]["ended"])


class Phase(object):
    def __init__(self, name, steps):
        super(Phase, self).__init__()

        self.name = str(name)
        self.steps = list(steps)

    def __getitem__(self, i):
        return self.steps[i]

    def __iter__(self):
        return iter(self.steps)

    def __len__(self):
        return len(self.steps)

    def __str__(self):
        return unicode(self).encode("utf-8")

    def __unicode__(self):
        return self.name.replace("_", " ").title()

    def __repr__(self):
        return "<Phase: {}>".format(self)


beginning = Phase("beginning", [untap, upkeep, draw])
first_main = Phase("first_main", [first_main])
combat = Phase("combat", [beginning_of_combat, declare_attackers,
                          declare_blockers, combat_damage, end_of_combat])
second_main = Phase("second_main", [second_main])
ending = Phase("ending", [end, cleanup])

phases = (beginning, first_main, combat, second_main, ending)
