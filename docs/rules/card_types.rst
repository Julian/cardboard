:tocdepth: 2

.. _card-types:

**********
Card Types
**********

.. _card-general:

General
=======

300.1
-----

The card types are artifact, creature, enchantment, instant, land, plane, planeswalker, scheme, sorcery, tribal, and vanguard.

300.2
-----

Some objects have more than one card type (for example, an artifact creature). Such objects combine the aspects of each of those card types, and are subject to spells and abilities that affect either or all of those card types.

    a. An object that's both a land and another card type (for example, an artifact land) can only be played as a land. It can't be cast as a spell.
    b. Each tribal card has another card type. Casting and resolving a tribal card follow the rules for casting and resolving a card of the other card type.

Artifacts
=========

301.1
-----

A player who has priority may cast an artifact card from his or her hand during a main phase of his or her turn when the stack is empty. Casting an artifact as a spell uses the stack. (See rule 601, "Casting Spells.")

301.2
-----

When an artifact spell resolves, its controller puts it onto the battlefield under his or her control.

301.3
-----

Artifact subtypes are always a single word and are listed after a long dash: "Artifact -- Equipment." Artifact subtypes are also called artifact types. Artifacts may have multiple subtypes. See rule 204.3f for the complete list of artifact types.

301.4
-----

Artifacts have no characteristics specific to their card type. Most artifacts have no colored mana symbols in their mana costs, and are the:ref:ore colorless. However, there is no correlation between being colorless and being an artifact: artifacts may be colored, and colorless objects may be card types other than artifact.

301.5
-----

Some artifacts have the subtype "Equipment." An Equipment can be attached to a creature. It can't legally be attached to an object that isn't a creature.

    a. The creature an Equipment is attached to is called the "equipped creature." The Equipment is attached to, or "equips," that creature.
    b. An Equipment is cast and enters the battlefield just like any other artifact. An Equipment doesn't enter the battlefield attached to a creature.  The equip keyword ability attaches the Equipment to a creature you control (see rule 702.6, "Equip"). Control of the creature matters only when the equip ability is activated and when it resolves. Spells and other abilities may also attach an Equipment to a creature. If an effect attempts to attach an Equipment to an object that can't be equipped by it, the Equipment doesn't move.
    c. An Equipment that's also a creature can't equip a creature. An Equipment that loses the subtype "Equipment" can't equip a creature. An Equipment can't equip itself. An Equipment that equips an illegal or nonexistent permanent becomes unattached from that permanent but remains on the battlefield. (This is a state-based action. See rule 704, "State-Based Actions.")
    d. An Equipment's controller is separate from the equipped creature's controller; the two need not be the same. Changing control of the creature doesn't change control of the Equipment, and vice versa. Only the Equipment's controller can activate its abilities. However, if the Equipment grants an ability to the equipped creature (with "gains" or "has"), the equipped creature's controller is the only one who can activate that ability.

301.6
-----

Some artifacts have the subtype "Fortification." A Fortification can be attached to a land. It can't legally be attached to an object that isn't a land. Fortification's analog to the equip keyword ability is the fortify keyword ability. Rules 301.5a-d apply to Fortifications in relation to lands just as they apply to Equipment in relation to creatures, with one clarification relating to rule 301.5c: a Fortification that's also a creature (not a land) can't fortify a land. (See rule 702.65, "Fortify.")

301.7
-----

If a non-Equipment permanent has an ability that :ref:ers to the "equipped creature," that phrase doesn't refer to any creature. Similarly, a non-Fortification permanent that has an ability that refers to the "fortified land" doesn't refer to any land.

Creatures
=========

302.1
-----

A player who has priority may cast a creature card from his or her hand during a main phase of his or her turn when the stack is empty. Casting a creature as a spell uses the stack. (See rule 601, "Casting Spells.")

302.2
-----

When a creature spell resolves, its controller puts it onto the battlefield under his or her control.

302.3
-----

Creature subtypes are always a single word and are listed after a long dash: "Creature -- Human Soldier," "Artifact Creature -- Golem," and so on.  Creature subtypes are also called creature types. Creatures may have multiple subtypes. See rule 204.3k for the complete list of creature types.

.. admonition:: Example

    "Creature -- Goblin Wizard" means the card is a creature with the subtypes Goblin and Wizard.

302.4
-----

Power and toughness are characteristics only creatures have.

    a. A creature's power is the amount of damage it deals in combat.
    b. A creature's toughness is the amount of damage needed to destroy it.
    c. To determine a creature's power and toughness, start with the numbers printed in its lower right corner, then apply any applicable continuous effects. (See rule 613, "Interaction of Continuous Effects.")

302.5
-----

Creatures can attack and block. (See rule 508, "Declare Attackers Step," and rule 509, "Declare Blockers Step.")

302.6
-----

A creature's activated ability with the tap symbol or the untap symbol in its activation cost can't be activated unless the creature has been under its controller's control continuously since his or her most recent turn began.  A creature can't attack unless it has been under its controller's control continuously since his or her most recent turn began. This rule is informally called the "summoning sickness" rule.

302.7
-----

Damage dealt to a creature by a source with neither wither nor infect is marked on that creature (see rule 119.3). If the total damage marked on that creature is greater than or equal to its toughness, that creature has been dealt lethal damage and is destroyed as a state-based action (see rule 704, "State-Based Actions").  All damage marked on a creature is removed when it regenerates (see rule 701.11, "Regenerate") and during the cleanup step (see rule 514.2).

Enchantments
============

303.1
-----

A player who has priority may cast an enchantment card from his or her hand during a main phase of his or her turn when the stack is empty. Casting an enchantment as a spell uses the stack. (See rule 601, "Casting Spells.")

303.2
-----

When an enchantment spell resolves, its controller puts it onto the battlefield under his or her control.

303.3
-----

Enchantment subtypes are always a single word and are listed after a long dash: "Enchantment -- Shrine." Each word after the dash is a separate subtype. Enchantment subtypes are also called enchantment types. Enchantments may have multiple subtypes. See rule 204.3g for the complete list of enchantment types.

303.4
-----

Some enchantments have the subtype "Aura." An Aura enters the battlefield attached to an object or player. What an Aura can be attached to is restricted by its enchant keyword ability (see rule 702.5, "Enchant"). Other effects can limit what a permanent can be enchanted by.

    a. An Aura spell requires a target, which is restricted by its enchant ability.
    b. The object or player an Aura is attached to is called enchanted. The Aura is attached to, or "enchants," that object or player.
    c. If an Aura is enchanting an illegal object or player, the object it was attached to no longer exists, or the player it was attached to has left the game, the Aura is put into its owner's graveyard. (This is a state-based action. See rule 704, "State-Based Actions.")
    d. An Aura can't enchant itself. If this occurs somehow, the Aura is put into its owner's graveyard. An Aura that's also a creature can't enchant anything. If this occurs somehow, the Aura becomes unattached, then is put into its owner's graveyard. (These are state-based actions. See rule 704, "State-Based Actions.")
    e. An Aura's controller is separate from the enchanted object's controller or the enchanted player; the two need not be the same. If an Aura enchants an object, changing control of the object doesn't change control of the Aura, and vice versa. Only the Aura's controller can activate its abilities. However, if the Aura grants an ability to the enchanted object (with "gains" or "has"), the enchanted object's controller is the only one who can activate that ability.
    f. If an Aura is entering the battlefield under a player's control by any means other than by resolving as an Aura spell, and the effect putting it onto the battlefield doesn't specify the object or player the Aura will enchant, that player chooses what it will enchant as the Aura enters the battlefield.  The player must choose a legal object or player according to the Aura's enchant ability and any other applicable effects.
    g. If an Aura is entering the battlefield and there is no legal object or player for it to enchant, the Aura remains in its current zone, unless that zone is the stack. In that case, the Aura is put into its owner's graveyard instead of entering the battlefield.
    h. If an effect attempts to attach an Aura on the battlefield to an object or player, that object or player must be able to be enchanted by it. If the object or player can't be, the Aura doesn't move.
    i. If a non-Aura permanent has an ability that :ref:ers to the "enchanted [object or player]" that phrase doesn't refer to any object or player.

Instants
========

304.1
-----

A player who has priority may cast an instant card from his or her hand.  Casting an instant as a spell uses the stack. (See rule 601, "Casting Spells.")

304.2
-----

When an instant spell resolves, the actions stated in its rules text are followed. Then it's put into its owner's graveyard.

304.3
-----

Instant subtypes are always a single word and are listed after a long dash: "Instant -- Arcane." Each word after the dash is a separate subtype. The set of instant subtypes is the same as the set of sorcery subtypes; these subtypes are called spell types. Instants may have multiple subtypes. See rule 204.3j for the complete list of spell types.

304.4
-----

Instants can't enter the battlefield. If an instant would enter the battlefield, it remains in its previous zone instead.

304.5
-----

If text states that a player may do something "any time he or she could cast an instant," it means only that the player must have priority. The player doesn't need to have an instant he or she could actually cast. Effects that would prevent that player from casting a spell or casting an instant don't affect the player's capability to perform that action (unless the action is actually casting a spell or casting an instant).

Lands
=====

305.1
-----

A player who has priority may play a land card from his or her hand during a main phase of his or her turn when the stack is empty. Playing a land is a special action; it doesn't use the stack (see rule 115). Rather, the player simply puts the land onto the battlefield. Since the land doesn't go on the stack, it is never a spell, and players can't respond to it with instants or activated abilities.

305.2
-----

A player may normally play only one land during his or her turn; however, continuous effects may increase this number. If any such effects exist, the player announces which effect, or this rule, applies to each land play as it happens.

305.3
-----

A player can't play a land, for any reason, if it isn't his or her turn.  Ignore any part of an effect that instructs a player to do so. Similarly, a player can't play a land, for any reason, if that player has used all of his or her land plays for that turn. Ignore any part of an effect that instructs a player to do so.

305.4
-----

Effects may also allow players to "put" lands onto the battlefield. This isn't the same as "playing a land" and doesn't count as a player's one land played during his or her turn.

305.5
-----

Land subtypes are always a single word and are listed after a long dash.  Land subtypes are also called land types. Lands may have multiple subtypes. See rule 204.3h for the complete list of land types.

.. admonition:: Example

    "Basic Land -- Mountain" means the card is a land with the subtype Mountain.

305.6
-----

The basic land types are Plains, Island, Swamp, Mountain, and Forest. If an object uses the words "basic land type," it's :ref:erring to one of these subtypes. A land with a basic land type has the intrinsic ability "|T|: Add [mana symbol] to your mana pool," even if the text box doesn't actually contain that text or the object has no text box. For Plains, [mana symbol] is |W|; for Islands, |U|; for Swamps, |B|; for Mountains, |R|; and for Forests, |G|. See rule 107.4a. Also see rule 605, "Mana Abilities."

305.7
-----

If an effect sets a land's subtype to one or more of the basic land types, the land no longer has its old land type. It loses all abilities generated from its rules text and its old land types, and it gains the appropriate mana ability for each new basic land type. Note that this doesn't remove any abilities that were granted to the land by other effects. Setting a land's subtype doesn't add or remove any card types (such as creature) or supertypes (such as basic, legendary, and snow) the land may have. If a land gains one or more land types in addition to its own, it keeps its land types and rules text, and it gains the new land types and mana abilities.

305.8
-----

Any land with the supertype "basic" is a basic land. Any land that doesn't have this supertype is a nonbasic land, even if it has a basic land type.

305.9
-----

If an object is both a land and another card type, it can be played only as a land. It can't be cast as a spell.

Planeswalkers
=============

306.1
-----

A player who has priority may cast a planeswalker card from his or her hand during a main phase of his or her turn when the stack is empty. Casting a planeswalker as a spell uses the stack. (See rule 601, "Casting Spells.")

306.2
-----

When a planeswalker spell resolves, its controller puts it onto the battlefield under his or her control.

306.3
-----

Planeswalker subtypes are always a single word and are listed after a long dash: "Planeswalker -- Jace." Each word after the dash is a separate subtype. Planeswalker subtypes are also called planeswalker types.  Planeswalkers may have multiple subtypes. See rule 204.3i for the complete list of planeswalker types.

306.4
-----

If two or more planeswalkers that share a planeswalker type are on the battlefield, all are put into their owners' graveyards as a state-based action.  This is called the "planeswalker uniqueness rule." See rule 704, "State-Based Actions."

306.5
-----

Loyalty is a characteristic only planeswalkers have.

    a. The loyalty of a planeswalker not on the battlefield is equal to the number printed in its lower right corner.
    b. A planeswalker is treated as if its text box included, "This permanent enters the battlefield with a number of loyalty counters on it equal to its printed loyalty number." This ability creates a replacement effect (see rule 614.1c).
    c. The loyalty of a planeswalker on the battlefield is equal to the number of loyalty counters on it.
    d. Each planeswalker has a number of loyalty abilities, which are activated abilities with loyalty symbols in their costs. Loyalty abilities follow special rules: A player may activate a loyalty ability of a permanent he or she controls any time he or she has priority and the stack is empty during a main phase of his or her turn, but only if none of that permanent's loyalty abilities have been activated that turn. See rule 606, "Loyalty Abilities."

306.6
-----

Planeswalkers can be attacked. (See rule 508, "Declare Attackers Step.")

306.7
-----

If noncombat damage would be dealt to a player by a source controlled by an opponent, that opponent may have that source deal that damage to a planeswalker the first player controls instead. This is a redirection effect (see rule 614.9) and is subject to the normal rules for ordering replacement effects (see rule 616). The opponent chooses whether to redirect the damage as the redirection effect is applied.

306.8
-----

Damage dealt to a planeswalker results in that many loyalty counters being removed from it.

306.9
-----

If a planeswalker's loyalty is 0, it's put into its owner's graveyard.  (This is a state-based action. See rule 704, "State-Based Actions.")

Sorceries
=========

307.1
-----

A player who has priority may cast a sorcery card from his or her hand during a main phase of his or her turn when the stack is empty. Casting a sorcery as a spell uses the stack. (See rule 601, "Casting Spells.")

307.2
-----

When a sorcery spell resolves, the actions stated in its rules text are followed. Then it's put into its owner's graveyard.

307.3
-----

Sorcery subtypes are always a single word and are listed after a long dash: "Sorcery -- Arcane." Each word after the dash is a separate subtype. The set of sorcery subtypes is the same as the set of instant subtypes; these subtypes are called spell types. Sorceries may have multiple subtypes. See rule 204.3j for the complete list of spell types.

307.4
-----

Sorceries can't enter the battlefield. If a sorcery would enter the battlefield, it remains in its previous zone instead.

307.5
-----

If a spell, ability, or effect states that a player can do something only "any time he or she could cast a sorcery," it means only that the player must have priority, it must be during the main phase of his or her turn, and the stack must be empty. The player doesn't need to have a sorcery he or she could actually cast. Effects that would prevent that player from casting a spell or casting a sorcery don't affect the player's capability to perform that action (unless the action is actually casting a spell or casting a sorcery).

    a. Similarly, if an effect checks to see if a spell was cast "any time a sorcery couldn't have been cast," it's checking only whether the spell's controller cast it without having priority, during a phase other than his or her main phase, or while another object was on the stack.

Tribals
=======

308.1
-----

Each tribal card has another card type. Casting and resolving a tribal card follows the rules for casting and resolving a card of the other card type.

308.2
-----

Tribal subtypes are always a single word and are listed after a long dash: "Tribal Enchantment -- Merfolk." The set of tribal subtypes is the same as the set of creature subtypes; these subtypes are called creature types.  Tribals may have multiple subtypes. See rule 204.3k for the complete list of creature types.

Planes
======

309.1
-----

Plane is a card type seen only on nontraditional *Magic* cards. Only the Planechase casual variant uses plane cards. See rule 901, "Planechase."

309.2
-----

Plane cards remain in the command zone throughout the game, both while they're part of a planar deck and while they're face up. They're not permanents. They can't be cast. If a plane card would leave the command zone, it remains in the command zone.

309.3
-----

Plane subtypes are listed after a long dash, and may be multiple words: "Plane -- Serra's Realm." All words after the dash are, collectively, a single subtype. Planar subtypes are called planar types. A plane can have only one subtype. See rule 204.3m for the complete list of planar types.

309.4
-----

A plane card may have any number of static, triggered, and/or activated abilities. As long as a plane card is face up in the command zone, its static abilities affect the game, its triggered abilities may trigger, and its activated abilities may be activated.

309.5
-----

The controller of a face-up plane card is the player designated as the planar controller. Normally, the planar controller is whoever the active player is. However, if the current planar controller would leave the game, instead the next player in turn order that wouldn't leave the game becomes the planar controller, then the old planar controller leaves the game. The new planar controller retains that designation until he or she leaves the game or a different player becomes the active player, whichever comes first.

309.6
-----

A plane card is treated as if its text box included "When you roll |PW|, put this card on the bottom of its owner's planar deck face down, then move the top card of your planar deck face up." This is called the "planeswalking ability." A face-up plane card that's turned face down becomes a new object.

309.7
-----

Each plane card has a triggered ability that triggers "Whenever you roll |C|." These are called "chaos abilities." Each one is indicated by a |C| to its left, though the symbol itself has no special rules meaning.

Vanguards
=========

310.1
-----

Vanguard is a card type seen only on nontraditional *Magic* cards. Only the Vanguard casual variant uses vanguard cards. See rule 902, "Vanguard."

310.2
-----

Vanguard cards remain in the command zone throughout the game. They're not permanents. They can't be cast. If a vanguard card would leave the command zone, it remains in the command zone.

310.3
-----

Vanguard cards have no subtypes.

310.4
-----

A vanguard card may have any number of static, triggered, and/or activated abilities. As long as a vanguard card is in the command zone, its static abilities affect the game, its triggered abilities may trigger, and its activated abilities may be activated.

310.5
-----

The owner of a vanguard card is the player who started the game with it in the command zone. The controller of a face-up vanguard card is its owner.

310.6
-----

Each vanguard card has a hand modifier printed in its lower left corner.  This is a number preceded by a plus sign, a number preceded by a minus sign, or a zero. This modifier is applied to the maximum hand size of the vanguard card's owner (normally seven) to determine both how many cards that player draws at the beginning of the game and his or her maximum hand size.

310.7
-----

Each vanguard card has a life modifier printed in its lower right corner. This is a number preceded by a plus sign, a number preceded by a minus sign, or a zero. This modifier is applied to the starting life total of the vanguard card's owner (normally 20) to determine how much life that player begins the game with.

Schemes
=======

311.1
-----

Scheme is a card type seen only on nontraditional *Magic* cards. Only the Archenemy casual variant uses scheme cards. See rule 904, "Archenemy."

311.2
-----

Scheme cards remain in the command zone throughout the game, both while they're part of a scheme deck and while they're face up. They're not permanents. They can't be cast. If a scheme card would leave the command zone, it remains in the command zone.

311.3
-----

Scheme cards have no subtypes.

311.4
-----

A scheme card may have any number of static, triggered, and/or activated abilities. As long as a scheme card is face up in the command zone, its static abilities affect the game, its triggered abilities may trigger, and its activated abilities may be activated.

311.5
-----

The owner of a scheme card is the player who started the game with it in the command zone. The controller of a face-up scheme card is its owner.

311.6
-----

If a non-ongoing scheme card is face up in the command zone, and it isn't the source of a triggered ability that has triggered but not yet left the stack, that scheme card is turned face down and put on the bottom of its owner's scheme deck the next time a player would receive priority. (This is a state-based action. See rule 704.)

311.7
-----

If an ability of a scheme card includes the text "this scheme," it means the scheme card in the command zone that's the source of that ability. This is an exception to rule 109.2.
