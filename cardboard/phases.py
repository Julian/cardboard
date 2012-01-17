"""
Implements the turn structure mechanics (phases and steps).

.. seealso::
    The :ref:`turn-structure` section of the :ref:`comprehensive-rules`.

"""

from collections import namedtuple

from cardboard import events
from cardboard.cards import match


def untap(game):
    """
    Perform the :ref:`untap-step`.

    What Happens
    ------------

    1. The active player's phased-in permanents phase out, and vice versa.
    2. The active player's permanents that can be untapped are untapped.
    3. No players get priority.

    """

    player = game.turn.active_player

    # XXX: Technically the rules say all this is "simultaneous".
    #      At some point that will probably matter, and we will need some tests
    #      and an implementation of that.

    game.events.trigger(
        event=events.STEP_BEGAN, phase="beginning",
        step="untap", player=player,
    )

    for permanent in player.battlefield:
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

    game.events.trigger(
        event=events.STEP_ENDED, phase="beginning",
        step="untap", player=player,
    )


def upkeep(game):
    """
    Perform the :ref:`upkeep-step`.

    What Happens
    ------------

    1. Abilities trigger.
    2. The active player gets priority.

    """

    game.events.trigger(
        event=events.STEP_BEGAN, phase="beginning",
        step="upkeep", player=game.turn.active_player,
    )

    game.grant_priority()

    game.events.trigger(
        event=events.STEP_ENDED, phase="beginning",
        step="upkeep", player=game.turn.active_player,
    )


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

    game.events.trigger(
        event=events.STEP_BEGAN, phase="beginning",
        step="draw", player=game.turn.active_player
    )

    game.grant_priority()

    game.events.trigger(
        event=events.STEP_ENDED, phase="beginning",
        step="draw", player=game.turn.active_player,
    )


def _main(game):
    """
    Perform the :ref:`main-phase`.

    """

    game.grant_priority()


def first_main(game):
    player = game.turn.active_player

    game.events.trigger(
        event=events.PHASE_BEGAN, phase="first main", player=player,
    )

    _main(game)

    game.events.trigger(
        event=events.PHASE_ENDED, phase="first main", player=player,
    )


def beginning_of_combat(game):
    """
    Perform the :ref:`beginning-combat-step`.

    """

    game.events.trigger(
        event=events.STEP_BEGAN, phase="combat",
        step="beginning", player=game.turn.active_player
    )

    game.grant_priority()

    game.events.trigger(
        event=events.STEP_ENDED, phase="combat",
        step="beginning", player=game.turn.active_player
    )


def declare_attackers(game):
    """
    Perform the :ref:`declare-attackers-step`.

    """

    game.events.trigger(
        event=events.STEP_BEGAN, phase="combat",
        step="declare attackers", player=game.turn.active_player
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
        event=events.STEP_ENDED, phase="combat",
        step="declare attackers", player=game.turn.active_player
    )


def declare_blockers(game):
    """
    Perform the :ref:`declare-blockers-step`.

    """

    game.events.trigger(
        event=events.STEP_BEGAN, phase="combat",
        step="declare blockers", player=game.turn.active_player
    )

    game.events.trigger(
        event=events.STEP_ENDED, phase="combat",
        step="declare blockers", player=game.turn.active_player
    )


def combat_damage(game):
    """
    Perform the :ref:`combat-damage-step`.

    """

    game.events.trigger(
        event=events.STEP_BEGAN, phase="combat",
        step="combat damage", player=game.turn.active_player
    )

    game.events.trigger(
        event=events.STEP_ENDED, phase="combat",
        step="combat damage", player=game.turn.active_player
    )


def end_of_combat(game):
    """
    Perform the :ref:`end-combat-step`.

    """

    game.events.trigger(
        event=events.STEP_BEGAN, phase="combat",
        step="end", player=game.turn.active_player
    )
    game.events.trigger(
        event=events.STEP_ENDED, phase="combat",
        step="end", player=game.turn.active_player
    )


def second_main(game):
    player = game.turn.active_player

    game.events.trigger(
        event=events.PHASE_BEGAN, phase="second main", player=player,
    )

    _main(game)

    game.events.trigger(
        event=events.PHASE_ENDED, phase="second main", player=player,
    )


def end(game):
    """
    Perform the :ref:`end-step`.

    What Happens
    ------------

    1. Abilities that trigger at the end of turn will be executed
    2. The active player gets priority.

    """

    game.events.trigger(
        event=events.STEP_BEGAN, phase="ending",
        step="end", player=game.turn.active_player
    )

    game.grant_priority()

    game.events.trigger(
        event=events.STEP_ENDED, phase="ending",
        step="end", player=game.turn.active_player
    )


def cleanup(game):
    """
    Perform the :ref:`cleanup-step`.

    """

    # 1. Hand size is trimmed to the max hand size (usually 7)
    # 2. XXX: All damage is removed and end of turn effects end.
    # 3. No players get priority # XXX: except for the exception in rule 514.3a

    game.events.trigger(
        event=events.STEP_BEGAN, phase="ending",
        step="cleanup", player=game.turn.active_player
    )

    player = game.turn.active_player
    discard = len(player.hand) - player.hand_size

    if discard > 0:
        selection = player.frontend.select_cards(
            zone=player.hand, how_many=discard,
        )

        for card in selection:
            card.owner.graveyard.move(card)

    game.events.trigger(
        event=events.STEP_ENDED, phase="ending",
        step="cleanup", player=game.turn.active_player
    )


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
