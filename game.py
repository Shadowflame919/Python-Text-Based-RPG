
import msvcrt
import random
import sys
import os
print(os.getcwd())
screenSize = (230, 80)
os.system("mode con cols=" + str(screenSize[0]+1) + " lines=" + str(screenSize[1]))
import time
from colorama.colorama import *
init()
import winsound
import stringAscii  # Custom module for printing ascii art text
import mapGen
import itemListModule
import spellListModule
import weaponListModule
#import inventoryClass


class Player():     # Player class, only one will exist
    def __init__(self):

        self.finished = False

        self.pos = {"x":4, "y":4}

        self.isBattling = None
        self.invOpen = False

        # Player Stats
        self.name = "Tim the Noob"

        self.maxHP = 25
        self.curHP = self.maxHP

        self.maxMP = 10
        self.curMP = self.maxMP

        # Other player stats
        self.enemiesDefeated = 0


        # Create Inventory
        self.inv = Inventory()
        # Add starting item/spell/weapon
        self.inv.addItem(0)
        self.inv.addSpell(0)
        self.inv.addWeapon(0)




        self.mapTile = [      # ▄ █ ▀
            "$▄████▄",       
            "%█.██.█",
             "██▄▄██",
            "$ ████ ",
            [Back.BLACK, Fore.CYAN]
        ]


        self.battleAscii = {
            "color": Back.BLACK + Fore.WHITE,
            "line0": "    ███████████     ",
            "line1": "  ███████████████   ",
            "line2": "     ██▀▀█▀▀██      ",
            "line3": "     ██▄▄█▄▄██      ",
            "line4": "     ██▄▄▄▄▄██      ",
            "line5": "        ███         ",
            "line6": "     █████████      ",
            "line7": "    ███████████     ",
            "line8": "    ███████████     ",
            "line9": "  ███████████████   ",
            "line10":"    ███████████     ",
            "line11":"    ███████████     ",
            "line12":"    ███████████     ",
            "line13":"    ███████████     ",
            "line14":"    ███████████     ",
            "line15":"    ██ ██ ██ ██     "
        }
        
    def keyInput(self, key):

        if self.isBattling != None:   # If player IS battling, pass key input into battle class
            self.isBattling.keyInput(key)

        else:   # This only runs if player IS NOT battling

            if key == "i":  # Only allow opening/closing inventory while NOT battling
                self.invOpen = not self.invOpen
                self.inv.scrollTop = 0
                self.inv.selectChoice = 0
                self.inv.renderMode = "main"
                if self.invOpen:
                    console.log("Opened Inventory")
                else:
                    console.log("Closed Inventory")

            if self.invOpen:
                self.inv.keyInput(key)

            else:     # Only allow movement if player IS NOT battling AND inventory is closed
                newPos = {"x":self.pos["x"], "y":self.pos["y"]}     # Edit this position, then check if player could have moved here
                if key == "a":
                    newPos["x"] -= 1    # Edit player position based on what was entered
                elif key == "d":
                    newPos["x"] += 1
                elif key == "w":
                    newPos["y"] -= 1
                elif key == "s":
                    newPos["y"] += 1

                if self.pos != newPos and mainMap.staticCollideLayer[newPos["y"]][newPos["x"]] == 3:
                    self.finished = True
                    return None


                if self.pos != newPos and mainMap.staticCollideLayer[newPos["y"]][newPos["x"]] == 0:   # Only update player position and map if new position does not collide with any staticColliders
                    self.pos = newPos
                    winsound.Beep(400,100)  # Player movement noise
                    #console.log("GAME: Player moved to position (" + str(self.pos["x"]) + ", " + str(self.pos["y"]) + ")")

                    mainMap.updatePlayer()    # Update players position on the map
                    renderMap()     # Renders the map screen after only player has moved
                    time.sleep(0.5)     # Pause game for a bit 

                    winsound.Beep(500,100)
                    mainMap.updateEnemies()     # Now move enemies

        '''
        # Other temporary letter commands       
        if key == "b":
            if self.isBattling == None:
                self.startBattle(0)
            else:
                self.isBattling = None

        elif key == "l":
            console.log("GAME: This was just logged to console!")
        '''

    def nextToEnemy(self):  # If next to enemy, return the enemies index, otherwise, return False
        
        # Values of entities to the left, right, up and down of the player
        L = mainMap.entityLayer[self.pos["y"]][self.pos["x"]-1]
        R = mainMap.entityLayer[self.pos["y"]][self.pos["x"]+1]
        U = mainMap.entityLayer[self.pos["y"]-1][self.pos["x"]]
        D = mainMap.entityLayer[self.pos["y"]+1][self.pos["x"]]

        # Test all values, if can find enemy, return index of that enemy
        if (type(L) is list) and (L[0] == 2):
            return L[1]
        elif (type(R) is list) and (R[0] == 2):
            return R[1]
        elif (type(U) is list) and (U[0] == 2):
            return U[1]
        elif (type(D) is list) and (D[0] == 2):
            return D[1]

        return None

    def startBattle(self, enemyIndex):
        self.isBattling = Battle(enemyIndex)
        renderMap()
        fillScreenWhite()


class Inventory():
    def __init__(self):

        self.scrollTop = 0      # The item rendered at the top of the inventory
        self.selectChoice = 0   
        self.renderMode = "main"

        # Anything contained in player inventory is stored as a class object, placed in a list based on what type it is

        self.spells = []    # Obviously contains all spells that player owns

        self.items = []     # Contains all usable items the player owns
            # Potions etc.

        self.weapons = []   # Contains weapons
            # Swords, Axes, Spears

        self.holdingWeapon = 0

    def addItem(self, itemIndex=itemListModule.randomItem()):
        newItem = itemListModule.itemList[itemIndex]
        for ownedItem in self.items:    # Test every item player owns, if any have same name just increase its count by one.
            if ownedItem.name == newItem[1]:
                ownedItem.count += 1
                return ownedItem

        newItem = Item(newItem[1], newItem[2], newItem[3])
        self.items.append(newItem)
        return newItem  # Return the item that was just added


    def addSpell(self, spellIndex=None):    # Takes the index of a spell and adds it to the player spell list while also removing the possibility of getting in in the future
        newSpell = spellListModule.giveSpell(spellIndex)    # The array information of the chosen spell that was just deleted from spellList
        newSpell = Spell(newSpell[1], newSpell[2], newSpell[3], newSpell[4])    # Spell Class of chosen spell
        self.spells.append(newSpell)    # Add spell to spell list
        return newSpell     # Return Spell Class of spell just added

    def addWeapon(self, weaponIndex=None):
        newWeapon = weaponListModule.giveWeapon(weaponIndex)
        newWeapon = Weapon(newWeapon[1], newWeapon[2], newWeapon[3])
        self.weapons.append(newWeapon)    # Add spell to spell list
        return newWeapon     # Return Spell Class of spell just added


    def keyInput(self, key):

        if key == "w":
            winsound.Beep(400,50)
            if self.selectChoice > 0:   # Move selection upwards
                self.selectChoice -= 1
                if self.selectChoice < self.scrollTop:
                    self.scrollTop -= 1

        elif key == "s":
            winsound.Beep(400,50)
            self.selectChoice += 1  # Move selection down

            if self.renderMode == "main":   # If still selecting which sets of items to view
                if self.selectChoice > 2:
                    self.selectChoice = 2

            elif self.renderMode == "spell":
                if self.selectChoice > len(self.spells):
                    self.selectChoice = len(self.spells)

            elif self.renderMode == "item":
                if self.selectChoice > len(self.items):
                    self.selectChoice = len(self.items)

            elif self.renderMode == "weapon":
                if self.selectChoice > len(self.weapons):
                    self.selectChoice = len(self.weapons)

            elif self.renderMode == "attack":   # Limit selection to the number of attacks on current weapon
                if self.selectChoice > len(self.weapons[self.holdingWeapon].attackList):
                    self.selectChoice = len(self.weapons[self.holdingWeapon].attackList)


            if self.selectChoice > self.scrollTop + 5:  # Move scrollTop down if selected item is off the screen
                self.scrollTop += 1

        elif key == "\r":
            winsound.Beep(400,50)
            if self.renderMode == "main":
                if self.selectChoice == 0:
                    if player.isBattling == None:
                        self.renderMode = "weapon"  # If player IS NOT battling, set to view weapons
                    else:
                        self.renderMode = "attack"  # If player IS battling, set to view attacks
                elif self.selectChoice == 1:
                    self.renderMode = "spell"
                elif self.selectChoice == 2:
                    self.renderMode = "item"

                self.selectChoice = 0   # After selected first set of option, move selector to the top

            else:   # Player wants to do something
                if self.selectChoice == 0:  # Player selected "go back" and wants to move back to main to reselect
                    if self.renderMode == "spell":  # Edit player's select choice for convenience
                        self.selectChoice = 1   
                    elif self.renderMode == "item":
                        self.selectChoice = 2
                    self.renderMode = "main"   
                else:   # Player wants to use an item
                    if self.renderMode == "weapon":     # When pressing enter while viewing weapons, they want to equip the selected weapon
                        self.holdingWeapon = self.selectChoice - 1

                    elif self.renderMode == "attack":   # Pressed enter when viewing an attack, they want to use this attack on the enemy
                        currentAttack = self.weapons[self.holdingWeapon].attackList[self.selectChoice - 1]
                        if random.random() <= currentAttack.accuracy:   # Roll random number to see if missing
                            damageRange = currentAttack.dmg    # Attacking with weapon deals damage between two values
                            damageDone = random.randrange(damageRange[0], damageRange[1]+1)     # Select random damage
                            player.isBattling.enemy.curHP -= random.randrange(damageRange[0], damageRange[1]+1)     # Deal damage to enemy
                            if player.isBattling.enemy.curHP < 0:
                                player.isBattling.enemy.curHP = 0
                            console.log("You dealt " + Fore.LIGHTRED_EX + str(damageDone) + " DMG" + Fore.WHITE + " to " + player.isBattling.enemy.name)

                        else:   # Player missed attack
                            console.log(Fore.YELLOW + "You missed the attack! :(" + Fore.WHITE)

                        player.isBattling.playerTurn = False     # Attacking causes players turn to end

                    elif self.renderMode == "item":
                        chosenItem = self.items[self.selectChoice - 1]  # The item player wants to use
                        if chosenItem.use():    # IF item was actually used
                            chosenItem.count -= 1   # Remove one of that item from the player
                            if chosenItem.count <= 0:   # After using, if no more of that item exist
                                self.items.pop(self.selectChoice - 1)   # Remove it from the array
                            if player.isBattling != None:   # If battling, end players turn
                                player.isBattling.playerTurn = False     # Using items causes players turn to end


                    elif self.renderMode == "spell":    # Player wants to use spell
                        if player.isBattling == None:
                            console.log(Fore.YELLOW + "You must be in battle to cast spells!" + Fore.WHITE)

                        else:   # Player IS battling, allow use of spell
                            chosenSpell = self.spells[self.selectChoice - 1]
                            if player.curMP >= chosenSpell.MP:  # Check if player has enough MP
                                player.curMP -= chosenSpell.MP
                                chosenSpell.use()
                                player.isBattling.playerTurn = False     # Casting spell causes players turn to end
                            else:
                                console.log("Cannot cast spell, you have " + Fore.LIGHTMAGENTA_EX + str(player.curMP) + Fore.WHITE + " of the " + Fore.LIGHTMAGENTA_EX + str(chosenSpell.MP) + " MP" + Fore.WHITE + " required.")


    ## DrawString returns the string used to render inventory, can be used for both battling and normally viewing inventory
    def drawString(self):
        inBattle = (player.isBattling != None)
        screenPrint = Back.BLACK + Fore.LIGHTWHITE_EX
        
        if self.renderMode == "main":   # Still viewing main options

            if inBattle:    # Render a different "main" when in battle
                screenPrint += stringAscii.stringToAscii("Attack", 32, 30, 0)
                screenPrint += stringAscii.stringToAscii("Cast Spell", 32, 40, 0)
                screenPrint += stringAscii.stringToAscii("Use Item", 32, 50, 0)
                screenPrint += stringAscii.stringToAscii("1", 13, 30 + self.selectChoice*10, 3)

            else:
                screenPrint += stringAscii.stringToAscii("Weapons", 32, 30, 0)
                screenPrint += stringAscii.stringToAscii("Spells", 32, 40, 0)
                screenPrint += stringAscii.stringToAscii("Items", 32, 50, 0)
                screenPrint += stringAscii.stringToAscii("1", 13, 30 + self.selectChoice*10, 3)


            screenPrint += stringAscii.stringToAscii("Use W and A to select your choice.", 10, 19, 2)

        
        else:
            ## Render string to go back to main choice
            if self.scrollTop == 0:
                goBackString = stringAscii.stringToAscii(",..,,Go Back,..,,", 42, 24, 2)
                if self.selectChoice == 0: 
                    screenPrint += Back.BLUE + goBackString + Back.BLACK
                else:
                    screenPrint += goBackString

            ## Create a list of what should be rendered
            itemList = []
            if self.renderMode == "weapon":
                itemList = self.weapons
            elif self.renderMode == "attack":
                itemList = self.weapons[self.holdingWeapon].attackList      # The list of attacks for the weapon currently equipped
            elif self.renderMode == "spell":
                itemList = self.spells
            elif self.renderMode == "item":
                itemList = self.items

            if self.scrollTop > 0: # Not rendering "go back"
                itemList = itemList[int(self.scrollTop-1):]

            for itemNum, itemObj in enumerate(itemList): # For every item being rendered
                if (self.scrollTop == 0 and itemNum >= 5) or (itemNum >= 6):   # Render a maximum of 5 spells if "go back" is visible, otherwise max of 6
                    break

                itemIndex = itemNum
                renderY = 29 + itemNum*5   # Y position on gui to render item
                if self.scrollTop > 0:   # Give room for 6 items if "go back" is not rendered
                    renderY -= 5
                    itemIndex += self.scrollTop - 1
                isSelected = (self.selectChoice == itemIndex+1) # Whether player has currently selected this item

                rightGuiText = ""
                if self.renderMode == "weapon":
                    if self.holdingWeapon == itemIndex:
                        rightGuiText = "E,QU,I,PPE,D"
                elif self.renderMode == "spell":
                    rightGuiText = str(itemObj.MP) + " MP"
                elif self.renderMode == "item":
                    rightGuiText = "x " + str(itemObj.count)

                canAfford = None   # Changes colour of rightGuiText text to red/green
                if self.renderMode == "spell" and player.isBattling != None:
                    canAfford = (player.curMP >= itemObj.MP)    # True/False whether player can afford to cast this spell


                rightGuiX = 108 - stringAscii.stringToAsciiLength(rightGuiText, 2)     # X position to render string on the right


                screenPrint += stringAscii.stringToAscii(str(itemIndex+1) + ".", 6, renderY, 2)     # Render number on the left displaying item index in the array + 1
                
                itemNameString = stringAscii.stringToAscii(" " + itemObj.name + " ", 16, renderY, 2)    # Item name to be rendered in selector
                if isSelected:  # If item is currently being selected
                    screenPrint += Back.BLUE + itemNameString + Back.BLACK  # Print its name, but in blue

                    ## Text selection describing current item
                    screenPrint += stringAscii.stringToAscii(itemObj.name, 7, 58, 2, True)
                    screenPrint += cursorPos(7,64) + "Description: " + itemObj.desc

                    # Descriptions are all different depending on the type of item selected
                    if self.renderMode == "weapon":
                        screenPrint += cursorPos(7,67) + "Attacks:"

                        for attackNum, attack in enumerate(itemObj.attackList):
                            screenPrint += cursorPos(11,69 + 2*attackNum) + attack.name + ","        # Render attack name
                            screenPrint += cursorPos(23,69 + 2*attackNum) + Fore.LIGHTRED_EX + str(attack.dmg[0]) + "-" + str(attack.dmg[1]) + " DMG" + Fore.WHITE + ","
                            screenPrint += cursorPos(39,69 + 2*attackNum) + Fore.YELLOW + str(attack.accuracy*100) + "% Accuracy" + Fore.WHITE

                        if self.holdingWeapon != itemIndex: # If NOT holding this item
                            screenPrint += cursorPos(75,76) + "Press ENTER to Equip this weapon."

                    elif self.renderMode == "attack":   # Render description for attacks
                        weaponStringX = 108 - stringAscii.stringToAsciiLength(self.weapons[self.holdingWeapon].name, 2)
                        screenPrint += cursorPos(weaponStringX-7,59) + "____"
                        screenPrint += stringAscii.stringToAscii(self.weapons[self.holdingWeapon].name, weaponStringX, 58, 2)
                        screenPrint += cursorPos(7,67) + "Damage:       " + Fore.LIGHTRED_EX + str(itemObj.dmg[0]) + " - " + str(itemObj.dmg[1]) + " HP" + Fore.WHITE
                        screenPrint += cursorPos(7,69) + "Accuracy:     " + Fore.YELLOW + str(itemObj.accuracy*100) + "%" + Fore.WHITE

                    elif self.renderMode == "item":
                        screenPrint += cursorPos(7,67) + "Effects: "
                        if itemObj.stats[0] == "heal":
                            screenPrint += cursorPos(11,69) + Fore.LIGHTGREEN_EX + "+ " + str(itemObj.stats[1]) + " HP" + Fore.WHITE
                        elif itemObj.stats[0] == "mp":
                            screenPrint += cursorPos(11,69) + Fore.LIGHTMAGENTA_EX + "+ " + str(itemObj.stats[1]) + " MP" + Fore.WHITE

                    elif self.renderMode == "spell":
                        screenPrint += cursorPos(7,67) + "Effects: "
                        if itemObj.stats[0] == "heal":
                            screenPrint += cursorPos(11,69) + Fore.LIGHTGREEN_EX + "+ Gain " + str(itemObj.stats[1]) + " - " + str(itemObj.stats[2]) + " HP" + Fore.WHITE
                        elif itemObj.stats[0] == "leech":
                            screenPrint += cursorPos(11,69) + Fore.LIGHTRED_EX + "+ Deal " + str(itemObj.stats[1]) + " - " + str(itemObj.stats[2]) + " DMG" + Fore.WHITE
                            screenPrint += cursorPos(11,71) + Fore.LIGHTGREEN_EX + "+ Gain DMG dealt as HP" + Fore.WHITE
                        elif itemObj.stats[0] == "poison":
                            screenPrint += cursorPos(11,69) + Fore.YELLOW + "+ Deal " + Fore.LIGHTGREEN_EX + str(itemObj.stats[1]) + " - " + str(itemObj.stats[2]) + " DMG" + Fore.YELLOW + " every turn." + Fore.WHITE

                    if canAfford:
                        screenPrint += Fore.GREEN
                    elif canAfford == False:
                        screenPrint += Fore.RED
                    screenPrint += stringAscii.stringToAscii(rightGuiText, rightGuiX, 74, 2)    # Render gui text is rendered in bottom right if item is selected
                    screenPrint += Fore.WHITE
                else:
                    screenPrint += itemNameString

                if canAfford:
                    screenPrint += Fore.GREEN
                elif canAfford == False:
                    screenPrint += Fore.RED
                screenPrint += stringAscii.stringToAscii(rightGuiText, rightGuiX, renderY, 2)  # Text to the right of the item's name
                screenPrint += Fore.WHITE

            if self.scrollTop > 0:
                screenPrint += stringAscii.stringToAscii("9", 80, 19, 3)    # You can scroll up arrow
            
            # You can scroll down arrow
            if (self.renderMode == "weapon") and (self.scrollTop+5 < len(self.weapons)):    
                screenPrint += stringAscii.stringToAscii("8", 80, 53, 3)
            elif (self.renderMode == "attack") and (self.scrollTop+5 < len(self.weapons[self.holdingWeapon].attackList)):    
                screenPrint += stringAscii.stringToAscii("8", 80, 53, 3)
            elif (self.renderMode == "spell") and (self.scrollTop+5 < len(self.spells)):    
                screenPrint += stringAscii.stringToAscii("8", 80, 53, 3)
            elif (self.renderMode == "item") and (self.scrollTop+5 < len(self.items)):    
                screenPrint += stringAscii.stringToAscii("8", 80, 53, 3)

            screenPrint += cursorPos(4,57) + "\u2500"*107   # Line between selector and description

        return screenPrint


class Item():
    def __init__(self, name, desc, stats):   # Info is array in form [rarity, name, desc, count, stats]
        self.name = name
        self.desc = desc
        self.count = 1

        self.stats = stats

    def use(self):  # Uses item, return True if sucessful
        if self.stats[0] == "heal":
            if player.curHP < player.maxHP:
                player.curHP += self.stats[1]
                if player.curHP > player.maxHP:
                    player.curHP = player.maxHP
                console.log("Consumed " + str(self.name) + ", " + str(self.count-1) + " remaining.")
                console.log(Fore.LIGHTGREEN_EX + "   + " + str(self.stats[1]) + " HP" + Fore.WHITE)
                return True
            else:   # Item was NOT used
                console.log(Fore.YELLOW + "Unable to use potion, you already have full HP!" + Fore.WHITE)

        if self.stats[0] == "mp":
            if player.isBattling == None:
                console.log(Fore.YELLOW + "Mana potions can not be used outside of a battle!" + Fore.WHITE)
            elif player.curMP < player.maxMP:
                player.curMP += self.stats[1]
                if player.curMP > player.maxMP:
                    player.curMP = player.maxMP
                console.log("Consumed " + str(self.name) + ", " + str(self.count-1) + " remaining.")
                console.log(Fore.LIGHTMAGENTA_EX + "   + " + str(self.stats[1]) + " MP" + Fore.WHITE)
                return True
            else:   # Item was NOT used
                console.log(Fore.YELLOW + "Unable to use potion, you already have full MP!" + Fore.WHITE)


class Spell():
    def __init__(self, name, desc, MP, stats):
        self.name = name
        self.desc = desc
        self.MP = MP
        self.stats = stats

    def use(self):
        if self.stats[0] == "heal":
            healAmount = random.randrange(self.stats[1], self.stats[2]+1)
            player.curHP += healAmount
            if player.curHP > player.maxHP:
                player.curHP = player.maxHP
            console.log("Casted " + str(self.name) + ", " + Fore.LIGHTMAGENTA_EX + str(player.curMP) + " MP" + Fore.WHITE + " remaining.")
            console.log(Fore.LIGHTGREEN_EX + "   Gained " + str(healAmount) + " HP" + Fore.WHITE)

        elif self.stats[0] == "leech":
            leechAmount = random.randrange(self.stats[1], self.stats[2]+1)
            if player.isBattling.enemy.curHP < leechAmount: # If enemy does not have enough health to leech
                leechAmount = player.isBattling.enemy.curHP
            player.isBattling.enemy.curHP -= leechAmount
            player.curHP += leechAmount
            if player.curHP > player.maxHP:
                player.curHP = player.maxHP

            console.log("Casted " + str(self.name) + ", " + Fore.LIGHTMAGENTA_EX + str(player.curMP) + " MP" + Fore.WHITE + " remaining.")
            console.log(Fore.LIGHTRED_EX + "   Dealt " + str(leechAmount) + " DMG" + Fore.WHITE)
            console.log(Fore.LIGHTGREEN_EX + "   Gained " + str(leechAmount) + " HP" + Fore.WHITE)

        elif self.stats[0] == "poison":
            poisonAmount = random.randrange(self.stats[1], self.stats[2]+1)
            player.isBattling.enemy.poisonAmount += poisonAmount

            console.log("Casted " + str(self.name) + ", " + Fore.LIGHTMAGENTA_EX + str(player.curMP) + " MP" + Fore.WHITE + " remaining.")
            console.log(Fore.YELLOW + "   Poisoned enemy for " + Fore.LIGHTGREEN_EX + str(poisonAmount) + " DMG" + Fore.WHITE + " per turn.")


class Weapon():
    def __init__(self, name, desc, attackList):
        self.name = name
        self.desc = desc
        self.attackList = []
        for attack in attackList:  # Turn arrays into actual Attack classes
            self.attackList.append(Attack(attack[0], attack[1], attack[2], attack[3]))


class Attack():
    def __init__(self, name, desc, dmg, accuracy):
        self.name = name
        self.desc = desc
        self.dmg = dmg
        self.accuracy = accuracy


class Enemy():
    def __init__(self, enemyStats):

        self.pos = enemyStats["pos"]

        # Enemy Stats
        self.name = enemyStats["name"]
        self.maxHP = enemyStats["maxHP"]
        self.curHP = self.maxHP

        self.poisonAmount = 0

        self.mapTile = [
            "$  ▄▄▄ ",
           "$ %█▀█▀█",
           "$ %██▄██",
            "$  ▀ ▀ ",
            [Back.BLACK, Fore.WHITE],
        ]

        self.battleAscii = {    
            "color": Back.BLACK + Fore.WHITE,  
            "line0": "             ▄█    ",
            "line1": "       ▄▄▄  ▄██▄   ",
            "line2": "      █▀█▀█    ▀█▄ ",
            "line3": "      ██▄██      ▀█",
            "line4": "       ▀▄▀   ▄▄▄▄▄▀",
            "line5": "     ▄▄▄██▀▀▀▀     ",
            "line6": "    █▀▄▄▄█ ▀▀      ",
            "line7": "    █ ▄▄▄██▀▀▀     ",
            "line8": " ▄ █   ▄▄ █ ▀▀     ",
            "line9": " ▀██   ▄ ▀█▀ ▀     ",
            "line10":"        ▄▄██▄▄     ",
            "line11":"        ▀███▀█ ▄   ",
            "line12":"       ██▀▄▀▄▀█▄   ",
            "line13":"       █▀      ██  ",
            "line14":"       █        █  ",
            "line15":"      ██         █ "
        }

        if self.name == "Skeleton King":
            self.mapTile = [
                "$ Y█▄▄▄█",
               "$ %█▀█▀█",
               "$ %██▄██",
                "$  ▀ ▀ ",
                [Back.BLACK, Fore.WHITE],
            ]
            self.battleAscii["line1"] = "      " + Fore.LIGHTYELLOW_EX + "█▄▄▄█" + Fore.LIGHTWHITE_EX + " ▄██▄   "

    
    def update(self):
        return self.move()
    
    def move(self):
        if self.name == "Skeleton King":
            return None

        if mainMap.entityLayer[self.pos["y"]][self.pos["x"]-1] == 1 or mainMap.entityLayer[self.pos["y"]][self.pos["x"]+1] == 1:    # Return None if player is to left/right of enemy
            return None
        if mainMap.entityLayer[self.pos["y"]-1][self.pos["x"]] == 1 or mainMap.entityLayer[self.pos["y"]+1][self.pos["x"]] == 1:    # Return None if player is above/below enemy
            return None


        newPos = {"x":self.pos["x"], "y":self.pos["y"]}     # Edit this position, then check if enemy could have moved here
        moveDir = random.randrange(0,4)
        if moveDir == 0:
            newPos["x"] -= 1
        elif moveDir == 1:
            newPos["x"] += 1
        elif moveDir == 2:
            newPos["y"] -= 1
        elif moveDir == 3:
            newPos["y"] += 1

        if mainMap.staticCollideLayer[newPos["y"]][newPos["x"]] == 0 and mainMap.entityLayer[newPos["y"]][newPos["x"]] == 0:   # Only update enemy position and map if new position does not collide with any staticColliders or entities
            oldPos = {"x":self.pos["x"], "y":self.pos["y"]}
            self.pos = newPos
            return oldPos   # After moving and changing position, returns oldPos
        return None    # Returning None means enemy did not move

class Battle():
    def __init__(self, enemyIndex):
        self.turnNumber = 0
        self.playerTurn = True

        self.enemyIndex = enemyIndex
        self.enemy = mainMap.enemyList[enemyIndex]

        console.log(Fore.YELLOW + "You have entered battle with - " + self.enemy.name + Fore.WHITE)

        player.curMP = int(player.maxMP/2)     # Player starts with half mana when in a battle

    def keyInput(self, key):
        '''
        if key == "k":
            self.enemy.curHP -= 5
        elif key == "j":
            player.curHP -= 1
        '''

        # Choice selection
        if key == "w":   # Move selection up
            player.inv.keyInput("w")

        elif key == "s":   # Move selection down
            player.inv.keyInput("s")

        elif key == "\r":   # Confirm Selection Choice
            player.inv.keyInput("\r")

        if not self.playerTurn:     # Player only just made their move
            if self.enemy.poisonAmount > 0:
                self.enemy.curHP -= self.enemy.poisonAmount
                console.log("Enemy is poisoned, " + Fore.LIGHTGREEN_EX + str(self.enemy.poisonAmount) + " DMG" + Fore.WHITE + " was dealt")
                if self.enemy.curHP < 0:
                    self.enemy.curHP = 0

            player.inv.renderMode = "main"
            player.inv.selectChoice = 0
            renderBattle()  # Render battle once to show enemies new health/stats
            time.sleep(1)   # Pause the game for 1 second so the player can see

            # Check if enemy is dead
            if self.enemy.curHP <= 0:   # Enemy has died
                # Tell player & give rewards
                player.enemiesDefeated += 1
                console.log(Fore.LIGHTGREEN_EX + self.enemy.name + " has been killed! " + Fore.WHITE)
                player.maxHP += 5
                console.log("Your Maximum Health has increased by " + Fore.LIGHTGREEN_EX + "5 HP")
                player.maxMP += 1
                console.log("Your Maximum Mana has increased by " + Fore.LIGHTMAGENTA_EX + "1 MP")

                newItem = player.inv.addItem()  # Give player a random item for killing enemy
                console.log(Fore.LIGHTGREEN_EX + "   + " + Fore.WHITE + newItem.name)

                for i in range(3):  # Give player 3 more 30% chances at another item
                    if random.random() < 0.3: 
                        newItem = player.inv.addItem()  # Give player a random item for killing enemy
                        console.log(Fore.LIGHTGREEN_EX + "   + " + Fore.WHITE + newItem.name)

                if spellListModule.spellsLeft() and random.random() < 0.25: # Give player a new spell 25% of the time
                    newSpell = player.inv.addSpell()
                    console.log(Fore.LIGHTGREEN_EX + "   + " + Fore.WHITE + newSpell.name)

                if weaponListModule.weaponsLeft() and (player.enemiesDefeated == 1 or random.random() < 0.25): # Give player a new weapon 25% of the time or if defeated first enemy
                    newWeapon = player.inv.addWeapon()
                    console.log(Fore.LIGHTGREEN_EX + "   + " + Fore.WHITE + newWeapon.name)
                    if len(player.inv.weapons) == 2:
                        console.log("You have just recieved a better weapon, open the inventory by typing 'open inv' to equip it.")

                mainMap.killEnemy(self.enemyIndex)
                fillScreenWhite()
                player.isBattling = None

            else:
                self.enemyTurn()
                if player.curHP <= 0:
                    player.curHP = 0
                    player.finished = True

                # Add some MP after every turn
                addedMP = 1
                if player.curMP == player.maxMP:
                    console.log("You turn, " + Fore.LIGHTMAGENTA_EX + "0 MP" + Fore.WHITE + " was added as you already have " + Fore.LIGHTMAGENTA_EX + str(player.curMP) + "/" + str(player.maxMP) + Fore.WHITE)
                console.log("Your turn, " + Fore.LIGHTMAGENTA_EX + "+ " + str(addedMP) + " MP" + Fore.WHITE)
                player.curMP += addedMP
                if player.curMP > player.maxMP:
                    player.curMP = player.maxMP

    def enemyTurn(self):
        if random.random() < 0.75:
            enemyDamage = 0

            if self.enemy.name == "Skeleton King":
                enemyDamage = random.randrange(10,20)
            else:
                enemyMinDamage = int(self.enemy.maxHP/5)
                enemyMaxDamage = int(1.5*self.enemy.maxHP/5)
                enemyDamage = random.randrange(enemyMinDamage,enemyMaxDamage)

            player.curHP -= enemyDamage
            console.log(self.enemy.name + " dealt " + Fore.LIGHTRED_EX + str(enemyDamage) + " DMG" + Fore.WHITE)
        else:
            console.log(Fore.YELLOW + self.enemy.name + " missed their attack!" + Fore.WHITE)

        self.playerTurn = True

		


class Console():
    def __init__(self):
        self.pos = {"x":115, "y":58, "w":114, "h":21}

        self.logList = [
            "Good luck! " + Fore.YELLOW + "Use WASD to move about." + Fore.WHITE,
            "If you ever forget the commands, type 'help' or '?' into this console.",
            "Your goal is to find the Skeleton King and defeat him as he is guarding the only way out.",
            "You have found yourself lost in a dungeon crawling with skeletons.",
            "Hello and welcome to SSS Dungeon."
        ]

    def log(self, text):
        self.logList.insert(0,str(text))
        #print(self.drawString(), end="")

    def logCommands(self):
        self.log("")
        self.log("List of commands:")
        self.log("    '?' or 'help' - Displays a list of commands.")
        self.log("    open inv - Opens the inventory.")
        self.log("    close inv - Closes the inventory.")
        self.log("    exit game - Completely quits the game.")
        self.log("")

    def drawString(self):   # Returns the string that when printed, will display the console.
        drawStr = Back.BLACK + Fore.LIGHTWHITE_EX

        # Render log messages in console
        for msgNum in range(self.pos["h"]-5):
            if msgNum >= len(self.logList):  # Stop writing messages if not enough exist
                break
            drawStr += cursorPos(self.pos["x"]+2,self.pos["y"]+self.pos["h"]-5-msgNum)
            drawStr += self.logList[msgNum]

        # Text input part of console
        drawStr += Back.BLACK + Fore.LIGHTWHITE_EX
        drawStr += boxPrint(self.pos["x"]+1, self.pos["y"]+self.pos["h"]-3, self.pos["w"]-35, 3, "thin")
        drawStr += cursorPos(self.pos["x"]+self.pos["w"]-33, self.pos["y"]+self.pos["h"]-2) + "Type '?' for a list of commands."

        drawStr += cursorPos(self.pos["x"]+2, self.pos["y"]+self.pos["h"]-2) + "Press 't' to start typing."

        return drawStr
        
def drawStats(x,y):     # Returns the string to render stats at (x,y)
    # Stats must fit into a space of 114x52
    screenPrint = cursorPos(x,y) + Style.NORMAL + Back.BLACK

    # Draw player stats
    nameLength = stringAscii.stringToAsciiLength(player.name, 1)
    nameX = int((106-nameLength)/2)
    screenPrint += stringAscii.stringToAscii(player.name, x+nameX, y+3, 1, True)

    screenPrint += stringAscii.stringToAscii("Health - " + str(player.curHP) + ",/" + str(player.maxHP), x+8, y+12, 2)

    screenPrint += stringAscii.stringToAscii("Max MP - " + str(player.maxMP), x+66, y+12, 2)

    '''
    screenPrint += stringAscii.stringToAscii("Maximum MP", x+8, y+18, 2)
    screenPrint += cursorPos(x+70,y+19) + "___"
    screenPrint += stringAscii.stringToAscii("4", x+76, y+18, 2)

    screenPrint += stringAscii.stringToAscii("Defence", x+8, y+24, 2)
    screenPrint += cursorPos(x+70,y+25) + "___"
    screenPrint += stringAscii.stringToAscii("4", x+76, y+24, 2)
    '''
    screenPrint += stringAscii.stringToAscii("E,nemies Defeated - " + str(player.enemiesDefeated), x+8, y+20, 2)

    screenPrint += stringAscii.stringToAscii("Weapon - " + str(player.inv.weapons[player.inv.holdingWeapon].name), x+8, y+26, 2)
    #screenPrint += stringAscii.stringToAscii("E,nemies Defeated - " + str(player.enemiesDefeated), x+15, y+30, 2)
    

    #screenPrint += cursorPos(x+2,y+3) + "Name: " + player.name
    #screenPrint += cursorPos(x+2,y+5) + "Health: " + str(player.curHP) + "/" + str(player.maxHP)
    #screenPrint += cursorPos(x+2,y+6) + "Level: " + str(player.level) + " (" + str(player.curXP) + "/" + str(player.maxXP) + "xp)"

    return screenPrint



def renderMap():
    # Move cursor to top left and remove all styling and set background black
    screenPrint = cursorPos(1,1) + Style.NORMAL + Back.BLACK

    # Fill screen black
    for i in range(80):
        screenPrint += cursorPos(1,i+1)
        screenPrint += " "*230
    
    ### Draw Main Boxes ###
    screenPrint += Back.BLACK + Fore.LIGHTWHITE_EX
    screenPrint += boxPrint(3,2,109,78)
    screenPrint += boxPrint(114,2,116,54)
    screenPrint += boxPrint(114,57,116,23)


    ### Render Left of Screen ###
    
    # Words at the top
    screenPrint += stringAscii.stringToAscii("SSS Dungeon", 22, 6, 0, True)
    screenPrint += stringAscii.stringToAscii("Use WASD to move.", 14, 15, 1)

    screenPrint += cursorPos(4,24) + "\u2500"*107   # Render line above player stats
    screenPrint += drawStats(4,25)


    ### Render Right of Screen ###
    
    # Draw console
    screenPrint += console.drawString()
    
    # Render Map in its box on right of screen
    screenPrint += mainMap.drawString(115,3,114,54)


    print(screenPrint, end="")

def renderInventory():
    ## Move cursor to top left and remove all styling and set background black
    screenPrint = cursorPos(1,1) + Style.NORMAL + Back.BLACK

    ## Fill screen black
    for i in range(80):
        screenPrint += cursorPos(1,i+1)
        screenPrint += " "*230

    ### Draw Main Layout Boxes ###
    screenPrint += Back.BLACK + Fore.LIGHTWHITE_EX
    screenPrint += boxPrint(3,2,109,78)
    #screenPrint += cursorPos(3,11) + "\u2560" + "\u2500"*107 + "\u2563"
    screenPrint += boxPrint(114,2,116,54)
    screenPrint += boxPrint(114,57,116,23)


    ### Draw left of screen ###
    screenPrint += stringAscii.stringToAscii("Inventory", 29, 6, 0, True)
    screenPrint += cursorPos(4,16) + "\u2500"*107   # Render line at the top

    if player.inv.renderMode == "weapon":
        screenPrint += stringAscii.stringToAscii("Weapons", 7, 18, 1, True)
    elif player.inv.renderMode == "spell":
        screenPrint += stringAscii.stringToAscii("Spells", 7, 18, 1, True)
        screenPrint += cursorPos(68,19) + "Spells can only be used during battles."
    elif player.inv.renderMode == "item":
        screenPrint += stringAscii.stringToAscii("Items", 7, 18, 1, True)

    screenPrint += player.inv.drawString()


    ### Draw right of screen ###
    screenPrint += drawStats(119,3)

            


    ## Draw console
    screenPrint += console.drawString()
    print(screenPrint, end="")
	
def renderBattle():
    # Move cursor to top left and remove all styling and set background black
    screenPrint = cursorPos(1,1) + Style.NORMAL + Back.BLACK

    # Fill screen black
    for i in range(80):
        screenPrint += cursorPos(1,i+1)
        screenPrint += " "*230
    
    ### Draw Main Boxes ###
    screenPrint += Back.BLACK + Fore.LIGHTWHITE_EX
    screenPrint += boxPrint(3,2,109,78)
    #screenPrint += cursorPos(3,11) + "\u2560" + "\u2500"*107 + "\u2563"
    screenPrint += boxPrint(114,2,116,54)
    screenPrint += boxPrint(114,57,116,23)
    
    ### Render Main Options List ###
    screenPrint += stringAscii.stringToAscii("What will you do?", 6, 4, 0)
    screenPrint += cursorPos(7,9) + "\u2500"*58 + cursorPos(71,9) + "\u2500"*36   # Custom Underline
    screenPrint += stringAscii.stringToAscii("Press enter to confirm choice.", 15, 10, 2)
    screenPrint += cursorPos(4,16) + "\u2500"*107   # Render line at the top

    # If player has not selected a main option
    if player.inv.renderMode == "main":
        screenPrint += player.inv.drawString()
    # Player has selected their main option
    else:    

        ## -- Player selected "Attack" -- ##
        if player.inv.renderMode == "attack":
            screenPrint += stringAscii.stringToAscii("Select Attack", 7, 18, 1, True)

            screenPrint += player.inv.drawString()

        ## -- Player selected "Cast Spell" -- ##
        elif player.inv.renderMode == "spell":
            screenPrint += stringAscii.stringToAscii("Select Spell", 7, 18, 1, True)

            screenPrint += player.inv.drawString()


        ## -- Player selected "Use Item" -- ##
        elif player.inv.renderMode == "item":
            screenPrint += stringAscii.stringToAscii("Select Item", 7, 18, 1, True)

            screenPrint += player.inv.drawString()


            

    
    ### Draw Battle Screen ###
    ## Draw player

    # Player Battle Ascii
    screenPrint += player.battleAscii["color"]
    for playerAsciiLayer in range(16):   
        screenPrint += cursorPos(130,35+playerAsciiLayer)
        screenPrint += player.battleAscii["line" + str(playerAsciiLayer)]

    # Player stats
    screenPrint += cursorPos(130,26) + Back.BLACK + Fore.LIGHTWHITE_EX + player.name    # Player name

    # Player health
    screenPrint += cursorPos(130,29)    # Set cursor to correct place for rendering player HP
    playerHPString = " " + str(player.curHP) + "/" + str(player.maxHP) + " HP" + " "*20  # String to be rendered showing HP
    curHPCharAmnt = int(20*player.curHP/player.maxHP)   # Number of tiles that are light red
    screenPrint += Back.LIGHTRED_EX + Fore.LIGHTWHITE_EX
    for charNum in range(20):
        if charNum == curHPCharAmnt:
            screenPrint += Back.RED
        screenPrint += playerHPString[charNum]
    screenPrint += Back.BLACK
    screenPrint += cursorPos(130,28) + Fore.LIGHTRED_EX + curHPCharAmnt * "▄" + Fore.RED + (20-curHPCharAmnt) * "▄"
    screenPrint += cursorPos(130,30) + Fore.LIGHTRED_EX + curHPCharAmnt * "▀" + Fore.RED + (20-curHPCharAmnt) * "▀"

    # Player mana
    screenPrint += cursorPos(130,32)    # Set cursor to correct place for rendering player HP
    playerMPString = " " + str(player.curMP) + "/" + str(player.maxMP) + " MP" + " "*20  # String to be rendered showing HP
    curMPCharAmnt = int(20*player.curMP/player.maxMP)   # Number of tiles that are light red
    screenPrint += Back.LIGHTBLUE_EX + Fore.LIGHTWHITE_EX
    for charNum in range(20):
        if charNum == curMPCharAmnt:
            screenPrint += Back.BLUE
        screenPrint += playerMPString[charNum]
    screenPrint += Back.BLACK
    screenPrint += cursorPos(130,31) + Fore.LIGHTBLUE_EX + curMPCharAmnt * "▄" + Fore.BLUE + (20-curMPCharAmnt) * "▄"
    screenPrint += cursorPos(130,33) + Fore.LIGHTBLUE_EX + curMPCharAmnt * "▀" + Fore.BLUE + (20-curMPCharAmnt) * "▀"



    ## Draw Enemy

    # Other stats
    screenPrint += cursorPos(190,14) + Back.BLACK + Fore.LIGHTWHITE_EX + player.isBattling.enemy.name
    if player.isBattling.enemy.poisonAmount > 0:
        screenPrint += cursorPos(212,17) + Back.BLACK + Fore.LIGHTGREEN_EX + "- " + str(player.isBattling.enemy.poisonAmount) + Fore.LIGHTWHITE_EX


    # Enemy Battle Ascii
    screenPrint += player.isBattling.enemy.battleAscii["color"]
    for enemyAsciiLayer in range(16):   
        screenPrint += cursorPos(190,20+enemyAsciiLayer)
        screenPrint += player.isBattling.enemy.battleAscii["line" + str(enemyAsciiLayer)]

    # Enemy health
    screenPrint += cursorPos(190,17)    # Set cursor to correct place for rendering enemy HP
    enemyHPString = " " + str(player.isBattling.enemy.curHP) + "/" + str(player.isBattling.enemy.maxHP) + " HP" + " "*20  # String to be rendered showing HP
    curHPCharAmnt = int(20*player.isBattling.enemy.curHP/player.isBattling.enemy.maxHP)   # Number of tiles that are light red
    screenPrint += Back.LIGHTRED_EX + Fore.LIGHTWHITE_EX
    for charNum in range(20):
        if charNum == curHPCharAmnt:
            screenPrint += Back.RED
        screenPrint += enemyHPString[charNum]
    screenPrint += Back.BLACK
    screenPrint += cursorPos(190,16) + Fore.LIGHTRED_EX + curHPCharAmnt * "▄" + Fore.RED + (20-curHPCharAmnt) * "▄"
    screenPrint += cursorPos(190,18) + Fore.LIGHTRED_EX + curHPCharAmnt * "▀" + Fore.RED + (20-curHPCharAmnt) * "▀"




    screenPrint += console.drawString()
    
    print(screenPrint, end="")
    
    #input(cursorPos(96,78))


def fillScreenWhite():       # Pauses the game and plays a kind of pointless but cool looking transition animation.
    startTime = time.time()

    '''
    print(Style.NORMAL + Back.LIGHTWHITE_EX,end="")
    pixelList = []
    for y in range(80):
        for x in range(int(230/2)):
            pixelList.append([x,y])

    while len(pixelList) > 0:
        whitePixel = pixelList.pop(random.randrange(len(pixelList)))
        screenPrint = cursorPos(whitePixel[0]*2+1, whitePixel[1]+1) + "  "
        print(screenPrint, end="")
    '''

    print(Style.NORMAL + Back.BLACK,end="")
    pixelList = []
    for y in range(80):
        for x in range(int(230/2)):
            pixelList.append([x,y])
    while len(pixelList) > 0:
        whitePixel = pixelList.pop(random.randrange(len(pixelList)))
        screenPrint = cursorPos(whitePixel[0]*2+1, whitePixel[1]+1) + "  "
        print(screenPrint, end="")

    #console.log("GAME: Transition length: " + str(time.time() - startTime))

def boxPrint(x,y,w,h,box_type="thick",filled=False):   # Draws custom box at x,y position on screen
    
    box_types = {   # Horizontal, Vertical, Top-left, Top-right, Bottom-left, Bottom-right
        "thick": ["\u2550","\u2551","\u2554","\u2557","\u255A","\u255D"],
        "thin": ["\u2500","\u2502","\u250C","\u2510","\u2514","\u2518"]
    }
    
    boxText = cursorPos(x,y)
    boxText += box_types[box_type][2] # Top left corner
    boxText += box_types[box_type][0] * (w-2) # Top side
    boxText += box_types[box_type][3] # Top right corner
    for i in range(h-2):
        boxText += cursorPos(x, y+i+1)
        boxText += box_types[box_type][1]
        if filled:
            boxText += (w-2)*" "
        else:
            boxText += cursorPos(x+w-1, y+i+1)
        boxText += box_types[box_type][1]
    boxText += cursorPos(x, y+h-1)
    boxText += box_types[box_type][4] # Bottom left corner
    boxText += box_types[box_type][0] * (w-2) # Bottom side
    boxText += box_types[box_type][5] # Bottom right corner
    
    return boxText
    
def cursorPos(x,y):
    return "\x1b[" + str(y) + ";" + str(x) + "H"



   
console = Console()     # Create console class first so anything can be logged
player = Player()
#popup = Popup(100,50,"enemy encountered", "you have encounted an enemy")
enemyList = [
    Enemy({"name":"Spooky Scary Skeleton",      "maxHP":10, "pos":{"x":9,  "y":4}     }),
    Enemy({"name":"Spooky Scary Skeleton",      "maxHP":15, "pos":{"x":22, "y":3}    }),
    Enemy({"name":"Spooky Scary Skeleton",      "maxHP":20, "pos":{"x":27, "y":11}   }),
    Enemy({"name":"Spooky Scary Skeleton",      "maxHP":25, "pos":{"x":18, "y":11}   }),
    Enemy({"name":"Spooky Scary Skeleton",      "maxHP":30, "pos":{"x":8,  "y":12}   }),
    Enemy({"name":"Spooky Scary Skeleton",      "maxHP":35, "pos":{"x":4,  "y":17}   }),
    Enemy({"name":"Spooky Scary Skeleton",      "maxHP":40, "pos":{"x":12, "y":17}  }),
    Enemy({"name":"Spooky Scary Skeleton",      "maxHP":50, "pos":{"x":20, "y":17}  }),
    Enemy({"name":"Skeleton King",              "maxHP":100,"pos":{"x":24, "y":16}   }),     # 24,16
]


mainMap = mapGen.World_Map(player, enemyList, console)    # Takes in current player pos

def renderScreen():
    if player.isBattling != None:
        renderBattle()
    elif player.invOpen:
        renderInventory()
    else:
        renderMap()
    print(cursorPos(1,1), end="")


# Start background music
winsound.PlaySound("background_music.wav", winsound.SND_ASYNC | winsound.SND_LOOP)

### Render intro screen

# Move cursor to top left and remove all styling and set background black
screenPrint = cursorPos(1,1) + Style.NORMAL + Back.BLACK + Fore.LIGHTWHITE_EX

# Fill screen black
for i in range(80):
    screenPrint += cursorPos(1,i+1)
    screenPrint += " "*230

# Text on the intro screen
screenPrint += boxPrint(26,12,178,56)
screenPrint += boxPrint(30,15,170,50)
screenPrint += stringAscii.stringToAscii("Welcome to SSS Dungeon!", 42, 20, 0)
screenPrint += stringAscii.stringToAscii("Please enter your name...", 55, 33, 1)
screenPrint += stringAscii.stringToAscii("Press enter to confirm.", 82, 55, 2)
screenPrint += boxPrint(62, 43, 110, 7, "thin")
print(screenPrint, end="")

# Get players name
nameInput = ""
print(stringAscii.stringToAscii(nameInput + ",_", 65, 44, 1), end="")
print(cursorPos(1,1), end="")
while True: # Loop keeps running through until player submits name
    if msvcrt.kbhit():
        key = msvcrt.getwch()
        while msvcrt.kbhit():    # Removes any key input buffering
            msvcrt.getwch()
        print(cursorPos(65,51) + " "*100, end="")
        if key == "\x08":   # If user typed a backspace
            if len(nameInput) > 0:
                nameInput = nameInput[:-1]  # Remove last key
                for i in range(5): # Clear text
                    print(cursorPos(65,44+i) + " "*106, end="")

        elif key == "\r":   # If player presses enter, this is their name
            if len(nameInput) > 0:
                player.name = nameInput
                break   # Breaking loop starts the game
            else:
                print(cursorPos(67,51) + "Enter a name before continuing.", end="")
                winsound.Beep(200,400)  # Make error noise

        else:   # Otherwise
            if (key != ",") and (key in stringAscii.fonts[1].keys()):  # If input can be found in the stringAscii key library
                stringLength = stringAscii.stringToAsciiLength(nameInput + key, 1)  # Check if length of name is within 100 character for stringAscii
                if stringLength < 100:
                    nameInput += key
                else:
                    print(cursorPos(67,51) + "Name too long", end="")
                    winsound.Beep(200,400)  # Make error noise
            else:
                print(cursorPos(67,51) + "Invalid Key.", end="")
                winsound.Beep(200,400)

    
        print(stringAscii.stringToAscii(nameInput + ",_", 65, 44, 1), end="")
        print(cursorPos(1,1), end="")
fillScreenWhite()

## REAL game loop

renderScreen()
while True:     # Entire Game loop
    if msvcrt.kbhit():  # Wait until player enters a key
        key = msvcrt.getwch()
        while msvcrt.kbhit():   # Removes any key input buffering
            msvcrt.getwch()
        if key == "t":  # Player wants to start typing
            print(Back.BLACK+Fore.LIGHTWHITE_EX+cursorPos(117,77)+" "*30, end="")
            playerInput = input(cursorPos(117,77))
            if playerInput.lower()[:8] == "open inv":
                if player.isBattling == None:
                    player.invOpen = True
                    player.inv.scrollTop = 0
                    player.inv.selectChoice = 0
                    player.inv.renderMode = "main"
                    console.log("Opened Inventory, to exit type 'close inv'")
                    fillScreenWhite()
                else:
                    console.log("You can NOT open inventory while in battle!")

            elif playerInput.lower()[:9] == "close inv":
                player.invOpen = False
                console.log("Closed Inventory, to re-open tyoe 'open inv'")
                fillScreenWhite()

            elif playerInput.lower() == "help" or playerInput == "?":
                console.logCommands()

            elif playerInput.lower() == "exit game":
                console.log("Are you sure you want to exit game? Type yes if sure.")
                renderScreen()
                print(Back.BLACK+Fore.LIGHTWHITE_EX+cursorPos(117,77)+" "*30, end="")
                playerInput = input(cursorPos(117,77))
                if playerInput.lower() == "yes":
                    break

            else:
                console.log("Invalid command, for a list of commands type 'help' or '?'")
        else:
            player.keyInput(key)    # Send input into player class for processing
            if player.finished:  # If the player has finished, break the loop and finish.
                break
        if key in ["t","w","a","s","d","i","\r"]:   # Only render screen if what player pressed actually did something
            renderScreen()  # Render the screen

if player.finished:
    if player.curHP > 0:
        console.log(Fore.LIGHTGREEN_EX + "You escaped the dungeon! Congratulations!!!")
        renderScreen()
        #time.sleep(3)
        fillScreenWhite()
        print(Back.BLACK + Fore.WHITE, end="")
        print(stringAscii.stringToAscii("You Win!", 85, 30, 0), end="")
        input()

    else:
        console.log(Fore.LIGHTRED_EX + "You lose!")
        renderScreen()
        #time.sleep(3)
        fillScreenWhite()
        print(Back.BLACK + Fore.WHITE, end="")
        print(stringAscii.stringToAscii("You lose!", 85, 30, 0), end="")
        print(stringAscii.stringToAscii("Better luck next time...", 50, 40, 0), end="")
        input()