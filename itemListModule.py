
import math
import random

# A list of every item in the game, the first number in each array is it's rarity to be dropped.
itemList = [
	[1, 	"Small Health Potion", 	"Drink this and gain a small amount of health.", 	["heal", 5]		],
	[0.5,	"Medium Health Potion", "Drink this and gain some health.", 				["heal", 10]	],
	[0.2,	"Large Health Potion", 	"Drink this and gain lots of health.", 				["heal", 20]	],
	[0.05,	"Super Health Potion", 	"Drink this and completely restore your health.", 	["heal", 999]	],

	[1, 	"Small Mana Potion", 	"Drink this and gain a small amount of mana.", 		["mp", 3]		],
	[0.5,	"Medium Mana Potion", 	"Drink this and gain some mana.", 					["mp", 7]		],
	[0.2,	"Large Mana Potion", 	"Drink this and gain lots of mana.", 				["mp", 10]		],
	[0.05,	"Super Mana Potion", 	"Drink this and completely restore your mana.", 	["mp", 999]		]

]

def randomItem():
	raritySum = 0
	for item in itemList:	
		raritySum += item[0]	# Sum every item rarity in the list
	raritySum *= random.random()	# Randomise it

	for itemIndex in range(len(itemList)):	# Loop through each item, return the randomly selected one.
		raritySum -= itemList[itemIndex][0]
		if raritySum <= 0:
			return itemIndex