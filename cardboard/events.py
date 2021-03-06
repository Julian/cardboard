"""
.. module:: events
    :synopsis: Defines the various game events.


Whenever a game event occurs, the event handler will trigger an event. Game
objects can subscribe and react to the events (see :doc:`implementing_a_card`
for examples).

A triggered event may have one or more parameters that describe more specific
information about the event. The names of these parameters are specific to the
event.

The different types of events are outlined below, along with an explanation of
each event's respective parameters.


Turn Events
===========

Turn events are events that trigger when a game, turn, :term:`phase` or
:term:`step` begins or ends.


+----------------------+----------------+-------------------------------------+
| Event                | Description    | Parameters                          |
+======================+================+=====================================+
| :const:`GAME_BEGAN`  | The game began | * ``game``: ``<the game object>``   |
+                      + (resp. ended). +                                     +
| :const:`GAME_ENDED`  |                |                                     |
+----------------------+----------------+-------------------------------------+
| :const:`TURN_BEGAN`  | A turn began   | * ``player``:                       |
|                      | (resp. ended). |   ``<the active player>``           |
| :const:`TURN_ENDED`  |                | * ``number``: ``<the turn number>`` |
+----------------------+----------------+-------------------------------------+
| :const:`PHASE_BEGAN` | A phase began  | * ``phase``:                        |
|                      | (resp. ended). |   ``<the beginning phase>``         |
| :const:`PHASE_ENDED` |                | * ``player``:                       |
|                      |                |   ``<the relevant player>``         |
+----------------------+----------------+-------------------------------------+


Player Events
=============

Player events are triggered for in-game events affecting a :term:`player` in
the game.


+--------------------------+--------------------+-----------------------------+
| Event                    | Description        | Parameters                  |
+==========================+====================+=============================+
| :const:`PLAYER_CONCEDED` | A player conceded. | * ``player``:               |
|                          |                    |   ``<the conceding player>``|
+--------------------------+--------------------+-----------------------------+
| :const:`PLAYER_DIED`     | A player died.     | * ``player``:               |
|                          |                    |   ``<the dying player>``    |
|                          |                    | * ``reason``:               |
|                          |                    |   ``<a reason for death>``  |
+--------------------------+--------------------+-----------------------------+
| :const:`DRAW`            | A player           | * ``player``:               |
|                          | :term:`drew <draw>`|   ``<the drawing player>``  |
|                          | a card.            |                             |
|                          |                    |                             |
+--------------------------+--------------------+-----------------------------+
| :const:`LIFE_GAINED`     | A player gained    | * ``player``:               |
|                          | or lost life.      |   ``<the player>``          |
| :const:`LIFE_LOST`       |                    | * ``amount``:               |
|                          |                    |   ``<the amount of life>``  |
|                          |                    |   (always positive)         |
+--------------------------+--------------------+-----------------------------+
| :const:`MANA_ADDED`      | :term:`Mana` was   | * ``color``:                |
|                          | added to or removed|   ``"white"`` / ``"blue"`` /|
|                          | from a player's    |   ``"black"`` / ``"red"`` / |
| :const:`MANA_REMOVED`    | :term:`mana pool`. |   ``"green"`` /             |
|                          |                    |   ``"colorless"``           |
|                          |                    | * ``player``:               |
|                          |                    |   ``<the player>``          |
|                          |                    | * ``amount``:               |
|                          |                    |   ``<the amount of mana>``  |
|                          |                    |   (always positive)         |
+--------------------------+--------------------+-----------------------------+


Card & Spell Events
===================

Card and spell events are triggered for events that are relevant to cards,
:term:`spells <spell>` and :term:`abilities <ability>`.

    .. note::

        Generally the game does not distinguish (currently) between cards and
        other game :term:`objects <object>`. They are also referred to as cards
        for this purpose.

The card and spell events are as follows:


+--------------------------+--------------------+-----------------------------+
| Event                    | Description        | Parameters                  |
+==========================+====================+=============================+
| :const:`CARD_CAST`       | A card was         | * ``card``:                 |
|                          | :term:`cast`.      |   ``<the casted card>``     |
|                          |                    | * ``player``:               |
|                          |                    |   ``<the casting player>``  |
+--------------------------+--------------------+-----------------------------+
| :const:`SPELL_COUNTERED` | A spell was        | * ``spell``:                |
|                          | :term:`countered   |   ``<the countered spell>`` |
|                          | <counter>`.        |                             |
+--------------------------+--------------------+-----------------------------+
| :const:`SPELL_RESOLVED`  | A spell            | * ``spell``:                |
|                          | :term:`resolved    |   ``<the resolving spell>`` |
|                          | <resolve>`.        |                             |
+--------------------------+--------------------+-----------------------------+
| :const:`STATUS_CHANGED`  | A card's           | * ``card``:                 |
|                          | :term:`status` was |   ``<the card>``            |
|                          | changed.           | * ``status``:               |
|                          |                    |                             |
|                          |                    |   * ``"tapped"`` /          |
|                          |                    |     ``"untapped"``          |
|                          |                    |   * ``"flipped"`` /         |
|                          |                    |     ``"unflipped"``         |
|                          |                    |   * ``"face up"`` /         |
|                          |                    |     ``"face down"``         |
|                          |                    |   * ``"phased in"`` /       |
|                          |                    |     ``"phased out"``        |
+--------------------------+--------------------+-----------------------------+
| :const:`ENTERED_ZONE`    | A card entered or  | * ``card``:                 |
|                          | left a             |   ``<the moving card>``     |
| :const:`LEFT_ZONE`       | :term:`zone`.      | * ``zone``:                 |
|                          |                    |   ``<the relevant zone>``   |
+--------------------------+--------------------+-----------------------------+

"""


GAME_BEGAN, GAME_ENDED = "game began", "game ended"
TURN_BEGAN, TURN_ENDED = "turn began", "turn ended"
PHASE_BEGAN, PHASE_ENDED = "phase began", "phase ended"
STEP_BEGAN, STEP_ENDED = "step began", "step ended"

PLAYER_CONCEDED = "player conceded"
PLAYER_DIED = "player died"
DRAW = "draw"
LIFE_GAINED, LIFE_LOST = "life gained", "life lost"
MANA_ADDED, MANA_REMOVED = "mana added", "mana removed"

CARD_CAST = "card cast"
SPELL_COUNTERED = "spell countered"
SPELL_RESOLVED = "spell resolved"

STATUS_CHANGED = "status changed"
TAPPED, UNTAPPED = "tapped", "untapped"
FLIPPED, UNFLIPPED = "flipped", "unflipped"
FACE_UP, FACE_DOWN = "face up", "face down"
PHASED_IN, PHASED_OUT = "phased in", "phased out"

ENTERED_ZONE, LEFT_ZONE = "entered zone", "left zone"
