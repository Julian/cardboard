:tocdepth: 2

.. _card-parts:

***************
Parts of a Card
***************

.. _parts-general:

General
=======

200.1
-----

The parts of a card are name, mana cost, illustration, type line, expansion symbol, text box, power and toughness, loyalty, hand modifier, life modifier, illustration credit, legal text, and collector number. Some cards may have more than one of any or all of these parts.

200.2
-----

Some parts of a card are also characteristics of the object that has them. See rule 109.3.

200.3
-----

Some objects that aren't cards (tokens, copies of cards, and copies of spells) have some of the parts of a card, but only the ones that are also characteristics. See rule 110.5 and rule 706.

.. _name:

Name
====

201.1
-----

The name of a card is printed on its upper left corner.

201.2
-----

Two objects have the same name if the English versions of their names are identical.

201.3
-----

If an effect instructs a player to name a card, the player must choose the name of a card that exists in the Oracle card reference (see rule 108.1) and is legal in the format of the game the player is playing. (See rule 100.6.) If the player wants to name a split card, the player must name both halves of the split card. (See rule 708.) If the player wants to name a flip card's alternative name, the player may do so. (See rule 709.) A player may not choose the name of a token unless it's also the name of a card.

201.4
-----

Text that refers to the object it's on by name means just that particular object and not any other objects with that name, regardless of any name changes caused by game effects.

    a. If an ability's effect grants another ability to an object, and that second ability refers to that first ability's source by name, the name refers only to the specific object that is that first ability's source, not to any other object with the same name.

        .. admonition:: Example

            Saproling Burst has an ability that reads "Remove a fade counter from Saproling Burst: Put a green Saproling creature token onto the battlefield. It has 'This creature's power and toughness are each equal to the number of fade counters on Saproling Burst.'" The ability granted to the token only looks at the Saproling Burst that created the token, not at any other Saproling Burst on the battlefield.

    b. If an ability of an object refers to that object by name, and an object with a different name gains that ability, all instances of the first name in the gained ability should be treated as the second name.

        .. admonition:: Example

            Quicksilver Elemental says, in part, "|U|: Quicksilver Elemental gains all activated abilities of target creature until end of turn." If it gains an ability that says "|B|: Regenerate Drudge Skeletons," activating that ability will regenerate Quicksilver Elemental, not the Drudge Skeletons it gained the ability from.

        .. admonition:: Example

            Glacial Ray is an instant with "splice onto Arcane" that says "Glacial Ray deals 2 damage to target creature or player." If it's spliced onto a Kodama's Reach, that Kodama's Reach deals 2 damage to the target creature or player.

        .. admonition:: Example

            Dimir Doppelganger says "|1|\ |U|\ |B|: Exile target creature card from a graveyard. Dimir Doppelganger becomes a copy of that card and gains this ability." Dimir Doppelganger's ability is activated targeting a Runeclaw Bear card. The Doppelganger becomes a copy of Runeclaw Bear and gains an ability that should be treated as saying "|1|\ |U|\ |B|: Exile target creature card from a graveyard. Runeclaw Bear becomes a copy of that card and gains this ability."

    c. Text printed on some legendary cards refers to that card by a shortened version of its name. This occurs only on a second reference or later; first references always use the card's full name. Instances of a card's shortened name used in this manner are treated as though they used the card's full name.

201.5
-----

If an ability of an object uses a phrase such as "this [something]" to identify an object, where [something] is a characteristic, it is referring to that particular object, even if it isn't the appropriate characteristic at the time.

.. admonition:: Example

    An ability reads "Target creature gets +2/+2 until end of turn.  Destroy that creature at the beginning of the next end step." The ability will destroy the object it gave +2/+2 to even if that object isn't a creature at the beginning of the next end step.

.. _mana-cost:

Mana Cost and Color
===================

202.1
-----

A card's mana cost is indicated by mana symbols near the top of the card. (See rule 107.4.) On most cards, these symbols are printed in the upper right corner. Some cards from the *Future Sight* set have alternate frames in which the mana symbols appear to the left of the illustration.

    a. The mana cost of an object represents what a player must spend from his or her mana pool to cast that card. Unless an object's mana cost includes Phyrexian mana symbols (see rule 107.4f), paying that mana cost requires matching the color of any colored mana symbols as well as paying the generic mana indicated in the cost.
    b. Some objects have no mana cost. This normally includes all land cards, any other cards that have no mana symbols where their mana cost would appear, tokens (unless the effect that creates them specifies otherwise), and nontraditional *Magic* cards. Having no mana cost represents an unpayable cost (see rule 117.6). Note that lands are played without paying any costs (see rule 305, "Lands").

202.2
-----

An object is the color or colors of the mana symbols in its mana cost, regardless of the color of its frame.

    a. The five colors are white, blue, black, red, and green. The white mana symbol is represented by |W|, blue by |U|, black by |B|, red by |R|, and green by |G|.

        .. admonition:: Example

            An object with a mana cost of |2|\ |W| is white, an object with a mana cost of |2| is colorless, and one with a mana cost of |2|\ |W|\ |B| is both white and black.

    b. Objects with no colored mana symbols in their mana costs are colorless.
    c. An object with two or more different colored mana symbols in its mana cost is each of the colors of those mana symbols. Most multicolored cards are printed with a gold frame, but this is not a requirement for a card to be multicolored.
    d. An object with one or more hybrid mana symbols and/or Phyrexian mana symbols in its mana cost is all of the colors of those mana symbols, in addition to any other colors the object might be. (Most cards with hybrid mana symbols in their mana costs are printed in a two-tone frame. See rule 107.4e.)
    e. Effects may change an object's color, give a color to a colorless object, or make a colored object become colorless; see rule 105.3.

202.3
-----

The converted mana cost of an object is a number equal to the total amount of mana in its mana cost, regardless of color.

    .. admonition:: Example

        A mana cost of |3|\ |U|\ |U| translates to a converted mana cost of 5.

    a. The converted mana cost of an object with no mana cost is 0.
    b. When calculating the converted mana cost of an object with an |X| in its mana cost, X is treated as 0 while the object is not on the stack, and X is treated as the number chosen for it while the object is on the stack.
    c. When calculating the converted mana cost of an object with a hybrid mana symbol in its mana cost, use the largest component of each hybrid symbol.

        .. admonition:: Example

            The converted mana cost of a card with mana cost |1|\ |W/U|\ |W/U| is 3.

        .. admonition:: Example

            The converted mana cost of a card with mana cost |2/B|\ |2/B|\ |2/B| is 6.

    d. Each Phyrexian mana symbol in a card's mana cost contributes 1 to its converted mana cost.

        .. admonition:: Example

            The converted mana cost of a card with mana cost |1|\ |W/P|\ |W/P| is 3.

202.4
-----

Any additional cost listed in an object's rules text or imposed by an effect isn't part of the mana cost. (See rule 601, "Casting Spells.") Such costs are paid at the same time as the spell's other costs.

.. _illustration:

Illustration
============

203.1
-----

The illustration is printed on the upper half of a card and has no effect on game play. For example, a creature doesn't have the flying ability unless stated in its rules text, even if it's depicted as flying.

.. _type-line:

Type Line
=========

204.1
-----

The type line is printed directly below the illustration. It contains the card's card type(s). It also contains the card's subtype(s) and supertype(s), if applicable.

    a. Some effects set an object's card type. In such cases, the new card type(s) replaces any existing card types. Counters, effects, and damage marked on the object remain with it, even if they are meaningless to the new card type. Similarly, when an effect sets one or more of an object's subtypes, the new subtype(s) replaces any existing subtypes from the appropriate set (creature types, land types, artifact types, enchantment types, planeswalker types, or spell types). If an object's card type is removed, the subtypes correlated with that card type will remain if they are also the subtypes of a card type the object currently has; otherwise, they are also removed for the entire time the object's card type is removed. Removing an object's subtype doesn't affect its card types at all.
    b. Some effects change an object's card type, supertype, or subtype but specify that the object retains a prior card type, supertype, or subtype. In such cases, all the object's prior card types, supertypes, and subtypes are retained. This rule applies to effects that use the phrase "in addition to its types" or that state that something is "still a [type, supertype, or subtype]." Some effects state that an object becomes an "artifact creature"; these effects also allow the object to retain all of its prior card types and subtypes.

        .. admonition:: Example

            An ability reads, "All lands are 1/1 creatures that are still lands." The affected lands now have two card types: creature and land. If there were any lands that were also artifacts before the ability's effect applied to them, those lands would become "artifact land creatures," not just "creatures," or "land creatures." The effect allows them to retain both the card type "artifact" and the card type "land." In addition, each land affected by the ability retains any land types and supertypes it had before the ability took effect.

        .. admonition:: Example

            An ability reads, "All artifacts are 1/1 artifact creatures." If a permanent is both an artifact and an enchantment, it will become an "artifact enchantment creature."

204.2
-----

Card Types

    a. The card types are artifact, creature, enchantment, instant, land, plane, planeswalker, scheme, sorcery, tribal, and vanguard.

        .. _seealso::

            :ref:`card-types`

    b. Some objects have more than one card type (for example, an artifact creature). Such objects satisfy the criteria for any effect that applies to any of their card types.
    c. Tokens have card types even though they aren't cards. The same is true of copies of spells and copies of cards.

204.3
-----

Subtypes

    a. A card can have one or more subtypes printed on its type line.
    b. Subtypes of each card type except plane are always single words and are listed after a long dash. Each word after the dash is a separate subtype; such objects may have multiple types. Subtypes of planes are also listed after a long dash, but may be multiple words; all words after the dash are, collectively, a single subtype.

        .. admonition:: Example

            "Basic Land -- Mountain" means the card is a land with the subtype Mountain. "Creature -- Goblin Wizard" means the card is a creature with the subtypes Goblin and Wizard. "Artifact -- Equipment" means the card is an artifact with the subtype Equipment.

    c. If a card with multiple card types has one or more subtypes, each subtype is correlated to its appropriate card type.

        .. admonition:: Example

            Dryad Arbor's type line says "Land Creature -- Forest Dryad." Forest is a land type, and Dryad is a creature type.

    d. If an effect instructs a player to choose a subtype, that player must choose one, and only one, existing subtype, and the subtype he or she chooses must be for the appropriate card type. For example, the player can't choose a land type if an instruction requires choosing a creature type.

        .. admonition:: Example

            When choosing a creature type, "Merfolk" or "Wizard" is acceptable, but "Merfolk Wizard" is not. Words like "artifact," "opponent," "Swamp," or "truck" can't be chosen because they aren't creature types.

    e. Many cards were printed with subtypes that are now obsolete. Many cards have retroactively received subtypes. Use the Oracle card reference to determine what a card's subtypes are. (See rule 108.1.)
    f. Artifacts have their own unique set of subtypes; these subtypes are called artifact types. The artifact types are Contraption, Equipment (see rule 301.5), and Fortification (see rule 301.6).
    g. Enchantments have their own unique set of subtypes; these subtypes are called enchantment types. The enchantment types are Aura (see rule 303.4), and Shrine.
    h. Lands have their own unique set of subtypes; these subtypes are called land types. The land types are Desert, Forest, Island, Lair, Locus, Mine, Mountain, Plains, Power-Plant, Swamp, Tower, and Urza's.  Of that list, Forest, Island, Mountain, Plains, and Swamp are the basic land types. See rule 305.6.
    i. Planeswalkers have their own unique set of subtypes; these subtypes are called planeswalker types. The planeswalker types are Ajani, Bolas, Chandra, Elspeth, Garruk, Gideon, Jace, Karn, Koth, Liliana, Nissa, Sarkhan, Sorin, Tezzeret, and Venser.  If two or more planeswalkers that share a planeswalker type are on the battlefield, all are put into their owners' graveyards. This "planeswalker uniqueness rule" is a state-based action. See rule 704, "State-Based Actions."
    j. Instants and sorceries share their lists of subtypes; these subtypes are called spell types. The spell types are Arcane and Trap.
    k. Creatures and tribals share their lists of subtypes; these subtypes are called creature types. The creature types are Advisor, Ally, Angel, Anteater, Antelope, Ape, Archer, Archon, Artificer, Assassin, Assembly-Worker, Atog, Aurochs, Avatar, Badger, Barbarian, Basilisk, Bat, Bear, Beast, Beeble, Berserker, Bird, Blinkmoth, Boar, Bringer, Brushwagg, Camarid, Camel, Caribou, Carrier, Cat, Centaur, Cephalid, Chimera, Citizen, Cleric, Cockatrice, Construct, Coward, Crab, Crocodile, Cyclops, Dauthi, Demon, Deserter, Devil, Djinn, Dragon, Drake, Dreadnought, Drone, Druid, Dryad, Dwarf, Efreet, Elder, Eldrazi, Elemental, Elephant, Elf, Elk, Eye, Faerie, Ferret, Fish, Flagbearer, Fox, Frog, Fungus, Gargoyle, Germ, Giant, Gnome, Goat, Goblin, Golem, Gorgon, Graveborn, Gremlin, Griffin, Hag, Harpy, Hellion, Hippo, Hippogriff, Homarid, Homunculus, Horror, Horse, Hound, Human, Hydra, Hyena, Illusion, Imp, Incarnation, Insect, Jellyfish, Juggernaut, Kavu, Kirin, Kithkin, Knight, Kobold, Kor, Kraken, Lammasu, Leech, Leviathan, Lhurgoyf, Licid, Lizard, Manticore, Masticore, Mercenary, Merfolk, Metathran, Minion, Minotaur, Monger, Mongoose, Monk, Moonfolk, Mutant, Myr, Mystic, Nautilus, Nephilim, Nightmare, Nightstalker, Ninja, Noggle, Nomad, Octopus, Ogre, Ooze, Orb, Orc, Orgg, Ouphe, Ox, Oyster, Pegasus, Pentavite, Pest, Phelddagrif, Phoenix, Pincher, Pirate, Plant, Praetor, Prism, Rabbit, Rat, Rebel, Reflection, Rhino, Rigger, Rogue, Salamander, Samurai, Sand, Saproling, Satyr, Scarecrow, Scorpion, Scout, Serf, Serpent, Shade, Shaman, Shapeshifter, Sheep, Siren, Skeleton, Slith, Sliver, Slug, Snake, Soldier, Soltari, Spawn, Specter, Spellshaper, Sphinx, Spider, Spike, Spirit, Splinter, Sponge, Squid, Squirrel, Starfish, Surrakar, Survivor, Tetravite, Thalakos, Thopter, Thrull, Treefolk, Triskelavite, Troll, Turtle, Unicorn, Vampire, Vedalken, Viashino, Volver, Wall, Warrior, Weird, Whale, Wizard, Wolf, Wolverine, Wombat, Worm, Wraith, Wurm, Yeti, Zombie, and Zubera.

    m. Planes have their own unique set of subtypes; these subtypes are called planar types. The planar types are Alara, Arkhos, Bolas's Meditation Realm, Dominaria, Equilor, Iquatana, Ir, Kaldheim, Kamigawa, Karsus, Kinshala, Lorwyn, Luvion, Mercadia, Mirrodin, Moag, Muraganda, Phyrexia, Pyrulea, Rabiah, Rath, Ravnica, Segovia, Serra's Realm, Shadowmoor, Shandalar, Ulgrotha, Valla, Wildfire, and Zendikar.
    n. Neither vanguard cards nor scheme cards have subtypes.

204.4
-----

Supertypes

    a. A card can also have one or more supertypes. These are printed directly before its card types. The supertypes are basic, legendary, ongoing, snow, and world.
    b. An object's supertype is independent of its card type and subtype, even though some supertypes are closely identified with specific card types.  Changing an object's card types or subtypes won't change its supertypes.  Changing an object's supertypes won't change its card types or subtypes. When an object gains or loses a supertype, it retains any other supertypes it had.

        .. admonition:: Example

            An ability reads, "All lands are 1/1 creatures that are still lands." If any of the affected lands were legendary, they are still legendary.

    c. Any land with the supertype "basic" is a basic land. Any land that doesn't have this supertype is a nonbasic land, even if it has a basic land type.  Cards printed in sets prior to the *Eighth Edition* core set didn't use the word "basic" to indicate a basic land. Cards from those sets with the following names are basic lands and have received errata in the Oracle card reference accordingly: Forest, Island, Mountain, Plains, Swamp, Snow-Covered Forest, Snow-Covered Island, Snow-Covered Mountain, Snow-Covered Plains, and Snow-Covered Swamp.
    d. Any permanent with the supertype "legendary" is subject to the state-based action for legendary permanents, also called the "legend rule" (see rule 704.5k).
    e. Any permanent with the supertype "world" is subject to the state-based action for world permanents, also called the "world rule" (see rule 704.5m).
    f. Any permanent with the supertype "snow" is a snow permanent. Any permanent that doesn't have this supertype is a nonsnow permanent, regardless of its name.
    g. Any scheme card with the supertype "ongoing" is exempt from the state-based action for schemes (see rule 704.5w).

.. _expansion-symbol:

Expansion Symbol
================

205.1
-----

The expansion symbol indicates which *Magic* set a card is from. It's a small icon normally printed below the right edge of the illustration.

205.2
-----

The color of the expansion symbol indicates the rarity of the card within its set. A red-orange symbol indicates the card is mythic rare. A gold symbol indicates the card is rare. A silver symbol indicates the card is uncommon. A black or white symbol indicates the card is common or is a basic land. A purple symbol signifies a special rarity; to date, only the *Time Spiral*\ ® "timeshifted" cards, which were rarer than that set's rare cards, have had purple expansion symbols. (Prior to the *Exodus*\ ™ set, all expansion symbols were black, regardless of rarity. Also, prior to the *Sixth Edition* core set, with the exception of the Simplified Chinese *Fifth Edition* core set, *Magic* core sets didn't have expansion symbols at all.)

205.3
-----

A spell or ability that affects cards from a particular set checks only for that set's expansion symbol. A card reprinted in the core set or another expansion receives that set's expansion symbol. Any reprinted version of the card no longer counts as part of its original set unless it was reprinted with that set's expansion symbol.

205.4
-----

Players may include cards from any printing in their constructed decks if those cards appear in sets allowed in that format (or those cards are specifically allowed by the *Magic* Tournament Rules). See the Magic Tournament Rules <http://www.wizards.com/wpn/Events/Rules.aspx> for the current definitions of the constructed formats.

205.5
-----

The full list of expansions and expansion symbols can be found in the `Magic Products section <http://www.wizards.com/Magic/TCG/Article.aspx?x=mtg/tcg/products/allproducts)>`_ of the Wizards of the Coast website.

.. _text-box:

Text Box
========

206.1
-----

The text box is printed on the lower half of the card. It usually contains rules text defining the card's abilities.

.. _no-func-text-box:

206.2
-----

The text box may also contain italicized text that has no game function.

    a. Reminder text is italicized text within parentheses that summarizes a rule that applies to that card. It usually appears on the same line as the ability it's relevant to, but it may appear on its own line if it applies to an aspect of the card other than an ability.
    b. Flavor text is italicized text that, like the illustration, adds artistic appeal to the game. It appears below the rules text.
    c. An ability word appears in italics at the beginning of some abilities on cards. Ability words are similar to keywords in that they tie together cards that have similar functionality, but they have no special rules meaning and no individual entries in the Comprehensive Rules. The ability words are channel, chroma, domain, grandeur, hellbent, imprint, join forces, kinship, landfall, metalcraft, radiance, sweep, and threshold.

206.3
-----

A guild icon appears in the text box of many *Ravnica*\ ® block cards.  These cards either have the specified guild's exclusive mechanic or somehow relate to the two colors associated with that guild. Guild icons have no effect on game play. Similarly, a faction icon appears in the text box of most *Scars of Mirrodin*\ ™ block cards. These faction icons have no effect on game play.

206.4
-----

The chaos symbol |C| appears in the text box of each plane card to the left of a triggered ability that triggers whenever |C| is rolled on the planar die. The symbol itself has no special rules meaning.

.. _power-toughness:

Power/Toughness
===============

207.1
-----

A creature card has two numbers separated by a slash printed in its lower right corner. The first number is its power (the amount of damage it deals in combat); the second is its toughness (the amount of damage needed to destroy it). For example, 2/3 means the object has power 2 and toughness 3.  Power and toughness can be modified or set to particular values by effects.

207.2
-----

Rather than a fixed number, some creature cards have power and/or toughness that includes a star (*).

    a. The card may have a characteristic-defining ability that sets its power and/or toughness according to some stated condition. (See rule 604.3.) Such an ability is worded "[This creature's] [power or toughness] is equal to . . ." or "[This creature's] power and toughness are each equal to . . ." This ability functions everywhere, even outside the game. If the ability needs to use a number that can't be determined, including inside a calculation, use 0 instead of that number.

        .. admonition:: Example

            Lost Order of Jarkeld has power and toughness each equal to 1+*. It says "As Lost Order of Jarkeld enters the battlefield, choose an opponent" and "Lost Order of Jarkeld's power and toughness are each equal to 1 plus the number of creatures that opponent controls." While Lost Order of Jarkeld isn't on the battlefield, there won't be a chosen opponent. Its power and toughness will each be equal to 1 plus 0, so it's 1/1.

    b. The card may have a static ability that creates a replacement effect that sets the creature's power and toughness to one of a number of specific choices as it enters the battlefield or is turned face up. (See rule 614, "Replacement Effects.") Such an ability is worded "As [this creature] enters the battlefield . . . ," "As [this creature] is turned face up . . . ," or "[This creature] enters the battlefield as . . ." and lists two or more specific power and toughness values (and may also list additional characteristics). The characteristics chosen with these effects affect the creature's copiable values. (See rule 706.2.) While the card isn't on the battlefield, its power and toughness are each considered to be 0.

207.3
-----

A noncreature permanent has no power or toughness, even if it's a card with a power and toughness printed on it (such as a Licid that's become an Aura).

.. _loyalty:

Loyalty
=======

208.1
-----

Each planeswalker card has a loyalty number printed in its lower right corner. This indicates its loyalty while it's not on the battlefield, and it also indicates that the planeswalker enters the battlefield with that many loyalty counters on it.

208.2
-----

An activated ability with a loyalty symbol in its cost is a loyalty ability. Loyalty abilities follow special rules: A player may activate a loyalty ability of a permanent he or she controls any time he or she has priority and the stack is empty during a main phase of his or her turn, but only if none of that permanent's loyalty abilities have been activated that turn. See rule 606, "Loyalty Abilities."

.. _hand-modifier:

Hand Modifier
=============

209.1
-----

Each vanguard card has a hand modifier printed in its lower left corner.  This is a number preceded by a plus sign, a number preceded by a minus sign, or a zero. This modifier is applied to the maximum hand size of the vanguard card's owner (normally seven) to determine both how many cards that player draws at the beginning of the game and his or her maximum hand size.

.. _life-modifier:

Life Modifier
=============

210.1
-----

Each vanguard card has a life modifier printed in its lower right corner. This is a number preceded by a plus sign, a number preceded by a minus sign, or a zero. This modifier is applied to the starting life total of the vanguard card's owner (normally 20) to determine how much life that player begins the game with.

.. _below-text-box:

Information Below the Text Box
==============================

211.1
-----

Each card features text printed below the text box that has no effect on game play.

    a. The illustration credit for a card is printed on the first line below the text box. It follows the paintbrush icon or, on older cards, the abbreviation "Illus."
    b. Legal text (the fine print at the bottom of the card) lists the trademark and copyright information.
    c. Some card sets feature collector numbers. This information is printed in the form [card number]/[total cards in the set], immediately following the legal text.
