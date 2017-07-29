
import math
import random

# A list of every weapon in the game, the first number in each array is the weapon tier.
# All weapons from the lowest tier must be found before any weapons from the next tier
weaponList = [
	[	
		1, 	
		"Wooden Sword", 		
		"A terrible wooden sword, you should try to find something better.", 		
		[	
			["Swing",     "Swing your sword across the enemy.", 	[1, 2],     1],
            ["Stab",      "Attempt to pierce the enemy.",  			[2, 3],   0.7]
        ]	
	],	[	
		2, 	
		"Stone Sword", 		
		"A primitive sword carved from stone.", 		
		[	
			["Swing",     "Swing your sword across the enemy.", 	[2, 3],     1],
            ["Stab",      "Attempt to pierce the enemy.",  			[3, 5],  0.65]
        ]	
	],	[	
		3, 	
		"Iron Sword", 		
		"A sword forged with iron.", 		
		[	
			["Swing",     "Swing your sword across the enemy.", 	[4, 5],     1],
            ["Stab",      "Attempt to pierce the enemy.",  			[7, 10],  0.6]
        ]	
	],	[	
		4, 	
		"Diamond Sword", 		
		"A mighty sword somehow made with diamond...", 		
		[	
			["Swing",     "Swing your sword across the enemy.", 	[10, 15],   1],
            ["Stab",      "Attempt to pierce the enemy.",  			[20, 25], 0.5]
        ]	
	],	[	
		3, 	
		"Stone Hammer", 		
		"A basic hammer crafted with stone.", 		
		[	
			["Smash",     "Smash the enemy with your hammer.", 		[3, 4],   0.9],
            ["Crush",     "Crush the enemy from above.",  			[6, 7],   0.5]
        ]	
	],	[	
		4, 	
		"Iron Hammer", 		
		"A strong hammer forged with iron.", 		
		[	
			["Smash",     "Smash the enemy with your hammer.", 		[6, 7],   0.85],
            ["Crush",     "Crush the enemy from above.",  			[9, 15],  0.5]
        ]	
	],	[	
		5, 	
		"Diamond Hammer", 		
		"A hammer completely made with diamond crystal.", 		
		[	
			["Smash",     "Smash the enemy with your hammer.", 		[20, 25], 0.8],
            ["Crush",     "Crush the enemy from above.",  			[30, 40], 0.4]
        ]	
	]

]

def giveWeapon(weaponIndex):
	chosenWeaponIndex = weaponIndex
	if chosenWeaponIndex == None:
		lowestTier = min([a[0] for a in weaponList])	# Lowest weapon tier that exists
		allowedWeapons = [a[0] for a in enumerate(weaponList) if weaponList[a[0]][0] == lowestTier]	# List of indexes of weapons that can be found
		chosenWeaponIndex = random.choice(allowedWeapons)	# Index of weapon that was chosen

	weaponInfo = weaponList.pop(chosenWeaponIndex)

	return weaponInfo	# Returns info about weapon

def weaponsLeft():
	return len(weaponList) > 0