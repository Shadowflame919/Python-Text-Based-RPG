import math
import random
from colorama.colorama import *
init()

def cursorPos(x,y):
    return "\x1b[" + str(y) + ";" + str(x) + "H"


class World_Map():
    def __init__(self, player, enemyList, console):

        self.consoleClone = console
        self.playerClone = player   # A reference to the player class variable (not a copy, a reference)
        self.oldPlayerPos = self.playerClone.pos    # Stores the value of the players old position for when removing player from the map
        #self.playerOffset = [0,0]   # The offset from the maps center the player gets rendered at

        self.enemyList = enemyList


        self.mapSize = {"x":30, "y":20}

        self.floorColour = [Back.YELLOW, Fore.BLACK]
        self.floorPatterns = [
            [
                "      ",
                "      ",
                "      ",
                "      "
            ], [
                "      ",
                "    * ",
                "      ",
                "      "
            ], [
                "      ",
                "      ",
                " ^    ",
                "      "
            ], [
                "      ",
                "      ",
                "   .  ",
                "      "
            ], [
                "      ",
                "      ",
                "      ",
                "  ^   "
            ], [
                "      ",
                "  ~   ",
                "      ",
                "      "
            ]
        ]


            # The lowest layer which just determines the colour of the floor
            # This is mostly for ground colour (green, light green and brown) for grass/dirt
            # Also includes paths (grey) and other floor covers - maybe white/light grey for certain building floors
        self.floorLayer = []
        for y in range(self.mapSize["y"]):
            mapLayer = []
            for x in range(self.mapSize["x"]):
                if random.random() <= 0.5:  # % chance of nothing
                    mapLayer.append(0)
                else:   # Otherwise make the ground have some patterns
                    randFloor = random.randrange(1,6)
                    mapLayer.append(randFloor)

            self.floorLayer.append(mapLayer)


        # The second layer contains everything static that the player collides with
        # This includes walls, rocks, tree trunks?

        # All the different wall patterns
        self.staticCollideTypes = {
            1: [
                Back.LIGHTBLACK_EX + "      ",
                Back.LIGHTBLACK_EX + " test ",
                Back.LIGHTBLACK_EX + " wall ",
                Back.LIGHTBLACK_EX + "      "
            ], 2: [
                Back.WHITE + "      ",
                Back.WHITE + " /  \ ",
                Back.WHITE + " \  / ",
                Back.WHITE + "      "
            ], 3: [
                Back.WHITE + "THE   ",
                Back.WHITE + " ONLY ",
                Back.WHITE + "  WAY ",
                Back.WHITE + "   OUT"
            ], 10: [ # N
                Back.LIGHTBLACK_EX + Fore.BLACK + " │  │ ",
                Back.LIGHTBLACK_EX + Fore.BLACK + " │  │ ",
                Back.LIGHTBLACK_EX + Fore.BLACK + " │  │ ",
                Back.LIGHTBLACK_EX + Fore.BLACK + " └──┘ "
            ], 11: [ # N E
                Back.LIGHTBLACK_EX + Fore.BLACK + " │  └─",
                Back.LIGHTBLACK_EX + Fore.BLACK + " │    ",
                Back.LIGHTBLACK_EX + Fore.BLACK + " │    ",
                Back.LIGHTBLACK_EX + Fore.BLACK + " └────"
            ], 12: [ # N  W
                Back.LIGHTBLACK_EX + Fore.BLACK + "─┘  │ ",
                Back.LIGHTBLACK_EX + Fore.BLACK + "    │ ",
                Back.LIGHTBLACK_EX + Fore.BLACK + "    │ ",
                Back.LIGHTBLACK_EX + Fore.BLACK + "────┘ "
            ], 13: [ # N EW
                Back.LIGHTBLACK_EX + Fore.BLACK + "─┘  └─",
                Back.LIGHTBLACK_EX + Fore.BLACK + "      ",
                Back.LIGHTBLACK_EX + Fore.BLACK + "      ",
                Back.LIGHTBLACK_EX + Fore.BLACK + "──────"
            ], 14: [ # NS
                Back.LIGHTBLACK_EX + Fore.BLACK + " │  │ ",
                Back.LIGHTBLACK_EX + Fore.BLACK + " │  │ ",
                Back.LIGHTBLACK_EX + Fore.BLACK + " │  │ ",
                Back.LIGHTBLACK_EX + Fore.BLACK + " │  │ "
            ], 15: [ # NSE
                Back.LIGHTBLACK_EX + Fore.BLACK + " │  └─",
                Back.LIGHTBLACK_EX + Fore.BLACK + " │    ",
                Back.LIGHTBLACK_EX + Fore.BLACK + " │    ",
                Back.LIGHTBLACK_EX + Fore.BLACK + " │  ┌─"
            ], 16: [ # NS W
                Back.LIGHTBLACK_EX + Fore.BLACK + "─┘  │ ",
                Back.LIGHTBLACK_EX + Fore.BLACK + "    │ ",
                Back.LIGHTBLACK_EX + Fore.BLACK + "    │ ",
                Back.LIGHTBLACK_EX + Fore.BLACK + "─┐  │ "
            ], 17: [ # NSEW
                Back.LIGHTBLACK_EX + Fore.BLACK + "─┘  └─",
                Back.LIGHTBLACK_EX + Fore.BLACK + "      ",
                Back.LIGHTBLACK_EX + Fore.BLACK + "      ",
                Back.LIGHTBLACK_EX + Fore.BLACK + "─┐  ┌─"
            ], 18: [ #  S
                Back.LIGHTBLACK_EX + Fore.BLACK + " ┌──┐ ",
                Back.LIGHTBLACK_EX + Fore.BLACK + " │  │ ",
                Back.LIGHTBLACK_EX + Fore.BLACK + " │  │ ",
                Back.LIGHTBLACK_EX + Fore.BLACK + " │  │ "
            ], 19: [ #  SE
                Back.LIGHTBLACK_EX + Fore.BLACK + " ┌────",
                Back.LIGHTBLACK_EX + Fore.BLACK + " │    ",
                Back.LIGHTBLACK_EX + Fore.BLACK + " │    ",
                Back.LIGHTBLACK_EX + Fore.BLACK + " │  ┌─"
            ], 20: [ #  S W
                Back.LIGHTBLACK_EX + Fore.BLACK + "────┐ ",
                Back.LIGHTBLACK_EX + Fore.BLACK + "    │ ",
                Back.LIGHTBLACK_EX + Fore.BLACK + "    │ ",
                Back.LIGHTBLACK_EX + Fore.BLACK + "─┐  │ "
            ], 21: [ #  SEW
                Back.LIGHTBLACK_EX + Fore.BLACK + "──────",
                Back.LIGHTBLACK_EX + Fore.BLACK + "      ",
                Back.LIGHTBLACK_EX + Fore.BLACK + "      ",
                Back.LIGHTBLACK_EX + Fore.BLACK + "─┐  ┌─"
            ], 22: [ #   E
                Back.LIGHTBLACK_EX + Fore.BLACK + " ┌────",
                Back.LIGHTBLACK_EX + Fore.BLACK + " │    ",
                Back.LIGHTBLACK_EX + Fore.BLACK + " │    ",
                Back.LIGHTBLACK_EX + Fore.BLACK + " └────"
            ], 23: [ #   EW
                Back.LIGHTBLACK_EX + Fore.BLACK + "──────",
                Back.LIGHTBLACK_EX + Fore.BLACK + "      ",
                Back.LIGHTBLACK_EX + Fore.BLACK + "      ",
                Back.LIGHTBLACK_EX + Fore.BLACK + "──────"
            ], 24: [ #    W
                Back.LIGHTBLACK_EX + Fore.BLACK + "────┐ ",
                Back.LIGHTBLACK_EX + Fore.BLACK + "    │ ",
                Back.LIGHTBLACK_EX + Fore.BLACK + "    │ ",
                Back.LIGHTBLACK_EX + Fore.BLACK + "────┘ "
            ]
        }

        self.staticCollideLayer = [
            [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
            [1,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
            [1,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
            [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
            [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,1],
            [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,1],
            [1,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,1,1,1],
            [1,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
            [1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
            [1,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
            [1,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
            [1,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,1],
            [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,1],
            [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1],
            [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,1],
            [1,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0,0,1,1,1,0,1],
            [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,3,1,0,1],
            [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,0,1],
            [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
            [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
        ]

        # Run through entire map, setting walls to the correct orientation
        for yIndex in range(len(self.staticCollideLayer)):
            for xIndex in range(len(self.staticCollideLayer[yIndex])):
                tile = self.staticCollideLayer[yIndex][xIndex]
                if tile == 1:
                    # Booleans based on wall type surrounding tile
                    N = (yIndex > 0) and (self.staticCollideLayer[yIndex-1][xIndex] != 0)
                    S = (yIndex < len(self.staticCollideLayer)-1) and (self.staticCollideLayer[yIndex+1][xIndex] != 0)
                    E = (xIndex < len(self.staticCollideLayer[yIndex])-1) and (self.staticCollideLayer[yIndex][xIndex+1] != 0)
                    W = (xIndex > 0) and (self.staticCollideLayer[yIndex][xIndex-1] != 0)

                    wallTypes = {
                        "1000":10,  # N
                        "1010":11,  # N E
                        "1001":12,  # N  W
                        "1011":13,  # N EW
                        "1100":14,  # NS
                        "1110":15,  # NSE
                        "1101":16,  # NS W
                        "1111":17,  # NSEW
                        "0100":18,  #  S
                        "0110":19,  #  SE
                        "0101":20,  #  S W
                        "0111":21,  #  SEW
                        "0010":22,  #   E
                        "0011":23,  #   EW
                        "0001":24   #    W
                    }
                    self.staticCollideLayer[yIndex][xIndex] = wallTypes[str(int(N))+str(int(S))+str(int(E))+str(int(W))]




        self.entityLayer = []
        for y in range(self.mapSize["y"]):
            mapLayer = []
            for x in range(self.mapSize["x"]):
                mapLayer.append(0)
            self.entityLayer.append(mapLayer)

        # Add player to entityLayer
        self.entityLayer[self.playerClone.pos["y"]][self.playerClone.pos["x"]] = 1  # Player is a 1

        # Add enemies to entityLayer
        for enemyIndex,enemy in enumerate(self.enemyList):
            self.entityLayer[enemy.pos["y"]][enemy.pos["x"]] = [2, enemyIndex]    # Enemy is 2


    def updatePlayer(self):  # Tells the map to update itself by moving enemies and looking at new player position
        ## Update entityLayer positions

        # Update players position in entityLayer
        self.entityLayer[self.oldPlayerPos["y"]][self.oldPlayerPos["x"]] = 0  # Remove previous player position
        self.oldPlayerPos = self.playerClone.pos
        self.entityLayer[self.playerClone.pos["y"]][self.playerClone.pos["x"]] = 1  # Player is a 1

    def updateEnemies(self):
        for enemyIndex,enemy in enumerate(self.enemyList):
            oldPos = enemy.update()
            if oldPos != None:  # If enemy did actually move
                self.entityLayer[oldPos["y"]][oldPos["x"]] = 0  # Set old pos to a blank
                self.entityLayer[enemy.pos["y"]][enemy.pos["x"]] = [2, enemyIndex]    # Enemy is 2


        # Start battle with enemy if player is next to it.
        nextToEnemyIndex = self.playerClone.nextToEnemy()
        if nextToEnemyIndex != None:
            self.playerClone.startBattle(nextToEnemyIndex)

    def killEnemy(self, enemyIndex):
        deadEnemy = self.enemyList.pop(enemyIndex)
        self.entityLayer[deadEnemy.pos["y"]][deadEnemy.pos["x"]] = 0

        # After killing enemy, go though each enemy [2,i] set in the entityLayer and fix the new index
        for enemyIndex,enemy in enumerate(self.enemyList):
            self.entityLayer[enemy.pos["y"]][enemy.pos["x"]] = [2, enemyIndex]


    def drawString(self, x, y, w, h):    # Returns the string to draw the map at an x,y with a particular width/height
        # There MUST be a divisibility of width:6 and height:4 for the map to render properly and both MUST BE ODD so player is rendered in the center

        # Need to make each 6x4 tile look good, add different kinds of colours in each tile.
        # Make enemies render and move every time player moves
        # Make sure im always optimising rendering!

        tileAmountX = int(w/6)   # No. of 6 wide tiles that fit horizonatally across map
        tileAmountY = int(h/4)   # No. of 4 high tiles that fit vertically on map

        tileIndexLeft = self.playerClone.pos["x"] - int((tileAmountX-1)/2)
        tileIndexTop =  self.playerClone.pos["y"] - int((tileAmountY-1)/2)

        mapString = Style.NORMAL

        for tileY in range(tileAmountY):   # For each tile working downwards
            tileYIndex = tileIndexTop + tileY  # Y Index of current tile

            for tileLayer in range(4):  # For all 4 horizontal layers of the tile

                mapString += cursorPos(x, y+tileY*4+tileLayer)   # Set cursor position to left most of screen, with y pos at the current horizontal layer of tile
                
                for tileX in range(tileAmountX):   # For each tile working across
                    tileXIndex = tileIndexLeft + tileX  # X Index of current tile

                    if (0 <= tileXIndex < self.mapSize["x"]) and (0 <= tileYIndex < self.mapSize["y"]):   # Only render colours and stuff if tile is inside map
                        entityObject = self.entityLayer[tileYIndex][tileXIndex]     # The value of this index on the entity layer
                        if entityObject == 0:   # No entity is on this tile index
                            staticCollideType = self.staticCollideLayer[tileYIndex][tileXIndex]
                            floorType = self.floorLayer[tileYIndex][tileXIndex]

                            if staticCollideType == 0:  # No static collider on this tile
                                mapString += self.floorColour[0] + self.floorColour[1]  # Add the colour of the floor tile
                                mapString += self.floorPatterns[floorType][tileLayer]
                            else:
                                mapString += self.staticCollideTypes[staticCollideType][tileLayer]  # Add the current layer of the static collidable tile

                        else:   # An entity IS on the tile index
                            if entityObject == 1:   # Player on tile index
                                playerMapTile = self.playerClone.mapTile  # Equals the map tile of the player
                                mapString += playerMapTile[-1][0] + playerMapTile[-1][1]    # Print the players default drawing colours

                                for char in playerMapTile[tileLayer]:   # For each character on this tile layer
                                    if char == "$":    # If player is transparent at this point
                                        mapString += self.floorColour[0]     # Print the floors background colour
                                    elif char == "%":   # If player wants to be seen on this character
                                        mapString += playerMapTile[-1][0]   # Print players background colour
                                    else:   # If neither, print the player's character at this spot
                                        mapString += char

                            elif (type(entityObject) is list) and (entityObject[0] == 2):   # Enemy on tile index
                                enemyMapTile = self.enemyList[entityObject[1]].mapTile  # Equals the map tile of the enemy
                                mapString += enemyMapTile[-1][0] + enemyMapTile[-1][1]       # Print the enemies default drawing colours

                                for char in enemyMapTile[tileLayer]:   # For each character on this tile layer
                                    if char == "$":    # If enemy is transparent at this point
                                        mapString += self.floorColour[0]     # Print the floors background colour
                                    elif char == "%":   # If enemy wants to be seen
                                        mapString += enemyMapTile[-1][0]   # Print enemies background colour
                                    elif char == "Y":   # If enemy is king
                                        mapString += Fore.LIGHTYELLOW_EX   # Print yellow
                                    else:   # If neither, print the enemy character at this spot
                                        mapString += char


                    else:   # Tile is not inside map
                        mapString += Back.BLACK # Add background colour for tile outside of map
                        mapString += " "*6
   
        return mapString
