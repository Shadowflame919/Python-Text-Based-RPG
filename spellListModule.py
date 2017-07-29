
import math
import random

# A list of every spell in the game, the first number in each array is the spells tier.
# All spells from the lowest tier must be found before any spells from the next tier
spellList = [
   #[tier,	name,						description,								MP,		effect/stats		] 
	[1, 	"Weak Healing Spell", 		"This spell gives you a little health", 	2,		["heal", 3, 5]		],
	[2,		"Medium Healing Spell", 	"This spell gives you some health.", 		4,		["heal", 6, 12]	],
	[3,		"Strong Healing Spell", 	"This spell heals you a lot.", 				6,		["heal", 10, 20]	],

	[2,		"Weak Leech Spell", 		"Steal a little health from the enemy.", 	3,		["leech", 2, 3]		],
	[3,		"Medium Leech Spell", 		"Steal some health from the enemy.", 		6,		["leech", 4, 7]		],
	[4,		"Strong Leech Spell", 		"Steal lots of health from the enemy.", 	10,		["leech", 6, 10]	],

	[3,		"Weak Poison Spell", 		"Deal a little damage to the enemy every turn.", 	6,		["poison", 1, 2]	],
	[4,		"Medium Poison Spell", 		"Deal a some damage to the enemy every turn.", 		8,		["poison", 2, 4]	],
	[5,		"Strong Poison Spell", 		"Deal a lots damage to the enemy every turn.", 		10,		["poison", 6, 8]	],
]

def giveSpell(spellIndex):
	chosenSpellIndex = spellIndex
	if chosenSpellIndex == None:
		lowestTier = min([a[0] for a in spellList])	# Lowest spell tier that exists
		allowedSpells = [a[0] for a in enumerate(spellList) if spellList[a[0]][0] == lowestTier]	# List of indexes of spells that can be found
		chosenSpellIndex = random.choice(allowedSpells)	# Index of spell that was chosen

	spellInfo = spellList.pop(chosenSpellIndex)

	return spellInfo	# Returns info about spell

def spellsLeft():
	return len(spellList) > 0