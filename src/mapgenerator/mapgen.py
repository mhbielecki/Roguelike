# -*- coding: utf-8 -*-
"""roguelike cave generator using cellular automata.
   Based on the algorithm in the article found here:
   http://roguebasin.roguelikedevelopment.org/index.php/Cellular_Automata_Method_for_Generating_Random_Cave-Like_Levels 
"""

import pygame, sys, random, os

#Constants for the cave map generator
#These settings can be changed to generate different kinds of maps.
#Try changing these to see the different results
#Standard settings (6, 5, 0, 40)
ITERATIONS = 6
WALLFACTOR = 5      #CA rule one
WALLFACTOR2 = 0    #CA rule two
FILLFACTOR = 40     #45% of the tiles will initially be ground tiles

WALL_TILE = 'graphics/Ikoner/wall_16.png'
GROUND_TILE = 'graphics/Ikoner/ground3_16.png'

class Tile:
    """This class is for wall and ground tile objects"""

    def __init__(self, passable, digable, position, screen, tile_image):
        """Constructor
        @param passable: true if tile is passable, false if not
        @param digable: true if tile is digable, false if not
        @param position: tuple representing this tiles position in pixels
        @param screen: the screen to draw on
        @param tile_image: the tile image
        """
        self.passable = passable
        self.digable = digable
        self.position = position
        self.screen = screen
        self.tile_image = tile_image

    def draw(self):
        """Draw the tile image on the screen"""
        self.screen.blit(self.tile_image, self.position)

    def isPassable(self):
        """Check if this tile is passable or not
           @return: true if this tile is passable, false if not
        """
        return self.passable

    def isDigable(self):
        """Check if this tile is digable
           @return: true if this tile is digable, false if not
        """
        return self.digable

    def updateTile(self, passable, tile):
        """Update the tile
           @param passable: new passable value
           @param tile: new tile image
        """
        self.passable = passable
        self.tile_image = tile

    def getXposition(self):
        """Get the tiles x-cord
           @return: x-cord of tile
        """
        return self.position[0]

    def getYposition(self):
        """Get the tiles y-cord
           @return: y-cord of tile
        """
        return self.position[1]


def calculateNearbyWalls(tile, cave):
    """Calculate number of adjacent walls
       @param cave: the map
       @return: number of adjacent walls
    """

    numwalls = 0

    """Loop through the 8 adjacent tiles surrounding"""
    for y in range(-1, 2*1):
        for x in range(-1, 2*1):

            #skip self
            if y == 0 and y == x:
                continue
            if not cave[(tile.getYposition() / 16) + y][(tile.getXposition() / 16) + x].isPassable():
                numwalls += 1

    return numwalls


def generate(xCord, yCord, wall_image, ground_image, screen):
    """Generate the cave using cellular automata. The rules are as follows:
       If a tile has at least WALLFACTOR adjacent walls, make it a wall.
       If a tile has WALLFACTOR2 adjacent wall tiles, make it a wall
       All other tiles are ground tiles
       The cave generator can take a few seconds to complete, depending on map size.
       A problem with this generator is that the cave can be disconnected.
       With the current settings, most the caves generated seems ok
       @param xCord: map width
       @param yCord: map height
       @param wall_image: image for wall tiles
       @param ground_image: image for ground tiles
       @param screen: the game screen to draw on
       @return: the generated cave
       """

    #The cavemap is a 2D list of tile objects
    cave = [[ None for x in range(0, xCord, 16)] for y in range(0, yCord, 16)]

    #Init cave. The cave edges are wall tiles, the rest are random
    for y in range(0, int(yCord / 16)):
        for x in range(0, int(xCord / 16)):
            #Make walls around border
            if x == 0 or y == 0 or y == (yCord / 16) - 1 or x == (xCord / 16) - 1:
                cave[y][x] = Tile(passable=False, digable=False, position=(x*16, y*16), screen=screen, tile_image=wall_image)
            #Make ground tile
            elif random.randint(0, 100) > FILLFACTOR:
                cave[y][x] = Tile(passable=True, digable=True, position=(x*16, y*16), screen=screen, tile_image=ground_image)
            #Make wall tile
            else:
                cave[y][x] = Tile(passable=False, digable=True, position=(x*16, y*16), screen=screen, tile_image=wall_image)

    #Iteratively build the cave
    for iteration in range(ITERATIONS):

        #lists of tiles to be updated
        tilesToWall = []
        tilesToGround = []

        for y in range(0, int(yCord / 16)):
            for x in range(0, int(xCord / 16)):

                #Dont do anything to border walls
                if x == 0 or y == 0 or y == (yCord / 16) - 1 or x == (xCord / 16) - 1:
                    continue

                #Calculate number of adjacent wall tiles
                adjacentWalls = calculateNearbyWalls(cave[y][x], cave)
                if adjacentWalls >= WALLFACTOR or adjacentWalls == WALLFACTOR2:
                    tilesToWall.append(cave[y][x])
                else:
                    tilesToGround.append(cave[y][x])

        #Update tiles
        for tile in tilesToWall:
            tile.updateTile(False, wall_image)
        for tile in tilesToGround:
            tile.updateTile(True, ground_image)

    return cave

def run_mapgen(MAP_WIDTH, MAP_HEIGHT, screen):
    """Load map tiles, make a call to generate and return the cave represented by a 2D list of Tile objects
       @param MAP_WIDTH: the map width in pixels
       @param MAP_HEIGHT: the map height in pixels
       @return the generated cave
    """

    wall_image = pygame.image.load(WALL_TILE).convert_alpha()
    ground_image = pygame.image.load(GROUND_TILE).convert_alpha()

    # This can take a couple of seconds to make
    return generate(MAP_WIDTH, MAP_HEIGHT, wall_image, ground_image, screen)

def updateCave(screen, cave, direction, xpos, ypos):
    """Update the cave if a user wants to dig down a wall
       @param screen: the screen to draw on
       @param cave: the cave to change
       @param direction: dig direction
       @param xpos: xcord to the tile to update
       @param ypos: ycord to the tile to update
       """

    ground_image = pygame.image.load(GROUND_TILE).convert_alpha()

    if direction == 'D' and cave[(ypos/16) + 1][xpos / 16].isDigable(): #Dig down
        cave[(ypos/16) + 1][xpos / 16].updateTile(True, ground_image)

    elif direction == 'U' and cave[(ypos/16) - 1][xpos / 16].isDigable(): #Dig up
        cave[(ypos/16) - 1][xpos / 16].updateTile(True, ground_image)

    elif direction == 'L' and cave[(ypos/16)][(xpos / 16) - 1].isDigable(): #Dig up
        cave[(ypos/16)][(xpos / 16) - 1].updateTile(True, ground_image)

    elif direction == 'R' and cave[(ypos/16)][(xpos / 16) + 1].isDigable(): #Dig up
        cave[(ypos/16)][(xpos / 16) + 1].updateTile(True, ground_image)

