artifact = u"Artifact"
creature = u"Creature"
enchantment = u"Enchantment"
land = u"Land"
planeswalker = u"Planeswalker"

instant = u"Instant"
sorcery = u"Sorcery"

permanents = frozenset({artifact, creature, enchantment, land, planeswalker})
nonpermanents = frozenset({instant, sorcery})

all = permanents | nonpermanents
unimplemented = frozenset({u"Plane", u"Scheme", u"Tribal", u"Vanguard"})

supertypes = frozenset({u"Basic", u"Legendary", u"Ongoing", u"Snow", u"World"})
subtypes = {
    artifact : frozenset({u"Contraption", u"Equipment", u"Fortification"}),
    creature : frozenset({
        u"Advisor", u"Ally", u"Angel", u"Anteater", u"Antelope", u"Ape",
        u"Archer", u"Archon", u"Artificer", u"Assassin", u"Assembly-Worker",
        u"Atog", u"Aurochs", u"Avatar", u"Badger", u"Barbarian", u"Basilisk",
        u"Bat", u"Bear", u"Beast", u"Beeble", u"Berserker", u"Bird",
        u"Blinkmoth", u"Boar", u"Bringer", u"Brushwagg", u"Camarid", u"Camel",
        u"Caribou", u"Carrier", u"Cat", u"Centaur", u"Cephalid", u"Chimera",
        u"Citizen", u"Cleric", u"Cockatrice", u"Construct", u"Coward", u"Crab",
        u"Crocodile", u"Cyclops", u"Dauthi", u"Demon", u"Deserter", u"Devil",
        u"Djinn", u"Dragon", u"Drake", u"Dreadnought", u"Drone", u"Druid",
        u"Dryad", u"Dwarf", u"Efreet", u"Elder", u"Eldrazi", u"Elemental",
        u"Elephant", u"Elf", u"Elk", u"Eye", u"Faerie", u"Ferret", u"Fish",
        u"Flagbearer", u"Fox", u"Frog", u"Fungus", u"Gargoyle", u"Germ",
        u"Giant", u"Gnome", u"Goat", u"Goblin", u"Golem", u"Gorgon",
        u"Graveborn", u"Gremlin", u"Griffin", u"Hag", u"Harpy", u"Hellion",
        u"Hippo", u"Hippogriff", u"Homarid", u"Homunculus", u"Horror",
        u"Horse", u"Hound", u"Human", u"Hydra", u"Hyena", u"Illusion", u"Imp",
        u"Incarnation", u"Insect", u"Jellyfish", u"Juggernaut", u"Kavu",
        u"Kirin", u"Kithkin", u"Knight", u"Kobold", u"Kor", u"Kraken",
        u"Lammasu", u"Leech", u"Leviathan", u"Lhurgoyf", u"Licid", u"Lizard",
        u"Manticore", u"Masticore", u"Mercenary", u"Merfolk", u"Metathran",
        u"Minion", u"Minotaur", u"Monger", u"Mongoose", u"Monk", u"Moonfolk",
        u"Mutant", u"Myr", u"Mystic", u"Nautilus", u"Nephilim", u"Nightmare",
        u"Nightstalker", u"Ninja", u"Noggle", u"Nomad", u"Octopus", u"Ogre",
        u"Ooze", u"Orb", u"Orc", u"Orgg", u"Ouphe", u"Ox", u"Oyster",
        u"Pegasus", u"Pentavite", u"Pest", u"Phelddagrif", u"Phoenix",
        u"Pincher", u"Pirate", u"Plant", u"Praetor", u"Prism", u"Rabbit",
        u"Rat", u"Rebel", u"Reflection", u"Rhino", u"Rigger", u"Rogue",
        u"Salamander", u"Samurai", u"Sand", u"Saproling", u"Satyr",
        u"Scarecrow", u"Scorpion", u"Scout", u"Serf", u"Serpent", u"Shade",
        u"Shaman", u"Shapeshifter", u"Sheep", u"Siren", u"Skeleton", u"Slith",
        u"Sliver", u"Slug", u"Snake", u"Soldier", u"Soltari", u"Spawn",
        u"Specter", u"Spellshaper", u"Sphinx", u"Spider", u"Spike", u"Spirit",
        u"Splinter", u"Sponge", u"Squid", u"Squirrel", u"Starfish",
        u"Surrakar", u"Survivor", u"Tetravite", u"Thalakos", u"Thopter",
        u"Thrull", u"Treefolk", u"Triskelavite", u"Troll", u"Turtle",
        u"Unicorn", u"Vampire", u"Vedalken", u"Viashino", u"Volver", u"Wall",
        u"Warrior", u"Weird", u"Whale", u"Wizard", u"Wolf", u"Wolverine",
        u"Wombat", u"Worm", u"Wraith", u"Wurm", u"Yeti", u"Zombie", u"Zubera"
    }),
    enchantment : frozenset({u"Aura", u"Shrine"}),
    instant : frozenset({u"Arcane", u"Trap"}),

    u"Basic Land" : frozenset({
        u"Forest", u"Island", u"Mountain", u"Plains", u"Swamp"
    }),

    u"Non-Basic Land" : frozenset({
        u"Desert", u"Lair", u"Locus", u"Mine",
        u"Power-Plant", u"Tower", u"Urza's"
    }),

    planeswalker : frozenset({
        u"Ajani", u"Bolas", u"Chandra", u"Elspeth", u"Garruk", u"Gideon",
        u"Jace", u"Karn", u"Koth", u"Liliana", u"Nissa", u"Sarkhan", u"Sorin",
        u"Tezzeret", u"Venser"
    }),
}

subtypes[sorcery] = subtypes[instant]
subtypes[land] = subtypes[u"Basic Land"] | subtypes[u"Non-Basic Land"]
