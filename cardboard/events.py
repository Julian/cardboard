"""
.. module:: events
    :synopsis: Defines the various game events.

======
Events
======

Whenever a game event occurs, the event handler will trigger an event. Game
objects can subscribe and react to the events (see :doc:`implementing_a_card`
for examples).

A triggered event may have one or more parameters that describe more specific
information about the event. The names of these parameters are specific to the
event.

The different types of events are outlined below, along with an explanation of
each event's respective parameters.


Turn Events
-----------

Turn events are events that trigger when a game, turn, :term:`phase` or
:term:`step` begins or ends.


+----------------------+----------------+-------------------------------------+
| Event                | Description    | Parameters                          |
+======================+================+=====================================+
| :const:`GAME_BEGAN`  | The game began.| * ``game``: ``<the game object>``   |
+----------------------+----------------+-------------------------------------+
| :const:`GAME_ENDED`  | The game ended.| * ``game``: ``<the game object>``   |
+----------------------+----------------+-------------------------------------+
| :const:`TURN_BEGAN`  | A turn began.  | * ``player``:                       |
|                      |                |   ``<the active player>``           |
|                      |                | * ``number``: ``<the turn number>`` |
+----------------------+----------------+-------------------------------------+
| :const:`TURN_ENDED`  | A turn ended.  | * ``player``:                       |
|                      |                |   ``<the formerly active player>``  |
|                      |                | * ``number``: ``<the turn number>`` |
+----------------------+----------------+-------------------------------------+
| :const:`PHASE_BEGAN` | A phase began. | * ``phase``:                        |
|                      |                |   ``<the beginning phase>``         |
|                      |                | * ``player``:                       |
|                      |                |   ``<the active player>``           |
+----------------------+----------------+-------------------------------------+
| :const:`PHASE_ENDED` | A phase ended. | * ``phase``:                        |
|                      |                |   ``<the beginning phase>``         |
|                      |                | * ``player``:                       |
|                      |                |   ``<the active player>``           |
+----------------------+----------------+-------------------------------------+


Player Events
-------------

Player events are triggered for in-game events affecting a :term:`player` in
the game.


+--------------------------+--------------------+-----------------------------+
| Event                    | Description        | Parameters                  |
+======================+======================================================+
| :const:`PLAYER_CONCEDED` | A player conceded. | * ``player``:               |
|                          |                    |   ``<the conceding player>``|
+--------------------------+------------+-------------------------------------+
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
| :const:`TURN_ENDED`      | A turn ended.      | * ``player``:               |
|                          |                    |   ``<the formere player>``  |
|                          |                    | * ``number``: `rn number>`` |
+--------------------------+--------------------+-----------------------------+
| :const:`PHASE_BEGAN`     | A phase began.     | * ``phase``:                |
|                          |                    |   ``<the beginne>``         |
|                          |                    | * ``player``:               |
|                          |                    |   ``<the active``           |
+--------------------------+--------------------+-----------------------------+
| :const:`PHASE_ENDED`     | A phase ended.     | * ``phase``:                |
|                          |                    |   ``<the beginne>``         |
|                          |                    | * ``player``:               |
|                          |                    |   ``<the active``           |
+--------------------------+--------------------+-------------------------------------+

draw
^^^^

A player :term:`drew <draw>` a card.

* ``event``: :const:`DRAW`
* ``player``: ``<the drawing player>``

life gained / life lost
^^^^^^^^^^^^^^^^^^^^^^^

A player gained or lost :term:`life <life, life total>`.

* ``event``: :const:`LIFE_GAINED` / :const:`LIFE_LOST`
* ``player``: ``<the player>``
* ``amount``: ``<the amount of life (always positive)>``

mana changes
^^^^^^^^^^^^

Player events will also be triggered when a player adds or removes :term:`mana`
from his :term:`mana pool`.  The mana event will be triggered with:

* ``event``: :const:`MANA_ADDED` / :const:`MANA_REMOVED`
* ``color``: ``"white"`` / ``"blue"`` / ``"black"`` / ``"red"`` /
    ``"green"`` / ``"colorless"``
* ``player``: ``<the player>``
* ``amount``: ``<the amount of mana (always positive)>``


Card & Spell Events
-------------------

Card and spell events are triggered for events that are relevant to cards,
:term:`spells <spell>` and :term:`abilities <ability>`.

    .. note::

        Generally the game does not distinguish (currently) between cards and
        other game :term:`objects <object>`. They are also referred to as cards
        for this purpose.

The card and spell events are as follows:

cast
^^^^

A card was :term:`cast`.

* ``event``: :const:`CARD_CAST`
* ``card``: ``<the casted card>``
* ``player``: ``<the casting player>``

countered
^^^^^^^^^

A spell was :term:`countered <counter>`.

* ``event``: :const:`SPELL_COUNTERED`
* ``spell``: ``<the countered spell>``

resolved
^^^^^^^^

A spell :term:`resolved <resolve>`.

* ``event``: :const:`SPELL_RESOLVED`
* ``spell``: ``<the resolving spell>``


status changes
^^^^^^^^^^^^^^

Additionally, cards have a number of :term:`status` change events that fire
when a card's status changes. The triggered event will look like:

* ``event``: :const:`STATUS_CHANGED`
* ``card``: ``<the card>``
* ``status``: one of:
    * ``"tapped"`` / ``"untapped"``
    * ``"flipped"`` / ``"unflipped"``
    * ``"face up"`` / ``"face down"``
    * ``"phased in"`` / ``"phased out"``


zone changes
^^^^^^^^^^^^

Finally, cards will trigger zone change events when their location is changed.
The card will trigger an event with the zone it is leaving, followed by another
when it enters its destination:

* ``event``: :const:`ENTERED_ZONE` / :const:`LEFT_ZONE`
* ``card``: ``<the card>``
* ``zone``: ``<the relevant zone>``

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
