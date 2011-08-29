:tocdepth: 2

.. _additional:

****************
Additional Rules
****************

.. _additional-general:

General
=======

700.1
-----

Anything that happens in a game is an event. Multiple events may take place during the resolution of a spell or ability. The text of triggered abilities and replacement effects defines the event they're looking for. One "happening" may be treated as a single event by one ability and as multiple events by another.

.. admonition:: Example

    If an attacking creature is blocked by two defending creatures, this is one event for a triggered ability that reads "Whenever [this creature] becomes blocked" but two events for a triggered ability that reads "Whenever [this creature] becomes blocked by a creature."

700.2
-----

A spell or ability is modal if it has two or more options preceded by "Choose one  -- ," "Choose two  -- ," "Choose one or both  -- ," or "[a specified player] chooses one  -- ." Each of those options is a mode.

    a. The controller of a modal spell or activated ability chooses the mode(s) as part of casting that spell or activating that ability. If one of the modes would be illegal (due to an inability to choose legal targets, for example), that mode can't be chosen.

        .. seealso::
            :ref:`Rule 601.2b <modal-spell>`

    b. The controller of a modal triggered ability chooses the mode(s) as part of putting that ability on the stack. If one of the modes would be illegal (due to an inability to choose legal targets, for example), that mode can't be chosen. If no mode can be chosen, the ability is removed from the stack.

        .. seealso::
            :ref:`Rule 603.3c <modal-triggered>`

    c. If a spell or ability targets one or more targets only if a particular mode is chosen for it, its controller will need to choose those targets only if he or she chose that mode. Otherwise, the spell or ability is treated as though it did not have those targets.

        .. seealso::
            :ref:`Rule 601.2c <choose-targets>`

    d. Some spells and abilities specify that a player other than their controller chooses a mode for it. In that case, the other player does so when the spell or ability's controller normally would do so. If there is more than one other player who could make such a choice, the spell or ability's controller decides which of those players will make the choice.
    e. Modal spells and abilities may have different targeting requirements for each mode. Changing a spell or ability's target can't change its mode.
    f. A copy of a modal spell or ability copies the mode(s) chosen for it. The controller of the copy can't choose a different mode.

        .. seealso::
            :ref:`Rule 706.9 <copy-spell>`

700.3
-----

Sometimes an effect will cause objects to be temporarily grouped into two or more piles.

    a. Each of the affected objects must be put into exactly one of those piles, unless the effect specifies otherwise.
    b. Each object in a pile is still an individual object. The pile is not an object.
    c. Objects grouped into piles don't leave the zone they're currently in. If cards in a graveyard are split into piles, the order of the graveyard must be maintained.

        .. admonition:: Example

            Fact or Fiction reads, "Reveal the top five cards of your library. An opponent separates those cards into two piles. Put one pile into your hand and the other into your graveyard." While an opponent is separating the revealed cards into piles, they're still in their owner's library. They don't leave the library until they're put into their owner's hand or graveyard.

    d. A pile can contain zero or more objects.

700.4
-----

If a permanent is indestructible, rules and effects can't destroy it.  (See rule 701.6, "Destroy.") Such permanents are not destroyed by lethal damage, and they ignore the lethal-damage state-based action (see rule 704.5g).  Rules or effects may cause an indestructible permanent to be sacrificed, put into a graveyard, or exiled.

    a. Although the text "[This permanent] is indestructible" is an ability, actually being indestructible is neither an ability nor a characteristic. It's just something that's true about a permanent.

700.5
-----

If an attacking creature is unblockable, no creature can legally block it. (See rule 509, 509.) Spells or abilities may still cause it to become blocked.

    a. Although the text "[This permanent] is unblockable" is an ability, actually being unblockable is neither an ability nor a characteristic. It's just something that's true about a creature.

700.6
-----

The term dies means "is put into a graveyard from the battlefield." It is used only when referring to creatures.

.. _keyword-actions:

Keyword Actions
===============

701.1
-----

Most actions described in a card's rules text use the standard English definitions of the verbs within, but some specialized verbs are used whose meanings may not be clear. These "keywords" are game terms; sometimes reminder text summarizes their meanings.

701.2
-----

Activate

    a. To activate an activated ability is to put it onto the stack and pay its costs, so that it will eventually resolve and have its effect. Only an object's controller (or its owner, if it doesn't have a controller) can activate its activated ability unless the object specifically says otherwise. A player may activate an ability if he or she has priority. See rule 602, 602.

701.3
-----

Attach

    a. To attach an Aura, Equipment, or Fortification to an object means to take it from where it currently is and put it onto that object. If something is attached to a permanent on the battlefield, it's customary to place it so that it's physically touching the permanent. An Aura, Equipment, or Fortification can't be attached to an object it couldn't enchant, equip, or fortify, respectively.
    b. If an effect tries to attach an Aura, Equipment, or Fortification to an object it can't be attached to, the Aura, Equipment, or Fortification doesn't move. If an effect tries to attach an Aura, Equipment, or Fortification to the object it's already attached to, the effect does nothing.
    c. Attaching an Aura, Equipment, or Fortification on the battlefield to a different object causes the Aura, Equipment, or Fortification to receive a new timestamp.
    d. To "unattach" an Equipment from a creature means to move it away from that creature so the Equipment is on the battlefield but is not equipping anything. It should no longer be physically touching any creature. If an Aura, Equipment, or Fortification that was attached to something ceases to be attached to it, that counts as "becoming unattached"; this includes if that object and/or that Aura, Equipment, or Fortification leaves the battlefield.

701.4
-----

Cast

    a. To cast a spell is to take it from the zone it's in (usually the hand), put it on the stack, and pay its costs, so that it will eventually resolve and have its effect. A player may cast a spell if he or she has priority. See rule 601, 601.
    b. To cast a card is to cast it as a spell.

701.5
-----

Counter

    a. To counter a spell or ability means to cancel it, removing it from the stack. It doesn't resolve and none of its effects occur. A countered spell is put into its owner's graveyard.
    b. The player who cast a countered spell or activated a countered ability doesn't get a "refund" of any costs that were paid.

701.6
-----

Destroy

    a. To destroy a permanent, move it from the battlefield to its owner's graveyard.
    b. The only ways a permanent can be destroyed are as a result of an effect that uses the word "destroy" or as a result of the state-based actions that check for lethal damage (see rule 704.5g) or damage from a source with deathtouch (see rule 704.5h). If a permanent is put into its owner's graveyard for any other reason, it hasn't been "destroyed."
    c. A regeneration effect replaces a destruction event. See rule 701.11, "Regenerate."

701.7
-----

Discard

    a. To discard a card, move it from its owner's hand to that player's graveyard.
    b. By default, effects that cause a player to discard a card allow the affected player to choose which card to discard. Some effects, however, require a random discard or allow another player to choose which card is discarded.
    c. If a card is discarded, but an effect causes it to be put into a hidden zone instead of into its owner's graveyard without being revealed, all values of that card's characteristics are considered to be undefined. If a card is discarded this way to pay a cost that specifies a characteristic about the discarded card, that cost payment is illegal; the game returns to the moment before the cost was paid (see rule 716, "716").

701.8
-----

Exchange

    a. A spell or ability may instruct players to exchange something (for example, life totals or control of two permanents) as part of its resolution.  When such a spell or ability resolves, if the entire exchange can't be completed, no part of the exchange occurs.

        .. admonition:: Example

            If a spell attempts to exchange control of two target creatures but one of those creatures is destroyed before the spell resolves, the spell does nothing to the other creature.

    b. When control of two permanents is exchanged, if those permanents are controlled by different players, each of those players simultaneously gains control of the permanent that was controlled by the other player. If, on the other hand, those permanents are controlled by the same player, the exchange effect does nothing.
    c. When life totals are exchanged, each player gains or loses the amount of life necessary to equal the other player's previous life total. Replacement effects may modify these gains and losses, and triggered abilities may trigger on them.
    d. Some spells or abilities may instruct a player to exchange cards in one zone with cards in a different zone (for example, exiled cards and cards in a player's hand). These spells and abilities work the same as other "exchange" spells and abilities, except they can exchange the cards only if all the cards are owned by the same player.
    e. If a card in one zone is exchanged with a card in a different zone, and either of them is attached to an object, that card stops being attached to that object and the other card becomes attached to that object.
    f. If a spell or ability instructs a player to simply exchange two zones, and one of the zones is empty, the cards in the zones are still exchanged.

701.9
-----

Exile

    a. To exile an object, move it to the exile zone from wherever it is. See rule 406, 406.

701.10
------

Play

    a. To play a land means to put it onto the battlefield from the zone it's in (usually the hand). A player may play a land if he or she has priority, it's the main phase of his or her turn, the stack is empty, and he or she hasn't yet played a land this turn. Playing a land is a special action (see rule 115), so it doesn't use the stack; it simply happens. Putting a land onto the battlefield as the result of a spell or ability isn't the same as playing a land. See rule 305, "Lands."
    b. To play a card means to play that card as a land or to cast that card as a spell, whichever is appropriate.
    c. Some effects instruct a player to "play" with a certain aspect of the game changed, such as "Play with the top card of your library revealed." "Play" in this sense means to play the *Magic* game.
    d. Previously, the action of casting a spell, or casting a card as a spell, was referred to on cards as "playing" that spell or that card. Cards that were printed with that text have received errata in the Oracle card reference so they now refer to "casting" that spell or that card.
    e. Previously, the action of using an activated ability was referred to on cards as "playing" that ability. Cards that were printed with that text have received errata in the Oracle card reference so they now refer to "activating" that ability.

701.11
------

Regenerate

    a. If the effect of a resolving spell or ability regenerates a permanent, it creates a replacement effect that protects the permanent the next time it would be destroyed this turn. In this case, "Regenerate [permanent]" means "The next time [permanent] would be destroyed this turn, instead remove all damage marked on it and tap it. If it's an attacking or blocking creature, remove it from combat."
    b. If the effect of a static ability regenerates a permanent, it replaces destruction with an alternate effect each time that permanent would be destroyed. In this case, "Regenerate [permanent]" means "Instead remove all damage marked on [permanent] and tap it. If it's an attacking or blocking creature, remove it from combat."
    c. Neither activating an ability that creates a regeneration shield nor casting a spell that creates a regeneration shield is the same as regenerating a permanent. Effects that say that a permanent can't be regenerated don't prevent such abilities from being activated or such spells from being cast; rather, they prevent regeneration shields from having any effect.

701.12
------

Reveal

    a. To reveal a card, show that card to all players for a brief time. If an effect causes a card to be revealed, it remains revealed for as long as necessary to complete the parts of the effect that card is relevant to. If the cost to cast a spell or activate an ability includes revealing a card, the card remains revealed from the time the spell or ability is announced until it the time it leaves the stack.
    b. Revealing a card doesn't cause it to leave the zone it's in.

701.13
------

Sacrifice

    a. To sacrifice a permanent, its controller moves it from the battlefield directly to its owner's graveyard. A player can't sacrifice something that isn't a permanent, or something that's a permanent he or she doesn't control.  Sacrificing a permanent doesn't destroy it, so regeneration or other effects that replace destruction can't affect this action.

701.14
------

Search

    a. To search for a card in a zone, look at all cards in that zone (even if it's a hidden zone) and find a card that matches the given description.
    b. If a player is searching a hidden zone for cards with a stated quality, such as a card with a certain card type or color, that player isn't required to find some or all of those cards even if they're present in that zone.

        .. admonition:: Example

            Splinter says "Exile target artifact. Search its controller's graveyard, hand, and library for all cards with the same name as that artifact and exile them.  That player then shuffles his or her library." A player casts Splinter targeting Howling Mine (an artifact). Howling Mine's controller has another Howling Mine in her graveyard and two more in her library. Splinter's controller must find the Howling Mine in the graveyard, but may choose to find zero, one, or two of the Howling Mines in the library.

    c. If a player is searching a hidden zone simply for a quantity of cards, such as "a card" or "three cards," that player must find that many cards (or as many as possible, if the zone doesn't contain enough cards).
    d. If the effect that contains the search instruction doesn't also contain instructions to reveal the found card(s), then they're not revealed.

701.15
------

Shuffle

    a. To shuffle a library or a face-down pile of cards, randomize the cards within it so that no player knows their order.
    b. Some effects cause a player to search a library for a card or cards, shuffle that library, then put the found card or cards in a certain position in that library. Even though the found card or cards never leave that library, they aren't included in the shuffle. Rather, all the cards in that library except those are shuffled. Abilities that trigger when a library is shuffled will still trigger.
    c. If an effect would cause a player to shuffle one or more specific objects into a library, but none of those objects are in the zone they're expected to be in, that library is not shuffled.

        .. admonition:: Example

            Guile says, in part, "When Guile is put into a graveyard from anywhere, shuffle it into its owner's library." It's put into a graveyard and its ability triggers, then a player exiles it from that graveyard in response. When the ability resolves, nothing happens.

    d. If an effect would cause a player to shuffle one or more specific objects into a library, and a replacement or prevention effect causes all such objects to be moved to another zone instead, that library isn't shuffled.

        .. admonition:: Example

            Black Sun's Zenith says, in part, "Shuffle Black Sun's Zenith into its owner's library." Black Sun's Zenith is in a graveyard, has gained flashback (due to Recoup, perhaps), and is cast from that graveyard. Black Sun's Zenith will be exiled, and its owner's library won't be shuffled.

    e. If an effect would cause a player to shuffle a set of objects into a library, that library is shuffled even if there are no objects in that set.

        .. admonition:: Example

            Loaming Shaman says "When Loaming Shaman enters the battlefield, target player shuffles any number of target cards from his or her graveyard into his or her library." It enters the battlefield, its ability triggers, and no cards are targeted. When the ability resolves, the targeted player will still have to shuffle his or her library.

    f. If an effect causes a player to shuffle a library containing zero or one cards, abilities that trigger when a library is shuffled will still trigger.
    g. If two or more effects cause a library to be shuffled multiple times simultaneously, abilities that trigger when that library is shuffled will trigger that many times.

701.16
------

Tap and Untap

    a. To tap a permanent, turn it sideways from an upright position. Only untapped permanents can be tapped.
    b. To untap a permanent, rotate it back to the upright position from a sideways position. Only tapped permanents can be untapped.

701.17
------

Scry

    a. To "scry N" means to look at the top N cards of your library, put any number of them on the bottom of your library in any order, and put the rest on top of your library in any order.

701.18
------

Fateseal

    a. To "fateseal N" means to look at the top N cards of an opponent's library, put any number of them on the bottom of that library in any order, and put the rest on top of that library in any order.

701.19
------

Clash

    a. To clash, a player reveals the top card of his or her library. That player may then put that card on the bottom of his or her library.
    b. "Clash with an opponent" means "Choose an opponent. You and that opponent each clash."
    c. A player wins a clash if that player revealed a card with a higher converted mana cost than all other cards revealed in that clash.

701.20
------

.. _planeswalk:

Planeswalk

    a. A player may planeswalk only during a Planechase game. Only the planar controller may planeswalk. See rule 901, 901.
    b. To planeswalk is to put the face-up plane card on the bottom of its owner's planar deck face down, then move the top card of your planar deck off that planar deck and turn it face up.
    c. A player may planeswalk as the result of the "planeswalking ability" (see rule 309.6) or because the owner of the face-up plane card leaves the game (see rule 901.9).
    d. The plane card that's turned face up is the plane the player planeswalks to. The plane card that's turned face down, or that leaves the game, is the plane the player planeswalks away from.

.. _set-in-motion:

701.21
------

Set in Motion

    a. Only a scheme card may be set in motion, and only during an Archenemy game. Only the archenemy may set a scheme card in motion. See rule 311, 311. and rule 904, "Archenemy."
    b. To set a scheme in motion, move it off the top of your scheme deck and turn it face up.

701.22
------

.. _abandon:

Abandon

    a. Only a face-up ongoing scheme card may be abandoned, and only during an Archenemy game. See rule 311, 311. and rule 904, "Archenemy."
    b. To abandon a scheme, turn it face down and put it on the bottom of its owner's scheme deck.

701.23
------

Proliferate

    a. To proliferate means to choose any number of permanents and/or players that have a counter, then give each exactly one additional counter of a kind that permanent or player already has.
    b. If a permanent or player chosen this way has more than one kind of counter, the player who is proliferating chooses which kind of counter to add.
    c. To proliferate in a Two-Headed Giant game means to choose any number of permanents and/or teams that have a counter, then give each exactly one additional counter of a kind that permanent or team already has. See rule 810, 810.

.. _keyword-abilities:

Keyword Abilities
=================

702.1
-----

Most abilities describe exactly what they do in the card's rules text.  Some, though, are very common or would require too much space to define on the card. In these cases, the object lists only the name of the ability as a "keyword"; sometimes reminder text summarizes the game rule.

702.2
-----

Deathtouch

    a. Deathtouch is a static ability.
    b. Any nonzero amount of combat damage assigned to a creature by a source with deathtouch is considered to be lethal damage, regardless of that creature's toughness. See rules 510.1c-d.
    c. A creature with toughness greater than 0 that's been dealt damage by a source with deathtouch since the last time state-based actions were checked is destroyed as a state-based action. See rule 704.
    d. The deathtouch rules function no matter what zone an object with deathtouch deals damage from.
    e. If an object changes zones before an effect causes it to deal damage, its last known information is used to determine whether it had deathtouch.
    f. Multiple instances of deathtouch on the same object are redundant.

702.3
-----

Defender

    a. Defender is a static ability.
    b. A creature with defender can't attack.
    c. Multiple instances of defender on the same creature are redundant.

702.4
-----

Double Strike

    a. Double strike is a static ability that modifies the rules for the combat damage step. (See rule 510, 510.)
    b. If at least one attacking or blocking creature has first strike (see rule 702.7) or double strike as the combat damage step begins, the only creatures that assign combat damage in that step are those with first strike or double strike. After that step, instead of proceeding to the end of combat step, the phase gets a second combat damage step. The only creatures that assign combat damage in that step are the remaining attackers and blockers that had neither first strike nor double strike as the first combat damage step began, as well as the remaining attackers and blockers that currently have double strike. After that step, the phase proceeds to the end of combat step.
    c. Removing double strike from a creature during the first combat damage step will stop it from assigning combat damage in the second combat damage step.
    d. Giving double strike to a creature with first strike after it has already dealt combat damage in the first combat damage step will allow the creature to assign combat damage in the second combat damage step.
    e. Multiple instances of double strike on the same creature are redundant.

702.5
-----

Enchant

    a. Enchant is a static ability, written "Enchant [object or player]." The enchant ability restricts what an Aura spell can target and what an Aura can enchant.
    b. For more information on Auras, see rule 303, 303.
    c. If an Aura has multiple instances of enchant, all of them apply. The Aura's target must follow the restrictions from all the instances of enchant.  The Aura can enchant only objects or players that match all of its enchant abilities.
    d. Auras that can enchant a player can target and be attached to players.  Such Auras can't target permanents and can't be attached to permanents.

702.6
-----

Equip

    a. Equip is an activated ability of Equipment cards. "Equip [cost]" means "[Cost]: Attach this permanent to target creature you control. Activate this ability only any time you could cast a sorcery."
    b. For more information about Equipment, see rule 301, 301.
    c. If a permanent has multiple instances of equip, any of its equip abilities may be activated.

702.7
-----

First Strike

    a. First strike is a static ability that modifies the rules for the combat damage step. (See rule 510, 510.)
    b. If at least one attacking or blocking creature has first strike or double strike (see rule 702.4) as the combat damage step begins, the only creatures that assign combat damage in that step are those with first strike or double strike. After that step, instead of proceeding to the end of combat step, the phase gets a second combat damage step. The only creatures that assign combat damage in that step are the remaining attackers and blockers that had neither first strike nor double strike as the first combat damage step began, as well as the remaining attackers and blockers that currently have double strike. After that step, the phase proceeds to the end of combat step.
    c. Giving first strike to a creature without it after combat damage has already been dealt in the first combat damage step won't prevent that creature from assigning combat damage in the second combat damage step. Removing first strike from a creature after it has already dealt combat damage in the first combat damage step won't allow it to also assign combat damage in the second combat damage step (unless the creature has double strike).
    d. Multiple instances of first strike on the same creature are redundant.

702.8
-----

Flash

    a. Flash is a static ability that functions in any zone from which you could play the card it's on. "Flash" means "You may play this card any time you could cast an instant."
    b. Multiple instances of flash on the same object are redundant.

702.9
-----

Flying

    a. Flying is an evasion ability.
    b. A creature with flying can't be blocked except by creatures with flying and/or reach. A creature with flying can block a creature with or without flying. (See rule 509, 509. and rule 702.16, "Reach.")
    c. Multiple instances of flying on the same creature are redundant.

702.10
------

Haste

    a. Haste is a static ability.
    b. If a creature has haste, it can attack even if it hasn't been controlled by its controller continuously since his or her most recent turn began. (See rule 302.6.)
    c. If a creature has haste, its controller can activate its activated abilities whose cost includes the tap symbol or the untap symbol even if that creature hasn't been controlled by that player continuously since his or her most recent turn began. (See rule 302.6.)
    d. Multiple instances of haste on the same creature are redundant.

702.11
------

Hexproof

    a. Hexproof is a static ability.
    b. "Hexproof" on a permanent means "This permanent can't be the target of spells or abilities your opponents control."
    c. "Hexproof" on a player means "You can't be the target of spells or abilities your opponents control."
    d. Multiple instances of hexproof on the same permanent or player are redundant.

702.12
------

Intimidate

    a. Intimidate is an evasion ability.
    b. A creature with intimidate can't be blocked except by artifact creatures and/or creatures that share a color with it. (See rule 509, 509.)
    c. Multiple instances of intimidate on the same creature are redundant.

702.13
------

Landwalk

    a. Landwalk is a generic term that appears within an object's rules text as "[type]walk," where [type] is usually a subtype, but can be the card type land, any land type, any supertype, or any combination thereof.
    b. Landwalk is an evasion ability.
    c. A creature with landwalk is unblockable as long as the defending player controls at least one land with the specified subtype (as in "islandwalk"), with the specified supertype (as in "legendary landwalk"), without the specified supertype (as in "nonbasic landwalk"), or with both the specified supertype and the specified subtype (as in "snow swampwalk"). (See rule 509, 509.)
    d. Landwalk abilities don't "cancel" one another.

        .. admonition:: Example

            If a player controls a snow Forest, that player can't block an attacking creature with snow forestwalk even if he or she also controls a creature with snow forestwalk.

    e. Multiple instances of the same kind of landwalk on the same creature are redundant.

702.14
------

Lifelink

    a. Lifelink is a static ability.
    b. Damage dealt by a source with lifelink causes that source's controller, or its owner if it has no controller, to gain that much life (in addition to any other results that damage causes). See rule 119.3.
    c. If a permanent leaves the battlefield before an effect causes it to deal damage, its last known information is used to determine whether it had lifelink.
    d. The lifelink rules function no matter what zone an object with lifelink deals damage from.
    e. Multiple instances of lifelink on the same object are redundant.

702.15
------

Protection

    a. Protection is a static ability, written "Protection from [quality]." This quality is usually a color (as in "protection from black") but can be any characteristic value. If the quality happens to be a card name, it is treated as such only if the protection ability specifies that the quality is a name. If the quality is a card type, subtype, or supertype, the ability applies to sources that are permanents with that card type, subtype, or supertype and to any sources not on the battlefield that are of that card type, subtype, or supertype. This is an exception to rule 109.2.
    b. A permanent or player with protection can't be targeted by spells with the stated quality and can't be targeted by abilities from a source with the stated quality.
    c. A permanent or player with protection can't be enchanted by Auras that have the stated quality. Such Auras attached to the permanent or player with protection will be put into their owners' graveyards as a state-based action.  (See rule 704, 704.)
    d. A permanent with protection can't be equipped by Equipment that have the stated quality or fortified by Fortifications that have the stated quality.  Such Equipment or Fortifications become unattached from that permanent as a state-based action, but remain on the battlefield. (See rule 704, 704.)
    e. Any damage that would be dealt by sources that have the stated quality to a permanent or player with protection is prevented.
    f. Attacking creatures with protection can't be blocked by creatures that have the stated quality.
    g. "Protection from [quality A] and from [quality B]" is shorthand for "protection from [quality A]" and "protection from [quality B]"; it behaves as two separate protection abilities. If an effect causes an object with such an ability to lose protection from [quality A], for example, that object would still have protection from [quality B].
    h. "Protection from all [characteristic]" is shorthand for "protection from [quality A]," "protection from [quality B]," and so on for each possible quality the listed characteristic could have; it behaves as multiple separate protection abilities. If an effect causes an object with such an ability to lose protection from [quality A], for example, that object would still have protection from [quality B], [quality C], and so on.
    i. "Protection from everything" is a variant of the protection ability. A permanent with protection from everything has protection from each object regardless of that object's characteristic values. Such a permanent can't be targeted by spells or abilities, enchanted by Auras, equipped by Equipment, fortified by Fortifications, or blocked by creatures, and all damage that would be dealt to it is prevented.
    j. Multiple instances of protection from the same quality on the same permanent or player are redundant.

702.16
------

Reach

    a. Reach is a static ability.
    b. A creature with flying can't be blocked except by creatures with flying and/or reach. (See rule 509, 509. and rule 702.9, "Flying.")
    c. Multiple instances of reach on the same creature are redundant.

702.17
------

Shroud

    a. Shroud is a static ability. "Shroud" means "This permanent or player can't be the target of spells or abilities."
    b. Multiple instances of shroud on the same permanent or player are redundant.

702.18
------

Trample

    a. Trample is a static ability that modifies the rules for assigning an attacking creature's combat damage. The ability has no effect when a creature with trample is blocking or is dealing noncombat damage. (See rule 510, 510.)
    b. The controller of an attacking creature with trample first assigns damage to the creature(s) blocking it. Once all those blocking creatures are assigned lethal damage, any remaining damage is assigned as its controller chooses among those blocking creatures and the player or planeswalker the creature is attacking. When checking for assigned lethal damage, take into account damage already marked on the creature and damage from other creatures that's being assigned during the same combat damage step, but not any abilities or effects that might change the amount of damage that's actually dealt. The attacking creature's controller need not assign lethal damage to all those blocking creatures but in that case can't assign any damage to the player or planeswalker it's attacking.

        .. admonition:: Example

            A 2/2 creature with an ability that enables it to block multiple attackers blocks two attackers: a 1/1 with no abilities a 3/3 with trample. The active player could assign 1 damage from the first attacker and 1 damage from the second to the blocking creature, and 2 damage to the defending player from the creature with trample.

        .. admonition:: Example

            A 6/6 green creature with trample is blocked by a 2/2 creature with protection from green. The attacking creature's controller must assign at least 2 damage to the blocker, even though that damage will be prevented by the blocker's protection ability. The attacking creature's controller can divide the rest of the damage as he or she chooses between the blocking creature and the defending player.

    c. If an attacking creature with trample is blocked, but there are no creatures blocking it when damage is assigned, all its damage is assigned to the player or planeswalker it's attacking.
    d. If a creature with trample is attacking a planeswalker, none of its combat damage can be assigned to the defending player, even if that planeswalker has been removed from combat or the damage the attacking creature could assign is greater than the planeswalker's loyalty.
    e. Multiple instances of trample on the same creature are redundant.

702.19
------

Vigilance

    a. Vigilance is a static ability that modifies the rules for the declare attackers step.
    b. Attacking doesn't cause creatures with vigilance to tap. (See rule 508, 508.)
    c. Multiple instances of vigilance on the same creature are redundant.

702.20
------

.. _banding:

Banding

    a. Banding is a static ability that modifies the rules for combat.
    b. "Bands with other" is a special form of banding. If an effect causes a permanent to lose banding, the permanent loses all "bands with other" abilities as well.
    c. As a player declares attackers, he or she may declare that one or more attacking creatures with banding and up to one attacking creature without banding (even if it has "bands with other") are all in a "band." He or she may also declare that one or more attacking [quality] creatures with "bands with other [quality]" and any number of other attacking [quality] creatures are all in a band. A player may declare as many attacking bands as he or she wants, but each creature may be a member of only one of them. (Defending players can't declare bands but may use banding in a different way; see rule 702.20j.)
    d. All creatures in an attacking band must attack the same player or planeswalker.
    e. Once an attacking band has been announced, it lasts for the rest of combat, even if something later removes banding or "bands with other" from one or more of the creatures in the band.
    f. An attacking creature that's removed from combat is also removed from the band it was in.
    g. Banding doesn't cause attacking creatures to share abilities, nor does it remove any abilities. The attacking creatures in a band are separate permanents.
    h. If an attacking creature becomes blocked by a creature, each other creature in the same band as the attacking creature becomes blocked by that same blocking creature.

        .. admonition:: Example

            A player attacks with a band consisting of a creature with flying and a creature with swampwalk. The defending player, who controls a Swamp, can block the flying creature if able. If he or she does, then the creature with swampwalk will also become blocked by the blocking creature(s).

    i. If one member of a band would become blocked due to an effect, the entire band becomes blocked.
    j. During the combat damage step, if an attacking creature is being blocked by a creature with banding, or by both a [quality] creature with "bands with other [quality]" and another [quality] creature, the defending player (rather than the active player) chooses how the attacking creature's damage is assigned. That player can divide that creature's combat damage as he or she chooses among any number of creatures blocking it. This is an exception to the procedure described in rule 510.1c.
    k. During the combat damage step, if a blocking creature is blocking a creature with banding, or both a [quality] creature with "bands with other [quality]" and another [quality] creature, the active player (rather than the defending player) chooses how the blocking creature's damage is assigned. That player can divide that creature's combat damage as he or she chooses among any number of creatures it's blocking. This is an exception to the procedure described in rule 510.1d.

    m. Multiple instances of banding on the same creature are redundant.  Multiple instances of "bands with other" of the same kind on the same creature are redundant.

702.21
------

Rampage

    a. Rampage is a triggered ability. "Rampage N" means "Whenever this creature becomes blocked, it gets +N/+N until end of turn for each creature blocking it beyond the first." (See rule 509, 509.)
    b. The rampage bonus is calculated only once per combat, when the triggered ability resolves. Adding or removing blockers later in combat won't change the bonus.
    c. If a creature has multiple instances of rampage, each triggers separately.

702.22
------

Cumulative Upkeep

    a. Cumulative upkeep is a triggered ability that imposes an increasing cost on a permanent. "Cumulative upkeep [cost]" means "At the beginning of your upkeep, if this permanent is on the battlefield, put an age counter on this permanent. Then you may pay [cost] for each age counter on it. If you don't, sacrifice it." If [cost] has choices associated with it, each choice is made separately for each age counter, then either the entire set of costs is paid, or none of them is paid. Partial payments aren't allowed.

        .. admonition:: Example

            A creature has "Cumulative upkeep |W| or |U|" and two age counters on it. When its ability next triggers and resolves, the creature's controller puts an age counter on it and then may pay |W|\ |W|\ |W|, |W|\ |W|\ |U|, |W|\ |U|\ |U|, or |U|\ |U|\ |U| to keep the creature on the battlefield.

        .. admonition:: Example

            A creature has "Cumulative upkeep -- Sacrifice a creature" and one age counter on it. When its ability next triggers and resolves, its controller can't choose the same creature to sacrifice twice.  Either two different creatures must be sacrificed, or the creature with cumulative upkeep must be sacrificed.

    b. If a permanent has multiple instances of cumulative upkeep, each triggers separately. However, the age counters are not connected to any particular ability; each cumulative upkeep ability will count the total number of age counters on the permanent at the time that ability resolves.

        .. admonition:: Example

            A creature has two instances of "Cumulative upkeep -- Pay 1 life." The creature currently has no counters but both cumulative upkeep abilities trigger. When the first ability resolves, the controller adds a counter and then chooses to pay 1 life. When the second ability resolves, the controller adds another counter and then chooses to pay an additional 2 life.

702.23
------

Flanking

    a. Flanking is a triggered ability that triggers during the declare blockers step. (See rule 509, 509.) "Flanking" means "Whenever this creature becomes blocked by a creature without flanking, the blocking creature gets -1/-1 until end of turn."
    b. If a creature has multiple instances of flanking, each triggers separately.

702.24
------

Phasing

    a. Phasing is a static ability that modifies the rules of the untap step.  During each player's untap step, before the active player untaps his or her permanents, all phased-in permanents with phasing that player controls "phase out." Simultaneously, all phased-out permanents that had phased out under that player's control "phase in."
    b. If a permanent phases out, its status changes to "phased out." Except for rules and effects that specifically mention phased-out permanents, a phased-out permanent is treated as though it does not exist. It can't affect or be affected by anything else in the game.

        .. admonition:: Example

            You control three creatures, one of which is phased out. You cast a spell that says "Draw a card for each creature you control." You draw two cards.

        .. admonition:: Example

            You control a phased-out creature. You cast Wrath of God, which says "Destroy all creatures.  They can't be regenerated." The phased-out creature is not destroyed.

    c. If a permanent phases in, its status changes to "phased in." The game once again treats it as though it exists.
    d. The phasing event doesn't actually cause a permanent to change zones or control, even though it's treated as though it's not on the battlefield and not under its controller's control while it's phased out. Zone-change triggers don't trigger when a permanent phases in or out. Counters remain on a permanent while it's phased out. Effects that check a phased-in permanent's history won't treat the phasing event as having caused the permanent to leave or enter the battlefield or its controller's control.
    e. Continuous effects that affect a phased-out permanent may expire while that permanent is phased out. If so, they will no longer affect that permanent once it's phased in. In particular, effects with "for as long as" durations that track that permanent (see rule 611.2b) end when that permanent phases out because they can no longer see it.
    f. When a permanent phases out, any Auras, Equipment, or Fortifications attached to that permanent phase out at the same time. This alternate way of phasing out is known as phasing out "indirectly." An Aura, Equipment, or Fortification that phased out indirectly won't phase in by itself, but instead phases in along with the permanent it's attached to.
    g. If an object would simultaneously phase out directly and indirectly, it just phases out indirectly.
    h. An Aura, Equipment, or Fortification that phased out directly will phase in attached to the object or player it was attached to when it phased out, if that object is still in the same zone or that player is still in the game. If not, that Aura, Equipment, or Fortification phases in unattached.  State-based actions apply as appropriate. (See rules 704.5n and 704.5p.)
    i. Abilities that trigger when a permanent becomes attached or unattached from an object or player don't trigger when that permanent phases in or out.
    j. Phased-out permanents owned by a player who leaves the game also leave the game. This doesn't trigger zone-change triggers. See rule 800.4.
    k. Phased-out tokens cease to exist as a state-based action. See rule 704.5d.

    m. If an effect causes a player to skip his or her untap step, the phasing event simply doesn't occur that turn.
    n. Multiple instances of phasing on the same permanent are redundant.

702.25
------

Buyback

    a. Buyback appears on some instants and sorceries. It represents two static abilities that function while the spell is on the stack. "Buyback [cost]" means "You may pay an additional [cost] as you cast this spell" and "If the buyback cost was paid, put this spell into its owner's hand instead of into that player's graveyard as it resolves." Paying a spell's buyback cost follows the rules for paying additional costs in rules 601.2b and 601.2e-g.

702.26
------

Shadow

    a. Shadow is an evasion ability.
    b. A creature with shadow can't be blocked by creatures without shadow, and a creature without shadow can't be blocked by creatures with shadow. (See rule 509, 509.)
    c. Multiple instances of shadow on the same creature are redundant.

702.27
------

Cycling

    a. Cycling is an activated ability that functions only while the card with cycling is in a player's hand. "Cycling [cost]" means "[Cost], Discard this card: Draw a card."
    b. Although the cycling ability can be activated only if the card is in a player's hand, it continues to exist while the object is on the battlefield and in all other zones. Therefore objects with cycling will be affected by effects that depend on objects having one or more activated abilities.
    c. Some cards with cycling have abilities that trigger when they're cycled. "When you cycle [this card]" means "When you discard [this card] to pay a cycling cost." These abilities trigger from whatever zone the card winds up in after it's cycled.
    d. Typecycling is a variant of the cycling ability. "[Type]cycling [cost]" means "[Cost], Discard this card: Search your library for a [type] card, reveal it, and put it into your hand. Then shuffle your library." This type is usually a subtype (as in "mountaincycling") but can be any card type, subtype, supertype, or combination thereof (as in "basic landcycling").
    e. Typecycling abilities are cycling abilities, and typecycling costs are cycling costs. Any cards that trigger when a player cycles a card will trigger when a card is discarded to pay a typecycling cost. Any effect that stops players from cycling cards will stop players from activating cards' typecycling abilities. Any effect that increases or reduces a cycling cost will increase or reduce a typecycling cost.

702.28
------

Echo

    a. Echo is a triggered ability. "Echo [cost]" means "At the beginning of your upkeep, if this permanent came under your control since the beginning of your last upkeep, sacrifice it unless you pay [cost]."
    b. Urza block cards with the echo ability were printed without an echo cost. These cards have been given errata in the Oracle card reference; each one now has an echo cost equal to its mana cost.

702.29
------

Horsemanship

    a. Horsemanship is an evasion ability.
    b. A creature with horsemanship can't be blocked by creatures without horsemanship. A creature with horsemanship can block a creature with or without horsemanship. (See rule 509, 509.)
    c. Multiple instances of horsemanship on the same creature are redundant.

702.30
------

Fading

    a. Fading is a keyword that represents two abilities. "Fading N" means "This permanent enters the battlefield with N fade counters on it" and "At the beginning of your upkeep, remove a fade counter from this permanent. If you can't, sacrifice the permanent."

702.31
------

Kicker

    a. Kicker is a static ability that functions while the spell with kicker is on the stack. "Kicker [cost]" means "You may pay an additional [cost] as you cast this spell." Paying a spell's kicker cost(s) follows the rules for paying additional costs in rules 601.2b and 601.2e-g.
    b. The phrase "Kicker [cost 1] and/or [cost 2]" means the same thing as "Kicker [cost 1], kicker [cost 2]."
    c. Multikicker is a variant of the kicker ability. "Multikicker [cost]" means "You may pay an additional [cost] any number of times as you cast this spell." A multikicker cost is a kicker cost.
    d. If a spell's controller declares the intention to pay any of that spell's kicker costs, that spell has been "kicked." If a spell has two kicker costs or has multikicker, it may be kicked multiple times. See rule 601.2b.
    e. Objects with kicker or multikicker have additional abilities that specify what happens if they are kicked. These abilities are linked to the kicker or multikicker abilities printed on that object: they can refer only to those specific kicker or multikicker abilities. See rule 607, 607.
    f. Objects with more than one kicker cost have abilities that each correspond to a specific kicker cost. They contain the phrases "if it was kicked with its [A] kicker" and "if it was kicked with its [B] kicker," where A and B are the first and second kicker costs listed on the card, respectively.  Each of those abilities is linked to the appropriate kicker ability.
    g. If part of a spell's ability has its effect only if that spell was kicked, and that part of the ability includes any targets, the spell's controller chooses those targets only if that spell was kicked. Otherwise, the spell is cast as if it did not have those targets. See rule 601.2c.

702.32
------

Flashback

    a. Flashback appears on some instants and sorceries. It represents two static abilities: one that functions while the card is in a player's graveyard and the other that functions while the card is on the stack. "Flashback [cost]" means "You may cast this card from your graveyard by paying [cost] rather than paying its mana cost" and "If the flashback cost was paid, exile this card instead of putting it anywhere else any time it would leave the stack." Casting a spell using its flashback ability follows the rules for paying alternative costs in rules 601.2b and 601.2e-g.

702.33
------

Madness

    a. Madness is a keyword that represents two abilities. The first is a static ability that functions while the card with madness is in a player's hand. The second is a triggered ability that functions when the first ability is applied. "Madness [cost]" means "If a player would discard this card, that player discards it, but may exile it instead of putting it into his or her graveyard" and "When this card is exiled this way, its owner may cast it by paying [cost] rather than paying its mana cost. If that player doesn't, he or she puts this card into his or her graveyard."
    b. Casting a spell using its madness ability follows the rules for paying alternative costs in rules 601.2b and 601.2e-g.

702.34
------

Fear

    a. Fear is an evasion ability.
    b. A creature with fear can't be blocked except by artifact creatures and/or black creatures. (See rule 509, 509.)
    c. Multiple instances of fear on the same creature are redundant.

702.35
------

Morph

    a. Morph is a static ability that functions in any zone from which you could play the card it's on, and the morph effect works any time the card is face down. "Morph [cost]" means "You may cast this card as a 2/2 face-down creature, with no text, no name, no subtypes, no expansion symbol, and no mana cost by paying |3| rather than paying its mana cost." (See rule 707, 707.)
    b. To cast a card using its morph ability, turn it face down. It becomes a 2/2 face-down creature card, with no text, no name, no subtypes, no expansion symbol, and no mana cost. Any effects or prohibitions that would apply to casting a card with these characteristics (and not the face-up card's characteristics) are applied to casting this card. These values are the copiable values of that object's characteristics. (See rule 613, 613. and rule 706, "Copying Objects.") Put it onto the stack (as a face-down spell with the same characteristics), and pay |3| rather than pay its mana cost. This follows the rules for paying alternative costs. You can use morph to cast a card from any zone from which you could normally play it.  When the spell resolves, it enters the battlefield with the same characteristics the spell had. The morph effect applies to the face-down object wherever it is, and it ends when the permanent is turned face up.
    c. You can't cast a card face down if it doesn't have morph.
    d. If you have priority, you may turn a face-down permanent you control face up. This is a special action; it doesn't use the stack (see rule 115). To do this, show all players what the permanent's morph cost would be if it were face up, pay that cost, then turn the permanent face up. (If the permanent wouldn't have a morph cost if it were face up, it can't be turned face up this way.) The morph effect on it ends, and it regains its normal characteristics.  Any abilities relating to the permanent entering the battlefield don't trigger when it's turned face up and don't have any effect, because the permanent has already entered the battlefield.
    e. See rule 707, 707. for more information on how to cast cards with morph.

702.36
------

Amplify

    a. Amplify is a static ability. "Amplify N" means "As this object enters the battlefield, reveal any number of cards from your hand that share a creature type with it. This permanent enters the battlefield with N +1/+1 counters on it for each card revealed this way. You can't reveal this card or any other cards that are entering the battlefield at the same time as this card."
    b. If a creature has multiple instances of amplify, each one works separately.

702.37
------

Provoke

    a. Provoke is a triggered ability. "Provoke" means "Whenever this creature attacks, you may choose to have target creature defending player controls block this creature this combat if able. If you do, untap that creature."
    b. If a creature has multiple instances of provoke, each triggers separately.

702.38
------

Storm

    a. Storm is a triggered ability that functions on the stack. "Storm" means "When you cast this spell, put a copy of it onto the stack for each other spell that was cast before it this turn. If the spell has any targets, you may choose new targets for any of the copies."
    b. If a spell has multiple instances of storm, each triggers separately.

702.39
------

Affinity

    a. Affinity is a static ability that functions while the spell is on the stack. "Affinity for [text]" means "This spell costs you |1| less to cast for each [text] you control."
    b. The affinity ability reduces only the amount of generic mana a spell's controller has to pay; it doesn't reduce how much colored mana that player has to pay.
    c. If a spell has multiple instances of affinity, each of them applies.

702.40
------

Entwine

    a. Entwine is a static ability of modal spells (see rule 700.2) that functions while the spell is on the stack. "Entwine [cost]" means "You may choose all modes of this spell instead of just one. If you do, you pay an additional [cost]." Using the entwine ability follows the rules for choosing modes and paying additional costs in rules 601.2b and 601.2e-g.
    b. If the entwine cost was paid, follow the text of each of the modes in the order written on the card when the spell resolves.

702.41
------

Modular

    a. Modular represents both a static ability and a triggered ability.  "Modular N" means "This permanent enters the battlefield with N +1/+1 counters on it" and "When this permanent is put into a graveyard from the battlefield, you may put a +1/+1 counter on target artifact creature for each +1/+1 counter on this permanent."
    b. If a creature has multiple instances of modular, each one works separately.

702.42
------

Sunburst

    a. Sunburst is a static ability that functions as an object is entering the battlefield from the stack. "Sunburst" means "If this object is entering the battlefield from the stack as a creature, it enters the battlefield with a +1/+1 counter on it for each color of mana spent to cast it. If this object is entering the battlefield from the stack and isn't entering the battlefield as a creature, it enters the battlefield with a charge counter on it for each color of mana spent to cast it."
    b. Sunburst applies only as the spell is resolving and only if one or more colored mana was spent on its costs. Mana paid for additional or alternative costs applies.
    c. Sunburst can also be used to set a variable number for another ability.  If the keyword is used in this way, it doesn't matter whether the ability is on a creature spell or on a noncreature spell.

        .. admonition:: Example

            The ability "Modular -- Sunburst" means "This permanent enters the battlefield with a +1/+1 counter on it for each color of mana spent to cast it" and "When this permanent is put into a graveyard from the battlefield, you may put a +1/+1 counter on target artifact creature for each +1/+1 counter on this permanent."

    d. If an object has multiple instances of sunburst, each one works separately.

702.43
------

Bushido

    a. Bushido is a triggered ability. "Bushido N" means "Whenever this creature blocks or becomes blocked, it gets +N/+N until end of turn." (See rule 509, 509.)
    b. If a creature has multiple instances of bushido, each triggers separately.

702.44
------

Soulshift

    a. Soulshift is a triggered ability. "Soulshift N" means "When this permanent is put into a graveyard from the battlefield, you may return target Spirit card with converted mana cost N or less from your graveyard to your hand."
    b. If a permanent has multiple instances of soulshift, each triggers separately.

702.45
------

Splice

    a. Splice is a static ability that functions while a card is in your hand.  "Splice onto [subtype] [cost]" means "You may reveal this card from your hand as you cast a [subtype] spell. If you do, copy this card's text box onto that spell and pay [cost] as an additional cost to cast that spell." Paying a card's splice cost follows the rules for paying additional costs in rules 601.2b and 601.2e-g.

        .. admonition:: Example

            Since the card with splice remains in the player's hand, it can later be cast normally or spliced onto another spell. It can even be discarded to pay a "discard a card" cost of the spell it's spliced onto.

    b. You can't choose to use a splice ability if you can't make the required choices (targets, etc.) for that card's instructions. You can't splice any one card onto the same spell more than once. If you're splicing more than one card onto a spell, reveal them all at once and choose the order in which their instructions will be followed. The instructions on the main spell have to be followed first.
    c. The spell has the characteristics of the main spell, plus the text boxes of each of the spliced cards. The spell doesn't gain any other characteristics (name, mana cost, color, supertypes, card types, subtypes, etc.) of the spliced cards. Text copied onto the spell that refers to a card by name refers to the spell on the stack, not the card from which the text was copied.

        .. admonition:: Example

            Glacial Ray is a red card with splice onto Arcane that reads, "Glacial Ray deals 2 damage to target creature or player." Suppose Glacial Ray is spliced onto Reach Through Mists, a blue spell. The spell is still blue, and Reach Through Mists deals the damage. This means that the ability can target a creature with protection from red and deal 2 damage to that creature.

    d. Choose targets for the added text normally (see rule 601.2c). Note that a spell with one or more targets will be countered if all of its targets are illegal on resolution.
    e. The spell loses any splice changes once it leaves the stack (for example, when it's countered, it's exiled, or it resolves).

702.46
------

Offering

    a. Offering is a static ability of a card that functions in any zone from which the card can be cast. "[Subtype] offering" means "You may cast this card any time you could cast an instant by sacrificing a [subtype] permanent. If you do, the total cost to cast this card is reduced by the sacrificed permanent's mana cost."
    b. The permanent is sacrificed at the same time the spell is announced (see rule 601.2a). The total cost of the spell is reduced by the sacrificed permanent's mana cost (see rule 601.2e).
    c. Generic mana in the sacrificed permanent's mana cost reduces generic mana in the total cost to cast the card with offering. Colored mana in the sacrificed permanent's mana cost reduces mana of the same color in the total cost to cast the card with offering. Colored mana in the sacrificed permanent's mana cost that doesn't match colored mana in the colored mana cost of the card with offering, or is in excess of the card's colored mana cost, reduces that much generic mana in the total cost.

702.47
------

Ninjutsu

    a. Ninjutsu is an activated ability that functions only while the card with ninjutsu is in a player's hand. "Ninjutsu [cost]" means "[Cost], Reveal this card from your hand, Return an unblocked attacking creature you control to its owner's hand: Put this card onto the battlefield from your hand tapped and attacking."
    b. The card with ninjutsu remains revealed from the time the ability is announced until the ability leaves the stack.
    c. A ninjutsu ability may be activated only while a creature on the battlefield is unblocked (see rule 509.1h). The creature with ninjutsu is put onto the battlefield unblocked. It will be attacking the same player or planeswalker as the creature that was returned to its owner's hand.

702.48
------

Epic

    a. Epic represents two spell abilities, one of which creates a delayed triggered ability. "Epic" means "For the rest of the game, you can't cast spells," and "At the beginning of each of your upkeeps for the rest of the game, copy this spell except for its epic ability. If the spell has any targets, you may choose new targets for the copy." See rule 706.9.
    b. A player can't cast spells once a spell with epic he or she controls resolves, but effects (such as the epic ability itself) can still put copies of spells onto the stack.

702.49
------

Convoke

    a. Convoke is a static ability that functions while the spell with convoke is on the stack. "Convoke" means "As an additional cost to cast this spell, you may tap any number of untapped creatures you control. Each creature tapped this way reduces the cost to cast this spell by |1| or by one mana of any of that creature's colors." Using the convoke ability follows the rules for paying additional costs in rules 601.2b and 601.2e-g.

        .. admonition:: Example

            You cast Guardian of Vitu-Ghazi, a spell with convoke that costs |6|\ |G|\ |W|. You announce that you're going to tap a colorless creature, a red creature, and a green-and-white creature to help pay for it. The colorless creature and the red creature each reduce the spell's cost by |1|. You choose whether the green-white creature reduces the spell's cost by |1|, |G|, or |W|. Then the creatures become tapped as you pay Guardian of Vitu-Ghazi's cost.

    b. Multiple instances of convoke on the same spell are redundant.

702.50
------

Dredge

    a. Dredge is a static ability that functions only while the card with dredge is in a player's graveyard. "Dredge N" means "As long as you have at least N cards in your library, if you would draw a card, you may instead put N cards from the top of your library into your graveyard and return this card from your graveyard to your hand."
    b. A player with fewer cards in his or her library than the number required by a dredge ability can't put any of them into his or her graveyard this way.

702.51
------

Transmute

    a. Transmute is an activated ability that functions only while the card with transmute is in a player's hand. "Transmute [cost]" means "[Cost], Discard this card: Search your library for a card with the same converted mana cost as the discarded card, reveal that card, and put it into your hand. Then shuffle your library. Activate this ability only any time you could cast a sorcery."
    b. Although the transmute ability can be activated only if the card is in a player's hand, it continues to exist while the object is on the battlefield and in all other zones. Therefore objects with transmute will be affected by effects that depend on objects having one or more activated abilities.

702.52
------

Bloodthirst

    a. Bloodthirst is a static ability. "Bloodthirst N" means "If an opponent was dealt damage this turn, this permanent enters the battlefield with N +1/+1 counters on it."
    b. "Bloodthirst X" is a special form of bloodthirst. "Bloodthirst X" means "This permanent enters the battlefield with X +1/+1 counters on it, where X is the total damage your opponents have been dealt this turn."
    c. If an object has multiple instances of bloodthirst, each applies separately.

702.53
------

Haunt

    a. Haunt is a triggered ability. "Haunt" on a permanent means "When this permanent is put into a graveyard from the battlefield, exile it haunting target creature." "Haunt" on an instant or sorcery spell means "When this spell is put into a graveyard during its resolution, exile it haunting target creature."
    b. Cards that are in the exile zone as the result of a haunt ability "haunt" the creature targeted by that ability. The phrase "creature it haunts" refers to the object targeted by the haunt ability, regardless of whether or not that object is still a creature.
    c. Triggered abilities of cards with haunt that refer to the haunted creature can trigger in the exile zone.

702.54
------

Replicate

    a. Replicate is a keyword that represents two abilities. The first is a static ability that functions while the spell with replicate is on the stack.  The second is a triggered ability that functions while the spell with replicate is on the stack. "Replicate [cost]" means "As an additional cost to cast this spell, you may pay [cost] any number of times" and "When you cast this spell, if a replicate cost was paid for it, copy it for each time its replicate cost was paid. If the spell has any targets, you may choose new targets for any of the copies." Paying a spell's replicate cost follows the rules for paying additional costs in rules 601.2b and 601.2e-g.
    b. If a spell has multiple instances of replicate, each is paid separately and triggers based on the payments made for it, not any other instance of replicate.

702.55
------

Forecast

    a. A forecast ability is a special kind of activated ability that can be activated only from a player's hand. It's written "Forecast -- [Activated ability]."
    b. A forecast ability may be activated only during the upkeep step of the card's owner and only once each turn. The controller of the forecast ability reveals the card with that ability from his or her hand as the ability is activated. That player plays with that card revealed in his or her hand until it leaves the player's hand or until a step or phase that isn't an upkeep step begins, whichever comes first.

702.56
------

Graft

    a. Graft represents both a static ability and a triggered ability. "Graft N" means "This permanent enters the battlefield with N +1/+1 counters on it" and "Whenever another creature enters the battlefield, if this permanent has a +1/+1 counter on it, you may move a +1/+1 counter from this permanent onto that creature."
    b. If a creature has multiple instances of graft, each one works separately.

702.57
------

Recover

    a. Recover is a triggered ability that functions only while the card with recover is in a player's graveyard. "Recover [cost]" means "When a creature is put into your graveyard from the battlefield, you may pay [cost]. If you do, return this card from your graveyard to your hand. Otherwise, exile this card."

702.58
------

Ripple

    a. Ripple is a triggered ability that functions only while the card with ripple is on the stack. "Ripple N" means "When you cast this spell, you may reveal the top N cards of your library, or, if there are fewer than N cards in your library, you may reveal all the cards in your library. If you reveal cards from your library this way, you may cast any of those cards with the same name as this spell without paying their mana costs, then put all revealed cards not cast this way on the bottom of your library in any order."
    b. If a spell has multiple instances of ripple, each triggers separately.

702.59
------

Split Second

    a. Split second is a static ability that functions only while the spell with split second is on the stack. "Split second" means "As long as this spell is on the stack, players can't cast other spells or activate abilities that aren't mana abilities."
    b. Players may activate mana abilities and take special actions while a spell with split second is on the stack. Triggered abilities trigger and are put on the stack as normal while a spell with split second is on the stack.
    c. Multiple instances of split second on the same spell are redundant.

702.60
------

Suspend

    a. Suspend is a keyword that represents three abilities. The first is a static ability that functions while the card with suspend is in a player's hand. The second and third are triggered abilities that function in the exile zone. "Suspend N -- [cost]" means "If you could begin to cast this card by putting it onto the stack from your hand, you may pay [cost] and exile it with N time counters on it. This action doesn't use the stack," and "At the beginning of your upkeep, if this card is suspended, remove a time counter from it," and "When the last time counter is removed from this card, if it's exiled, play it without paying its mana cost if able. If you can't, it remains exiled.  If you cast a creature spell this way, it gains haste until you lose control of the spell or the permanent it becomes."
    b. A card is "suspended" if it's in the exile zone, has suspend, and has a time counter on it.
    c. Casting a spell as an effect of its suspend ability follows the rules for paying alternative costs in rules 601.2b and 601.2e-g.

702.61
------

Vanishing

    a. Vanishing is a keyword that represents three abilities. "Vanishing N" means "This permanent enters the battlefield with N time counters on it," "At the beginning of your upkeep, if this permanent has a time counter on it, remove a time counter from it," and "When the last time counter is removed from this permanent, sacrifice it."
    b. Vanishing without a number means "At the beginning of your upkeep, if this permanent has a time counter on it, remove a time counter from it" and "When the last time counter is removed from this permanent, sacrifice it."
    c. If a permanent has multiple instances of vanishing, each works separately.

702.62
------

Absorb

    a. Absorb is a static ability. "Absorb N" means "If a source would deal damage to this creature, prevent N of that damage."
    b. Each absorb ability can prevent only N damage from any one source at any one time. It will apply separately to damage from other sources, or to damage dealt by the same source at a different time.
    c. If an object has multiple instances of absorb, each applies separately.

702.63
------

Aura Swap

    a. Aura swap is an activated ability of some Aura cards. "Aura swap [cost]" means "[Cost]: You may exchange this permanent with an Aura card in your hand."
    b. If either half of the exchange can't be completed, the ability has no effect.

        .. admonition:: Example

            You activate the aura swap ability of an Aura. The only Aura card in your hand can't enchant the permanent that's enchanted by the Aura with aura swap. The ability has no effect.

        .. admonition:: Example

            You activate the aura swap ability of an Aura that you control but you don't own. The ability has no effect.

702.64
------

Delve

    a. Delve is a static ability that functions while the spell that has delve is on the stack. "Delve" means "As an additional cost to cast this spell, you may exile any number of cards from your graveyard. Each card exiled this way reduces the cost to cast this spell by |1|." Using the delve ability follows the rules for paying additional costs in rules 601.2b and 601.2e-g.
    b. Multiple instances of delve on the same spell are redundant.

702.65
------

Fortify

    a. Fortify is an activated ability of Fortification cards. "Fortify [cost]" means "[Cost]: Attach this Fortification to target land you control.  Activate this ability only any time you could cast a sorcery."
    b. For more information about Fortifications, see rule 301, 301.
    c. If a Fortification has multiple instances of fortify, any of its fortify abilities may be used.

702.66
------

Frenzy

    a. Frenzy is a triggered ability. "Frenzy N" means "Whenever this creature attacks and isn't blocked, it gets +N/+0 until end of turn."
    b. If a creature has multiple instances of frenzy, each triggers separately.

702.67
------

Gravestorm

    a. Gravestorm is a triggered ability that functions on the stack.  "Gravestorm" means "When you cast this spell, put a copy of it onto the stack for each permanent that was put into a graveyard from the battlefield this turn. If the spell has any targets, you may choose new targets for any of the copies."
    b. If a spell has multiple instances of gravestorm, each triggers separately.

702.68
------

Poisonous

    a. Poisonous is a triggered ability. "Poisonous N" means "Whenever this creature deals combat damage to a player, that player gets N poison counters." (For information about poison counters, see rule 104.3d.)
    b. If a creature has multiple instances of poisonous, each triggers separately.

702.69
------

Transfigure

    a. Transfigure is an activated ability. "Transfigure [cost]" means "[Cost], Sacrifice this permanent: Search your library for a creature card with the same converted mana cost as this permanent and put it onto the battlefield.  Then shuffle your library. Activate this ability only any time you could cast a sorcery."

702.70
------

Champion

    a. Champion represents two triggered abilities. "Champion an [object]" means "When this permanent enters the battlefield, sacrifice it unless you exile another [object] you control" and "When this permanent leaves the battlefield, return the exiled card to the battlefield under its owner's control."
    b. The two abilities represented by champion are linked. See rule 607, 607.
    c. A permanent is "championed" by another permanent if the latter exiles the former as the direct result of a champion ability.

702.71
------

Changeling

    a. Changeling is a characteristic-defining ability. "Changeling" means "This object is every creature type." This ability works everywhere, even outside the game. See rule 604.3.
    b. Multiple instances of changeling on the same object are redundant.

702.72
------

Evoke

    a. Evoke represents two abilities: a static ability that functions in any zone from which the card with evoke can be cast and a triggered ability that functions on the battlefield. "Evoke [cost]" means "You may cast this card by paying [cost] rather than paying its mana cost" and "When this permanent enters the battlefield, if its evoke cost was paid, its controller sacrifices it." Paying a card's evoke cost follows the rules for paying alternative costs in rules 601.2b and 601.2e-g.

702.73
------

Hideaway

    a. Hideaway represents a static ability and a triggered ability.  "Hideaway" means "This permanent enters the battlefield tapped" and "When this permanent enters the battlefield, look at the top four cards of your library.  Exile one of them face down and put the rest on the bottom of your library in any order. The exiled card gains 'Any player who has controlled the permanent that exiled this card may look at this card in the exile zone.'"

702.74
------

Prowl

    a. Prowl is a static ability that functions on the stack. "Prowl [cost]" means "You may pay [cost] rather than pay this spell's mana cost if a player was dealt combat damage this turn by a source that, at the time it dealt that damage, was under your control and had any of this spell's creature types." Paying a spell's prowl cost follows the rules for paying alternative costs in rules 601.2b and 601.2e-g.

702.75
------

Reinforce

    a. Reinforce is an activated ability that functions only while the card with reinforce is in a player's hand. "Reinforce N -- [cost]" means "[Cost], Discard this card: Put N +1/+1 counters on target creature."
    b. Although the reinforce ability can be activated only if the card is in a player's hand, it continues to exist while the object is on the battlefield and in all other zones. Therefore objects with reinforce will be affected by effects that depend on objects having one or more activated abilities.

702.76
------

Conspire

    a. Conspire is a keyword that represents two abilities. The first is a static ability that functions while the spell with conspire is on the stack.  The second is a triggered ability that functions while the spell with conspire is on the stack. "Conspire" means "As an additional cost to cast this spell, you may tap two untapped creatures you control that each share a color with it" and "When you cast this spell, if its conspire cost was paid, copy it. If the spell has any targets, you may choose new targets for the copy." Paying a spell's conspire cost follows the rules for paying additional costs in rules 601.2b and 601.2e-g.
    b. If a spell has multiple instances of conspire, each is paid separately and triggers based on its own payment, not any other instance of conspire.

702.77
------

Persist

    a. Persist is a triggered ability. "Persist" means "When this permanent is put into a graveyard from the battlefield, if it had no -1/-1 counters on it, return it to the battlefield under its owner's control with a -1/-1 counter on it."

702.78
------

Wither

    a. Wither is a static ability. Damage dealt to a creature by a source with wither isn't marked on that creature. Rather, it causes that many -1/-1 counters to be put on that creature. See rule 119.3.
    b. If a permanent leaves the battlefield before an effect causes it to deal damage, its last known information is used to determine whether it had wither.
    c. The wither rules function no matter what zone an object with wither deals damage from.
    d. Multiple instances of wither on the same object are redundant.

702.79
------

Retrace

    a. Retrace appears on some instants and sorceries. It represents a static ability that functions while the card with retrace is in a player's graveyard.  "Retrace" means "You may cast this card from your graveyard by discarding a land card as an additional cost to cast it." Casting a spell using its retrace ability follows the rules for paying additional costs in rules 601.2b and 601.2e-g.

702.80
------

Devour

    a. Devour is a static ability. "Devour N" means "As this object enters the battlefield, you may sacrifice any number of creatures. This permanent enters the battlefield with N +1/+1 counters on it for each creature sacrificed this way."
    b. Some objects have abilities that refer to the number of creatures the permanent devoured. "It devoured" means "sacrificed as a result of its devour ability as it entered the battlefield."

702.81
------

Exalted

    a. Exalted is a triggered ability. "Exalted" means "Whenever a creature you control attacks alone, that creature gets +1/+1 until end of turn."
    b. A creature "attacks alone" if it's the only creature declared as an attacker in a given combat phase. See rule 506.5.

702.82
------

Unearth

    a. Unearth is an activated ability that functions while the card with unearth is in a graveyard. "Unearth [cost]" means "[Cost]: Return this card from your graveyard to the battlefield. It gains haste. Exile it at the beginning of the next end step. If it would leave the battlefield, exile it instead of putting it anywhere else. Activate this ability only any time you could cast a sorcery."

702.83
------

Cascade

    a. Cascade is a triggered ability that functions only while the spell with cascade is on the stack. "Cascade" means "When you cast this spell, exile cards from the top of your library until you exile a nonland card whose converted mana cost is less than this spell's converted mana cost. You may cast that card without paying its mana cost. Then put all cards exiled this way that weren't cast on the bottom of your library in a random order."
    b. If a spell has multiple instances of cascade, each triggers separately.

702.84
------

Annihilator

    a. Annihilator is a triggered ability. "Annihilator N" means "Whenever this creature attacks, defending player sacrifices N permanents."
    b. If a creature has multiple instances of annihilator, each triggers separately.

702.85
------

Level Up

    a. Level up is an activated ability. "Level up [cost]" means "[Cost]: Put a level counter on this permanent. Activate this ability only any time you could cast a sorcery."
    b. Each card printed with a level up ability is known as a leveler card.  It has a nonstandard layout and includes two level symbols that are themselves keyword abilities. See rule 710, 710.

702.86
------

Rebound

    a. Rebound appears on some instants and sorceries. It represents a static ability that functions while the spell is on the stack and may create a delayed triggered ability. "Rebound" means "If this spell was cast from your hand, instead of putting it into your graveyard as it resolves, exile it and, at the beginning of your next upkeep, you may cast this card from exile without paying its mana cost."
    b. Casting a card without paying its mana cost as the result of a rebound ability follows the rules for paying alternative costs in rules 601.2b and 601.2e-g.
    c. Multiple instances of rebound on the same spell are redundant.

702.87
------

Totem Armor

    a. Totem armor is a static ability that appears on some Auras. "Totem armor" means "If enchanted permanent would be destroyed, instead remove all damage marked on it and destroy this Aura."

702.88
------

Infect

    a. Infect is a static ability.
    b. Damage dealt to a player by a source with infect doesn't cause that player to lose life. Rather, it causes the player to get that many poison counters. See rule 119.3.
    c. Damage dealt to a creature by a source with infect isn't marked on that creature. Rather, it causes that many -1/-1 counters to be put on that creature. See rule 119.3.
    d. If a permanent leaves the battlefield before an effect causes it to deal damage, its last known information is used to determine whether it had infect.
    e. The infect rules function no matter what zone an object with infect deals damage from.
    f. Multiple instances of infect on the same object are redundant.

702.89
------

Battle Cry

    a. Battle cry is a triggered ability. "Battle cry" means "Whenever this creature attacks, each other attacking creature gets +1/+0 until end of turn."
    b. If a creature has multiple instances of battle cry, each triggers separately.

702.90
------

Living Weapon

    a. Living weapon is a triggered ability. "Living weapon" means "When this Equipment enters the battlefield, put a 0/0 black Germ creature token onto the battlefield, then attach this Equipment to it."

.. _turn-based-actions:

Turn-Based Actions
==================

703.1
-----

Turn-based actions are game actions that happen automatically when certain steps or phases begin, or when each step and phase ends. Turn-based actions don't use the stack.

    a. Abilities that watch for a specified step or phase to begin are triggered abilities, not turn-based actions. (See rule 603, 603.)

703.2
-----

Turn-based actions are not controlled by any player.

703.3
-----

Whenever a step or phase begins, if it's a step or phase that has any turn-based action associated with it, those turn-based actions are automatically dealt with first. This happens before state-based actions are checked, before triggered abilities are put on the stack, and before players receive priority.

703.4
-----

The turn-based actions are as follows:

    a. Immediately after the untap step begins, all phased-in permanents with phasing that the active player controls phase out, and all phased-out permanents that the active player controlled when they phased out phase in.  This all happens simultaneously. See rule 502.1.
    b. Immediately after the phasing action has been completed during the untap step, the active player determines which permanents he or she controls will untap. Then he or she untaps them all simultaneously. See rule 502.2.
    c. Immediately after the draw step begins, the active player draws a card.  See rule 504.1.
    d. In an Archenemy game (see rule 904), immediately after the archenemy's precombat main phase begins, that player sets the top card of his or her scheme deck in motion. See rule 701.21.
    e. Immediately after the beginning of combat step begins, if the game being played is a multiplayer game in which the active player's opponent's don't all automatically become defending players, the active player chooses one of his or her opponents. That player becomes the defending player. See rule 507.1.
    f. Immediately after the declare attackers step begins, the active player declares attackers. See rule 508.1.
    g. Immediately after the declare blockers step begins, the defending player declares blockers. See rule 509.1.
    h. Immediately after blockers have been declared during the declare blockers step, for each attacking creature that's become blocked by multiple creatures, the active player announces the damage assignment order among the blocking creatures. See rule 509.2.
    i. Immediately after the active player has announced damage assignment orders (if necessary) during the declare blockers step, for each creature that's blocking multiple creatures, the defending player announces the damage assignment order among the attacking creatures. See rule 509.3.
    j. Immediately after the combat damage step begins, each player in APNAP order announces how each attacking or blocking creature he or she controls assigns its combat damage. See rule 510.1.
    k. Immediately after combat damage has been assigned during the combat damage step, all combat damage is dealt simultaneously. See rule 510.2.

    m. Immediately after the cleanup step begins, if the active player's hand contains more cards than his or her maximum hand size (normally seven), he or she discards enough cards to reduce his or her hand size to that number. See rule 514.1.
    n. Immediately after the active player has discarded cards (if necessary) during the cleanup step, all damage is removed from permanents and all "until end of turn" and "this turn" effects end. These actions happen simultaneously.  See rule 514.2.

    p. When each step or phase ends, any unused mana left in a player's mana pool empties. See rule 500.4.

.. _state-based-actions:

State-Based Actions
===================

704.1
-----

State-based actions are game actions that happen automatically whenever certain conditions (listed below) are met. State-based actions don't use the stack.

    a. Abilities that watch for a specified game state are triggered abilities, not state-based actions. (See rule 603, 603.)

704.2
-----

State-based actions are checked throughout the game and are not controlled by any player.


.. _grant-priority:

704.3
-----

Whenever a player would get priority (see :ref:`timing`"), the game checks for any of the listed conditions for state-based actions, then performs all applicable state-based actions simultaneously as a single event. If any state-based actions are performed as a result of a check, the check is repeated; otherwise all triggered abilities that are waiting to be put on the stack are put on the stack, then the check is repeated. Once no more state-based actions have been performed as the result of a check and no triggered abilities are waiting to be put on the stack, the appropriate player gets priority. This process also occurs during the cleanup step (see rule 514), except that if no state-based actions are performed as the result of the step's first check and no triggered abilities are waiting to be put on the stack, then no player gets priority and the step ends.

704.4
-----

Unlike triggered abilities, state-based actions pay no attention to what happens during the resolution of a spell or ability.

.. admonition:: Example

    A player controls a creature with the ability "This creature's power and toughness are each equal to the number of cards in your hand" and casts a spell whose effect is "Discard your hand, then draw seven cards." The creature will temporarily have toughness 0 in the middle of the spell's resolution but will be back up to toughness 7 when the spell finishes resolving. Thus the creature will survive when state-based actions are checked. In contrast, an ability that triggers when the player has no cards in hand goes on the stack after the spell resolves, because its trigger event happened during resolution.

.. _sba-list:

704.5
-----

The state-based actions are as follows:

    a. If a player has 0 or less life, he or she loses the game.
    b. If a player attempted to draw a card from a library with no cards in it since the last time state-based actions were checked, he or she loses the game.
    c. If a player has ten or more poison counters, he or she loses the game.  Ignore this rule in Two-Headed Giant games; see rule 704.5u instead.
    d. If a token is phased out, or is in a zone other than the battlefield, it ceases to exist.
    e. If a copy of a spell is in a zone other than the stack, it ceases to exist. If a copy of a card is in any zone other than the stack or the battlefield, it ceases to exist.
    f. If a creature has toughness 0 or less, it's put into its owner's graveyard. Regeneration can't replace this event.
    g. If a creature has toughness greater than 0, and the total damage marked on it is greater than or equal to its toughness, that creature has been dealt lethal damage and is destroyed. Regeneration can replace this event.
    h. If a creature has toughness greater than 0, and it's been dealt damage by a source with deathtouch since the last time state-based actions were checked, that creature is destroyed. Regeneration can replace this event.
    i. If a planeswalker has loyalty 0, it's put into its owner's graveyard.

    .. _planeswalker-uniqueness-rule:

    j. If two or more planeswalkers that share a planeswalker type are on the battlefield, all are put into their owners' graveyards. This is called the "planeswalker uniqueness rule."

    .. _legend-rule:

    k. If two or more legendary permanents with the same name are on the battlefield, all are put into their owners' graveyards. This is called the "legend rule." If only one of those permanents is legendary, this rule doesn't apply.

    .. _world-rule:

    m. If two or more permanents have the supertype world, all except the one that has been a permanent with the world supertype on the battlefield for the shortest amount of time are put into their owners' graveyards. In the event of a tie for the shortest amount of time, all are put into their owners' graveyards. This is called the "world rule."
    n. If an Aura is attached to an illegal object or player, or is not attached to an object or player, that Aura is put into its owner's graveyard.

    p. If an Equipment or Fortification is attached to an illegal permanent, it becomes unattached from that permanent. It remains on the battlefield.
    q. If a creature is attached to an object or player, it becomes unattached and remains on the battlefield. Similarly, if a permanent that's neither an Aura, an Equipment, nor a Fortification is attached to an object or player, it becomes unattached and remains on the battlefield.
    r. If a permanent has both a +1/+1 counter and a -1/-1 counter on it, N +1/+1 and N -1/-1 counters are removed from it, where N is the smaller of the number of +1/+1 and -1/-1 counters on it.
    s. If a permanent with an ability that says it can't have more than N counters of a certain kind on it has more than N counters of that kind on it, all but N of those counters are removed from it.
    t. In a Two-Headed Giant game, if a team has 0 or less life, that team loses the game. See rule 810, 810.
    u. In a Two-Headed Giant game, if a team has fifteen or more poison counters, that team loses the game. See rule 810, 810.
    v. In a Commander game, a player that's been dealt 21 or more combat damage by the same commander over the course of the game loses the game. See rule 903, 903.
    w. In an Archenemy game, if a non-ongoing scheme card is face up in the command zone, and it isn't the source of a triggered ability that has triggered but not yet left the stack, that scheme card is turned face down and put on the bottom of its owner's scheme deck. See rule 904, 904.

704.6
-----

If multiple state-based actions would have the same result at the same time, a single replacement effect will replace all of them.

.. admonition:: Example

    You control Lich's Mirror, which says "If you would lose the game, instead shuffle your hand, your graveyard, and all permanents you own into your library, then draw seven cards and your life total becomes 20." There's one card in your library and your life total is 1. A spell causes you to draw two cards and lose 2 life. The next time state-based actions are checked, you'd lose the game due to rule 704.5a and rule 704.5b. Instead, Lich's Mirror replaces that game loss and you keep playing.

.. _coin:

Flipping a Coin
===============

705.1
-----

To flip a coin for an object that cares whether a player wins or loses the flip, the affected player flips the coin and calls "heads" or "tails." If the call matches the result, that player wins the flip. Otherwise, the player loses the flip. Only the player who flips the coin wins or loses the flip; no other players are involved.

705.2
-----

To flip a coin for an object that cares whether the coin comes up heads or tails, each affected player flips a coin without making a call. No player wins or loses this kind of flip.

705.3
-----

A coin used in a flip must be a two-sided object with easily distinguished sides and equal likelihood that either side lands face up. If the coin that's being flipped doesn't have an obvious "heads" or "tails," designate one side to be "heads," and the other side to be "tails." Other methods of randomization may be substituted for flipping a coin as long as there are two possible outcomes of equal likelihood and all players agree to the substitution. For example, the player may roll an even-sided die and call "odds" or "evens," or roll an even-sided die and designate that "odds" means "heads" and "evens" means "tails."

.. _copying:

Copying Objects
===============

706.1
-----

Some objects become or turn another object into a "copy" of a spell, permanent, or card. Some effects put a token onto the battlefield that's a copy of another object. (Certain older cards were printed with the phrase "search for a copy." This section doesn't cover those cards, which have received new text in the Oracle card reference.)

706.2
-----

When copying an object, the copy acquires the copiable values of the original object's characteristics and, for an object on the stack, choices made when casting or activating it (mode, targets, the value of X, whether it was kicked, how it will affect multiple targets, and so on). The "copiable values" are the values derived from the text printed on the object (that text being name, mana cost, card type, subtype, supertype, expansion symbol, rules text, power, toughness, and/or loyalty), as modified by other copy effects, by "as .  . . enters the battlefield" and "as . . . is turned face up" abilities that set characteristics, and by abilities that caused the object to be face down. Other effects (including type-changing and text-changing effects), status, and counters are not copied.

    .. admonition:: Example

        Chimeric Staff is an artifact that reads "|X|: Chimeric Staff becomes an X/X artifact creature until end of turn." Clone is a creature that reads, "You may have Clone enter the battlefield as a copy of any creature on the battlefield." After a Staff has become a 5/5 artifact creature, a Clone enters the battlefield as a copy of it. The Clone is an artifact, not a 5/5 artifact creature. (The copy has the Staff's ability, however, and will become a creature if that ability is activated.) Example: Clone enters the battlefield as a copy of a face-down Grinning Demon (a creature with morph |2|\ |B|\ |B|). The Clone is a colorless 2/2 creature with no name, no types, no abilities, and no mana cost. It will still be face up. Its controller can't pay |2|\ |B|\ |B| to turn it face up.

    a. A copy acquires the color of the object it's copying because that value is derived from its mana cost. A copy acquires the abilities of the object it's copying because those values are derived from its rules text. A copy doesn't wind up with two values of each ability (that is, it doesn't copy the object's abilities and its rules text, then have that rules text define a new set of abilities).

706.3
-----

The copy's copiable values become the copied information, as modified by the copy's status (see rule 110.6). Objects that copy the object will use the new copiable values.

.. admonition:: Example

    Vesuvan Doppelganger reads, "You may have Vesuvan Doppelganger enter the battlefield as a copy of any creature on the battlefield except it doesn't copy that creature's color and it gains 'At the beginning of your upkeep, you may have this creature become a copy of target creature except it doesn't copy that creature's color. If you do, this creature gains this ability.'" A Vesuvan Doppelganger enters the battlefield as a copy of Runeclaw Bear (a 2/2 green Bear creature with no abilities). Then a Clone enters the battlefield as a copy of the Doppelganger. The Clone is a 2/2 blue Bear named Runeclaw Bear that has the Doppelganger's upkeep-triggered ability.

.. admonition:: Example

    Tomoya the Revealer (a flipped flip card) becomes a copy of Nezumi Shortfang (an unflipped flip card). Tomoya's characteristics become the characteristics of Stabwhisker the Odious, which is the flipped version of Nezumi Shortfang.

.. admonition:: Example

    A face-down Grinning Demon (a creature with morph) becomes a copy of a face-up Branchsnap Lorian (a 4/1 green creature with trample and morph |G|). The Demon's characteristics become the characteristics of Branchsnap Lorian. However, since the creature is face down, it remains a 2/2 colorless creature with no name, types, or abilities, and no mana cost. It can be turned face up for |G|. If it's turned face up, it will have the characteristics of Branchsnap Lorian.

.. admonition:: Example

    A face-down Grinning Demon (a creature with morph) becomes a copy of Wandering Ones (a 1/1 blue Spirit creature that doesn't have morph). It will be a face-down Wandering Ones. It remains a 2/2 colorless creature with no name, types, or abilities, and no mana cost. Its controller can't turn it face up as a special action. If an effect turns it face up, it will have the characteristics of Wandering Ones.

706.4
-----

Some effects cause a permanent that's copying a permanent to copy a different object while remaining on the battlefield. The change doesn't trigger enters-the-battlefield or leaves-the-battlefield abilities. This also doesn't change any noncopy effects presently affecting the permanent.

.. admonition:: Example

    Unstable Shapeshifter reads, "Whenever a creature enters the battlefield, Unstable Shapeshifter becomes a copy of that creature and gains this ability." It's affected by Giant Growth, which reads "Target creature gets +3/+3 until end of turn." If a creature enters the battlefield later this turn, Unstable Shapeshifter will become a copy of that creature, but it will still get +3/+3 from the Giant Growth.

706.5
-----

An object that enters the battlefield "as a copy" or "that's a copy" of another object becomes a copy as it enters the battlefield. It doesn't enter the battlefield, and then become a copy of that permanent. If the text that's being copied includes any abilities that replace the enters-the-battlefield event (such as "enters the battlefield with" or "as [this] enters the battlefield" abilities), those abilities will take effect. Also, any enters-the-battlefield triggered abilities of the copy will have a chance to trigger.

.. admonition:: Example

    Skyshroud Behemoth reads, "Fading 2 (This creature enters the battlefield with two fade counters on it. At the beginning of your upkeep, remove a fade counter from it. If you can't, sacrifice it.)" and "Skyshroud Behemoth enters the battlefield tapped." A Clone that enters the battlefield as a copy of a Skyshroud Behemoth will also enter the battlefield tapped with two fade counters on it.

.. admonition:: Example

    Striped Bears reads, "When Striped Bears enters the battlefield, draw a card." A Clone enters the battlefield as a copy of Striped Bears. The Clone has the Bears' enters-the-battlefield triggered ability, so the Clone's controller draws a card.

706.6
-----

When copying a permanent, any choices that have been made for that permanent aren't copied. Instead, if an object enters the battlefield as a copy of another permanent, the object's controller will get to make any "as [this] enters the battlefield" choices for it.

.. admonition:: Example

    A Clone enters the battlefield as a copy of Chameleon Spirit. Chameleon Spirit reads, in part, "As Chameleon Spirit enters the battlefield, choose a color." The Clone won't copy the color choice of the Spirit; rather, the controller of the Clone will get to make a new choice.

706.7
-----

If a pair of linked abilities are copied, those abilities will be similarly linked to one another on the object that copied them. One ability refers only to actions that were taken or objects that were affected by the other. They can't be linked to any other ability, regardless of what other abilities the copy may currently have or may have had in the past. See rule 607, 607.

    a. If an ability causes a player to "choose a [value]" or "name a card," and a second, linked ability refers to that choice, the second ability is the only ability that can refer to that choice. An object doesn't "remember" that choice and use it for other abilities it may copy later. If an object copies an ability that refers to a choice, but either (a) doesn't copy that ability's linked ability or (b) does copy the linked ability but no choice is made for it, then the choice is considered to be "undefined." If an ability refers to an undefined choice, that part of the ability won't do anything.

.. admonition:: Example

    Voice of All enters the battlefield and Unstable Shapeshifter copies it. Voice of All reads, in part, "As Voice of All enters the battlefield, choose a color." and "Voice of All has protection from the chosen color." Unstable Shapeshifter never had a chance for a color to be chosen for it, because it didn't enter the battlefield as a Voice of All card, so the protection ability doesn't protect it from anything at all.

.. admonition:: Example

    A Vesuvan Doppelganger enters the battlefield as a copy of Chameleon Spirit, and the Doppelganger's controller chooses blue. Later, the Doppelganger copies Quirion Elves. The Elves has the ability, "|T|: Add one mana of the chosen color to your mana pool." Even though a color was chosen for the Doppelganger, it wasn't chosen for the ability linked to the mana ability copied from the Elves. If that mana ability of the Doppelganger is activated, it will not produce mana.

706.8
-----

Copy effects may include modifications or exceptions to the copying process.

    a. Some copy effects cause the copy to gain an ability as part of the copying process. This ability becomes part of the copiable values for the copy, along with any other abilities that were copied.

        .. admonition:: Example

            Quirion Elves enters the battlefield and an Unstable Shapeshifter copies it. The copiable values of the Shapeshifter now match those of the Elves, except that the Shapeshifter also has the ability "Whenever a creature enters the battlefield, Unstable Shapeshifter becomes a copy of that creature and gains this ability." Then a Clone enters the battlefield as a copy of the Unstable Shapeshifter. The Clone copies the new copiable values of the Shapeshifter, including the ability that the Shapeshifter gave itself when it copied the Elves.

    b. Some copy effects specifically state that they don't copy certain characteristics and instead retain their original values. These effects use the phrase "except its [characteristic] is still [value]" or "except it's still [value(s)]." They may also simply state that certain characteristics are not copied.
    c. Some copy effects modify a characteristic as part of the copying process. The final value(s) for that characteristic becomes part of the copiable values for the copy.

        .. admonition:: Example

            Copy Artifact is an enchantment that reads, "You may have Copy Artifact enter the battlefield as a copy of any artifact on the battlefield, except it's an enchantment in addition to its other types." It enters the battlefield as a copy of Juggernaut. The copiable values of the Copy Artifact now match those of Juggernaut with one modification: its types are now artifact, creature, and enchantment.

    d. When applying a copy effect that doesn't copy a certain characteristic, retains an original value for a certain characteristic, or modifies the final value of a certain characteristic, any characteristic-defining ability (see rule 604.3) of the object being copied that defines that characteristic is not copied.

        .. admonition:: Example

            Quicksilver Gargantuan is a creature that reads, "You may have Quicksilver Gargantuan enter the battlefield as a copy of any creature on the battlefield, except it's still 7/7." Quicksilver Gargantuan enters the battlefield as a copy of Tarmogoyf, which has a characteristic-defining ability that defines its power and toughness. Quicksilver Gargantuan does not have that ability. It will be 7/7.

.. _copy-spell:

706.9
-----

To copy a spell or activated ability means to put a copy of it onto the stack; a copy of a spell isn't cast and a copy of an activated ability isn't activated. A copy of a spell or ability copies both the characteristics of the spell or ability and all decisions made for it, including modes, targets, the value of X, and additional or alternative costs. (See rule 601, 601.) Choices that are normally made on resolution are not copied. If an effect of the copy refers to objects used to pay its costs, it uses the objects used to pay the costs of the original spell or ability. A copy of a spell is owned by the player under whose control it was put on the stack. A copy of a spell or ability is controlled by the player under whose control it was put on the stack. A copy of a spell is itself a spell, even though it has no spell card associated with it. A copy of an ability is itself an ability.

    .. admonition:: Example

        A player casts Fork, targeting an Emerald Charm. Fork reads, "Copy target instant or sorcery spell, except that the copy is red. You may choose new targets for the copy." Emerald Charm is a green instant that reads, "Choose one -- Untap target permanent; or destroy target non-Aura enchantment; or target creature loses flying until end of turn." When the Fork resolves, it puts a copy of the Emerald Charm on the stack except the copy is red, not green. The copy has the same mode that was chosen for the original Emerald Charm. It does not necessarily have the same target, but only because Fork allows choosing of new targets.

    .. admonition:: Example

        Fling is an instant that reads, "As an additional cost to cast Fling, sacrifice a creature" and "Fling deals damage equal to the sacrificed creature's power to target creature or player." When determining how much damage a copy of Fling deals, it checks the power of the creature sacrificed to pay for the original Fling.

    a. If a copy of a spell is in a zone other than the stack, it ceases to exist. If a copy of a card is in any zone other than the stack or the battlefield, it ceases to exist. These are state-based actions. See rule 704.
    b. A copy of an ability has the same source as the original ability. If the ability refers to its source by name, the copy refers to that same object and not to any other object with the same name. The copy is considered to be the same ability by effects that count how many times that ability has resolved during the turn.
    c. Some effects copy a spell or ability and state that its controller may choose new targets for the copy. The player may leave any number of the targets unchanged, even if those targets would be illegal. If the player chooses to change some or all of the targets, the new targets must be legal. Once the player has decided what the copy's targets will be, the copy is put onto the stack with those targets.

706.10
------

If an effect refers to a permanent by name, the effect still tracks that permanent even if it changes names or becomes a copy of something else.

.. admonition:: Example

    An Unstable Shapeshifter copies a Crazed Armodon. Crazed Armodon reads, "|G|: Crazed Armodon gets +3/+0 and gains trample until end of turn.  Destroy Crazed Armodon at the beginning of the next end step. Activate this ability only once each turn." If this ability of the Shapeshifter is activated, the Shapeshifter will be destroyed at the beginning of the next end step, even if it's no longer a copy of Crazed Armodon at that time.

706.11
------

An effect that instructs a player to "cast a copy" of an object follows the rules for casting spells, except that the copy is cast while another spell or ability is resolving. Casting a copy of an object follows steps 601.2a-g of rule 601, 601. and then the copy becomes cast. The cast copy is a spell on the stack, and just like any other spell it can resolve or be countered.

.. _face-down:

Face-Down Spells and Permanents
===============================

707.1
-----

Two cards (Illusionary Mask and Ixidron) and the morph ability (see rule 702.35) allow spells and permanents to be face down.

707.2
-----

Face-down spells and face-down permanents have no characteristics other than those listed by the ability or rules that allowed the spell or permanent to be face down. Any listed characteristics are the copiable values of that object's characteristics. (See rule 613, 613. and rule 706, "Copying Objects.")

    a. If a face-up permanent is turned face down by a spell or ability, it becomes a 2/2 face-down creature with no text, no name, no subtypes, no expansion symbol, and no mana cost. These values are the copiable values of that object's characteristics.

707.3
-----

Objects that are put onto the battlefield face down are turned face down before they enter the battlefield, so the permanent's enters-the-battlefield abilities won't trigger (if triggered) or have any effect (if static).

707.4
-----

Objects that are cast face down are turned face down before they are put onto the stack, so effects that care about the characteristics of a spell will see only the face-down spell's characteristics. Any effects or prohibitions that would apply to casting an object with these characteristics (and not the face-up object's characteristics) are applied to casting this object.

707.5
-----

At any time, you may look at a face-down spell you control on the stack or a face-down permanent you control (even if it's phased out). You can't look at face-down cards in any other zone or face-down spells or permanents controlled by another player.

707.6
-----

If you control multiple face-down spells or face-down permanents, you must ensure at all times that your face-down spells and permanents can be easily differentiated from each other. This includes, but is not limited to, knowing the order spells were cast, the order that face-down permanents entered the battlefield, which creature attacked last turn, and any other differences between face-down spells or permanents. Common methods for distinguishing between face-down objects include using counters or dice to mark the different objects, or clearly placing those objects in order on the table.

707.7
-----

The ability or rules that allow a permanent to be face down may also allow the permanent's controller to turn it face up. Spells normally can't be turned face up.

707.8
-----

As a face-down permanent is turned face up, its copiable values revert to its normal copiable values. Any effects that have been applied to the face-down permanent still apply to the face-up permanent. Any abilities relating to the permanent entering the battlefield don't trigger and don't have any effect, because the permanent has already entered the battlefield.

707.9
-----

If a face-down permanent moves from the battlefield to any other zone, its owner must reveal it to all players as he or she moves it. If a face-down spell moves from the stack to any zone other than the battlefield, its owner must reveal it to all players as he or she moves it. At the end of each game, all face-down permanents and spells must be revealed to all players.

707.10
------

If a face-down permanent becomes a copy of another permanent, its copiable values become the copiable values of that permanent, as modified by its face-down status. Its characteristics therefore remain the same: the characteristics listed by the ability or rules that allowed it to be turned face down. However, if it is turned face up, its copiable values become the values it copied from the other permanent. See rule 706.3.

707.11
------

If a face-down permanent would have an "As [this permanent] is turned face up . . ." ability after it's turned face up, that ability is applied while that permanent is being turned face up, not afterward.

.. _split:

Split Cards
===========

708.1
-----

Split cards have two card faces on a single card. The back of a split card is the normal *Magic* card back.

708.2
-----

In every zone except the stack, split cards have two sets of characteristics and two converted mana costs. As long as a split card is a spell on the stack, only the characteristics of the half being cast exist. The other half's characteristics are treated as though they didn't exist.

    a. If a player casts a split card, that player chooses which half of that split card he or she is casting before putting it onto the stack. Only the half that is being cast is considered to be put onto the stack.

708.3
-----

Each split card that consists of two halves with different colored mana symbols in their mana costs is a multicolored card while it's not a spell on the stack. While it's a spell on the stack, it's only the color or colors of the half being cast.

708.4
-----

Although split cards have two castable halves, each split card is only one card. For example, a player who has drawn or discarded a split card has drawn or discarded one card, not two.

708.5
-----

An effect that asks for a particular characteristic of a split card while it's in a zone other than the stack gets two answers (one for each of the split card's two halves).

.. admonition:: Example

    Infernal Genesis has an ability that reads, "At the beginning of each player's upkeep, that player puts the top card from his or her library into his or her graveyard. He or she then puts X 1/1 black Minion creature tokens onto the battlefield, where X is that card's converted mana cost." If the top card of your library is Assault/Battery when this ability resolves, the game sees its converted mana cost as "1, and 4." You get five creature tokens.

708.6
-----

Some effects perform comparisons involving characteristics of one or more split cards in a zone other than the stack.

    a. An effect that performs a positive comparison (such as asking if a card is red) or a relative comparison (such as asking if a card's converted mana cost is less than 2) involving characteristics of one or more split cards in any zone other than the stack gets only one answer. This answer is "yes" if either side of each split card in the comparison would return a "yes" answer if compared individually.
    b. An effect that performs a negative comparison (such as asking if cards have different names) involving characteristics of one or more split cards in any zone other than the stack also gets only one answer. This answer is "yes" if performing the analogous positive comparison would return a "no" answer.
    c. If an effect performs a comparison involving multiple characteristics of one or more split cards in any zone other than the stack, each characteristic is compared separately. If each of the individual comparisons would return a "yes" answer, the whole comparison returns a "yes" answer.

        .. admonition:: Example

            Void reads, "Choose a number. Destroy all artifacts and creatures with converted mana cost equal to that number. Then target player reveals his or her hand and discards all nonland cards with converted mana cost equal to the number." If a player casts Void and chooses 1, his or her opponent would discard Assault/Battery because the game sees its converted mana cost as "1, and 4." The same is true if the player chooses 4. If the player chooses 5, however, Assault/Battery would be unaffected.

708.7
-----

If an effect instructs a player to name a card and the player wants to name a split card, the player must name both halves of the split card. An object has the chosen name if it has at least one of the two names chosen this way.

.. _flip:

Flip Cards
==========

709.1
-----

Flip cards have a two-part card frame on a single card. The text that appears right side up on the card defines the card's normal characteristics.  Additional alternative characteristics appear upside down on the card. The back of a flip card is the normal *Magic* card back.

    a. The top half of a flip card contains the card's normal name, text box, type line, power, and toughness. The text box usually contains an ability that causes the permanent to "flip" if certain conditions are met.
    b. The bottom half of a flip card contains an alternative name, text box, type line, power, and toughness. These characteristics are used only if the permanent is on the battlefield and only if the permanent is flipped.
    c. A flip card's color, mana cost, expansion symbol, illustration credit, and legal text don't change if the permanent is flipped. Also, any changes to it by external effects will still apply.

709.2
-----

In every zone other than the battlefield, and also on the battlefield before the permanent flips, a flip card has only the normal characteristics of the card. Once a permanent is flipped, its normal name, text box, type line, power, and toughness don't apply and the alternative versions of those characteristics apply instead.

.. admonition:: Example

    Akki Lavarunner is a nonlegendary creature that flips into a legendary creature named Tok-Tok, Volcano Born. An effect that says "search your library for a legendary card" can't find this flip card. An effect that says "legendary creatures get +2/+2" doesn't affect Akki Lavarunner, but it does affect Tok-Tok.

709.3
-----

You must ensure that it's clear at all times whether a permanent you control is flipped or not, both when it's untapped and when it's tapped. Common methods for distinguishing between flipped and unflipped permanents include using coins or dice to mark flipped objects.

709.4
-----

Flipping a permanent is a one-way process. Once a permanent is flipped, it's impossible for it to become unflipped. However, if a flipped permanent leaves the battlefield, it retains no memory of its status. See rule 110.6.

709.5
-----

If an effect instructs a player to name a card and the player wants to name a flip card's alternative name, the player may do so.

.. _leveler:

Leveler Cards
=============

710.1
-----

Each leveler card has a striated text box and three power/toughness boxes. The text box of a leveler card contains two level symbols.

710.2
-----

A level symbol is a keyword ability that represents a static ability.  The level symbol includes either a range of numbers, indicated here as "N1-N2," or a single number followed by a plus sign, indicated here as "N3+." Any abilities printed within the same text box striation as a level symbol are part of its static ability. The same is true of the power/toughness box printed within that striation, indicated here as "[P/T]."

    a. "{LEVEL N1-N2} [Abilities] [P/T]" means "As long as this creature has at least N1 level counters on it, but no more than N2 level counters on it, it's [P/T] and has [abilities]."
    b. "{LEVEL N3+} [Abilities] [P/T]" means "As long as this creature has N3 or more level counters on it, it's [P/T] and has [abilities]."

710.3
-----

The text box striations have no game significance other than clearly demarcating which abilities and which power/toughness box are associated with which level symbol. Leveler cards each contain only one text box.

710.4
-----

Any ability a leveler card has that isn't preceded by a level symbol is treated normally. In particular, each leveler permanent has its level up ability (see rule 702.85) at all times; it may be activated regardless of how many level counters are on that permanent.

710.5
-----

If the number of level counters on a leveler creature is less than N1 (the first number printed in its {LEVEL N1-N2} symbol), it has the power and toughness denoted by its uppermost power/toughness box.

710.6
-----

In every zone other than the battlefield, a leveler card has the power and toughness denoted by its uppermost power/toughness box.

.. _controlling:

Controlling Another Player
==========================

711.1
-----

Two cards (Mindslaver and Sorin Markov) allow a player to control another player during that player's next turn. This effect applies to the next turn that the affected player actually takes. The affected player is controlled during the entire turn; the effect doesn't end until the beginning of the next turn.

    a. Multiple player-controlling effects that affect the same player overwrite each other. The last one to be created is the one that works.
    b. If a turn is skipped, any pending player-controlling effects wait until the player who would be affected actually takes a turn.

711.2
-----

One card (Word of Command) allows a player to control another player for a limited duration.

711.3
-----

Only control of the player changes. All objects are controlled by their normal controllers. A player who's being controlled during his or her turn is still the active player.

711.4
-----

If information about an object would be visible to the player being controlled, it's visible to both that player and the controller of the player.

.. admonition:: Example

    The controller of a player can see that player's hand and the identity of any face-down creatures he or she controls.

711.5
-----

While controlling another player, a player makes all choices and decisions the controlled player is allowed to make or is told to make by the rules or by any objects. This includes choices and decisions about what to play, and choices and decisions called for by spells and abilities.

    .. admonition:: Example

        The controller of another player decides which spells that player casts and what those spells target, and makes any required decisions when those spells resolve.

    .. admonition:: Example

        The controller of another player during his or her turn decides which of that player's creatures attack, which player or planeswalker each one attacks, what the damage assignment order of the creatures that block them is (if any of the attacking creatures are blocked by multiple creatures), and how those attacking creatures assign their combat damage.

    a. The controller of another player can use only that player's resources (cards, mana, and so on) to pay costs for that player.

        .. admonition:: Example

            If the controller of a player decides that the controlled player will cast a spell with an additional cost of discarding cards, the cards are discarded from the controlled player's hand.

    b. The controller of another player can't make choices or decisions for that player that aren't called for by the rules or by any objects. The controller also can't make any choices or decisions for the player that would be called for by the tournament rules.

        .. admonition:: Example

            The player who's being controlled still chooses whether he or she leaves to visit the restroom, trades a card to someone else, takes an intentional draw, or calls a judge about an error or infraction.

711.6
-----

The controller of another player can't make that player concede. A player may concede the game at any time, even if he or she is controlled by another player. See rule 104.3a.

711.7
-----

The effect that gives control of a player to another player may restrict the actions the controlled player is allowed to take or specify actions that the controlled player must take.

711.8
-----

A player who controls another player also continues to make his or her own choices and decisions.

711.9
-----

A player may gain control of himself or herself. That player will make his or her own decisions and choices as normal.

.. _ending-turn:

Ending the Turn
===============

712.1
-----

Two cards (Time Stop and Sundial of the Infinite) end the turn. When an effect ends the turn, follow these steps in order, as they differ from the normal process for resolving spells and abilities (see rule 608, "Resolving Spells and Abilities").

    a. Exile every object on the stack, including the object that's resolving.  Remove all creatures and planeswalkers (including those that are phased out) from combat. All objects not on the battlefield or in the command zone that aren't represented by cards will cease to exist the next time state-based actions are checked (see rule 704, "State-Based Actions").
    b. Check state-based actions. No player gets priority, and no triggered abilities are put onto the stack.
    c. The current phase and/or step ends. The game skips straight to the cleanup step. Skip any phases or steps between this phase or step and the cleanup step.

712.2
-----

No player gets priority during this process, so triggered abilities are not put onto the stack. If any triggered abilities have triggered between the spell or ability resolving and the cleanup step ending, those abilities are put onto the stack during the cleanup step, then the active player gets priority and players can cast spells and activate abilities. Then there will be another cleanup step before the turn finally ends. If no triggered abilities have triggered during this process, no player gets priority during the cleanup step.  See rule 514, 514.

712.3
-----

Even though the turn ends, "at the beginning of the end step" triggered abilities don't trigger because the end step is skipped.

.. _restarting:

Restarting the Game
===================

713.1
-----

One card (Karn Liberated) restarts the game. A game that is restarted immediately ends. No players in that game win, lose, or draw that game. All players in that game when it ended then start a new game following the procedures set forth in rule 103, 103. with the following exception:

    a. The starting player in the new game is the player who controlled the spell or ability that restarted the game.

713.2
-----

All *Magic* cards involved in the game that was restarted when it ended, including phased-out permanents and nontraditional *Magic* cards, are involved in the new game, even if those cards were not originally involved in the restarted game. Ownership of cards in the new game doesn't change, regardless of their location when the new game begins.

.. admonition:: Example

    A player casts Living Wish, bringing a creature card into the game from outside the game. Then that game is restarted. The creature card will be part of that player's library when the new game begins.

713.3
-----

Because each player draws seven cards when the new game begins, any player with fewer than seven cards in his or her library will lose the game when state-based actions are checked during the upkeep step of the first turn, regardless of any mulligans that player takes. (See rule 704, 704.)

713.4
-----

The effect that restarts the game finishes resolving just before the first turn's untap step. If the spell or ability that generated that effect has additional instructions, those instructions are followed at this time. No player has priority, and any triggered abilities that trigger as a result will go on the stack the next time a player receives priority, usually during the first turn's upkeep step.

713.5
-----

Effects may exempt certain cards from the procedure that restarts the game. These cards are not in their owner's deck as the new game begins.

    a. In a Commander game, a commander that has been exempted from the procedure that restarts the game won't begin the new game in the command zone.  However, it remains that deck's commander for the new game. See rule 903, 903.

713.6
-----

If a *Magic* subgame (see rule 714) is restarted, the main game is unaffected. Main-game effects that refer to the winner or loser of the subgame now refer to the winner or loser of the restarted subgame.

713.7
-----

If a multiplayer game using the limited range of influence option (see rule 801, Limited Range of Influence Option) is restarted, all players in the game are involved, regardless of the range of influence of the player who controls the ability that restarted the game.

.. _subgames:

Subgames
========

714.1
-----

One card (Shahrazad) allows players to play a *Magic* subgame.

    a. A "subgame" is a completely separate *Magic* game created by an effect.  Essentially, it's a game within a game. The "main game" is the game in which the spell or ability that created the subgame was cast or activated. The main game is temporarily discontinued while the subgame is in progress. It resumes when the subgame ends.
    b. No effects or definitions created in either the main game or the subgame have any meaning in the other, except as defined by the effect that created the subgame. For example, the effect may say that something happens in the main game to the winner or loser of the subgame.

714.2
-----

As the subgame starts, an entirely new set of game zones is created.  Each player takes all the cards in his or her main-game library, moves them to his or her subgame library, and shuffles them. No other cards in a main-game zone are moved to their corresponding subgame zone, except as specified in rules 714.2a-d. Randomly determine which player goes first. The subgame proceeds like a normal game, following all other rules in rule 103, 103.

    a. As a subgame of a Planechase game starts, each player moves his or her planar deck from the main-game command zone to the subgame command zone and shuffles it. (Face-up plane cards remain in the main-game command zone.)
    b. As a subgame of a Vanguard game starts, each player moves his or her vanguard card from the main-game command zone to the subgame command zone.
    c. As a subgame of a Commander game starts, each player moves his or her commander from the main-game command zone (if it's there) to the subgame command zone.
    d. As a subgame of an Archenemy game starts, the archenemy moves his or her scheme deck from the main-game command zone to the subgame command zone and shuffles it. (Face-up scheme cards remain in the main-game command zone.)

714.3
-----

Because each player draws seven cards when a game begins, any player with fewer than seven cards in his or her deck will lose the subgame when state-based actions are checked during the upkeep step of the first turn, regardless of any mulligans that player takes. (See rule 704, 704.)

714.4
-----

All objects in the main game and all cards outside the main game are considered outside the subgame (except those specifically brought into the subgame). All players not currently in the subgame are considered outside the subgame.

    a. Some effects can bring cards into a game from outside of it. If a card is brought into a subgame from a main game, abilities in the main game that trigger on objects leaving a main-game zone will trigger, but they won't be put onto the stack until the main game resumes.

714.5
-----

At the end of a subgame, each player takes all cards he or she owns that are in the subgame other than those in the subgame command zone, puts them into his or her main-game library, then shuffles them. This includes cards in the subgame's exile zone. Except as specified in rules 714.5a-c, all other objects in the subgame cease to exist, as do the zones created for the subgame. The main game continues from the point at which it was discontinued: First, the spell or ability that created the subgame finishes resolving, even if it was created by a spell card that's no longer on the stack. Then, if any main-game abilities triggered while the subgame was in progress due to cards being removed from the main game, those abilities are put onto the stack.

    .. admonition:: Example

        If a card was brought into the subgame either from the main game or from outside the main game, that card will be put into its owner's main-game library when the subgame ends.

    a. At the end of a subgame of a Planechase game, the face-up plane card is turned face down and put on the bottom of its owner's planar deck. Then each player moves his or her planar deck from the subgame command zone to the main-game command zone and shuffles it.
    b. At the end of a subgame of a Vanguard game, each player moves his or her vanguard card from the subgame command zone to the main-game command zone.
    c. At the end of a subgame of a Commander game, each player moves his or her commander from the subgame command zone (if it's there) to the main-game command zone.

714.6
-----

A subgame can be created within a subgame. The existing subgame becomes the main game in relation to the new subgame.

.. _shortcuts:

Taking Shortcuts
================

715.1
-----

When playing a game, players typically make use of mutually understood shortcuts rather than explicitly identifying each game choice (either taking an action or passing priority) a player makes.

    a. The rules for taking shortcuts are largely unformalized. As long as each player in the game understands the intent of each other player, any shortcut system they use is acceptable.
    b. Occasionally the game gets into a state in which a set of actions could be repeated indefinitely (thus creating a "loop"). In that case, the shortcut rules can be used to determine how many times those actions are repeated without having to actually perform them, and how the loop is broken.

715.2
-----

Taking a shortcut follows the following procedure.

    a. At any point in the game, the player with priority may suggest a shortcut by describing a sequence of game choices, for all players, that may be legally taken based on the current game state and the predictable results of the sequence of choices. This sequence may be a non-repetitive series of choices, a loop that repeats a specified number of times, multiple loops, or nested loops, and may even cross multiple turns. It can't include conditional actions, where the outcome of a game event determines the next action a player takes. The ending point of this sequence must be a place where a player has priority, though it need not be the player proposing the shortcut.

        .. admonition:: Example

            A player controls a creature enchanted by Presence of Gond, which grants the creature the ability "|T|: Put a 1/1 green Elf Warrior creature token onto the battlefield," and another player controls Intruder Alarm, which reads, in part, "Whenever a creature enters the battlefield, untap all creatures." When the player has priority, he may suggest "I'll create a million tokens," indicating the sequence of activating the creature's ability, all players passing priority, letting the creature's ability resolve and put a token onto the battlefield (which causes Intruder Alarm's ability to trigger), Intruder Alarm's controller putting that triggered ability on the stack, all players passing priority, Intruder Alarm's triggered ability resolving, all players passing priority until the player proposing the shortcut has priority, and repeating that sequence 999,999 more times, ending just after the last token-creating ability resolves.

    b. Each other player, in turn order starting after the player who suggested the shortcut, may either accept the proposed sequence, or shorten it by naming a place where he or she will make a game choice that's different than what's been proposed. (The player doesn't need to specify at this time what the new choice will be.) This place becomes the new ending point of the proposed sequence.

        .. admonition:: Example

            The active player draws a card during her draw step, then says, "Go." The nonactive player is holding Into the Fray (an instant that says "Target creature attacks this turn if able") and says, "I'd like to cast a spell during your beginning of combat step." The current proposed shortcut is that all players pass priority at all opportunities during the turn until the nonactive player has priority during the beginning of combat step.

    c. Once the last player has either accepted or shortened the shortcut proposal, the shortcut is taken. The game advances to the last proposed ending point, with all game choices contained in the shortcut proposal having been taken. If the shortcut was shortened from the original proposal, the player who now has priority must make a different game choice than what was originally proposed for that player.

715.3
-----

Sometimes a loop can be fragmented, meaning that each player involved in the loop performs an independent action that results in the same game state being reached multiple times. If that happens, the active player (or, if the active player is not involved in the loop, the first player in turn order who is involved) must then make a different game choice so the loop does not continue.

.. admonition:: Example

    In a two-player game, the active player controls a creature with the ability "|0|: [This creature] gains flying," the nonactive player controls a permanent with the ability "|0|: Target creature loses flying," and nothing in the game cares how many times an ability has been activated. Say the active player activates his creature's ability, it resolves, then the nonactive player activates her permanent's ability targeting that creature, and it resolves. This returns the game to a game state it was at before. The active player must make a different game choice (in other words, anything other than activating that creature's ability again). The creature doesn't have flying.  Note that the nonactive player could have prevented the fragmented loop simply by not activating her permanent's ability, in which case the creature would have had flying. The nonactive player always has the final choice and is therefore able to determine whether the creature has flying.

715.4
-----

If a loop contains only mandatory actions, the game is a draw. (See rules 104.4b and 104.4f.)

715.5
-----

No player can be forced to perform an action that would end a loop other than actions called for by objects involved in the loop.

.. admonition:: Example

    A player controls Seal of Cleansing, an enchantment that reads, "Sacrifice Seal of Cleansing: Destroy target artifact or enchantment." A mandatory loop that involves an artifact begins. The player is not forced to sacrifice Seal of Cleansing to destroy the artifact and end the loop.

715.6
-----

If a loop contains an effect that says "[A] unless [B]," where [A] and [B] are each actions, no player can be forced to perform [B] to break the loop.  If no player chooses to perform [B], the loop will continue as though [A] were mandatory.

.. _illegal-actions:

Handling Illegal Actions
========================

716.1
-----

If a player realizes that he or she can't legally take an action after starting to do so, the entire action is reversed and any payments already made are canceled. No abilities trigger and no effects apply as a result of an undone action. If the action was casting a spell, the spell returns to the zone it came from. The player may also reverse any legal mana abilities activated while making the illegal play, unless mana from them or from any triggered mana abilities they triggered was spent on another mana ability that wasn't reversed. Players may not reverse actions that moved cards to a library, moved cards from a library to any zone other than the stack, or caused a library to be shuffled.

716.2
-----

When reversing illegal spells and abilities, the player who had priority retains it and may take another action or pass. The player may redo the reversed action in a legal way or take any other action allowed by the rules.
