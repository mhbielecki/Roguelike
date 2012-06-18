# -*- coding: utf-8 -*-

import pygame, random
from pygame.sprite import Sprite

PIXELS = 16 #width and height of a tile

DIRECTION = ['L', 'R', 'D', 'U'] #Left, right, down, up

class GameObject(Sprite):
    """A generic class for containing methods for the different game objects"""

    def __init__(self, screen, position, object_image, object_cave):
        """ Constructor
            @param screen: the screen to draw on
            @param position: the objects position representet by a tuple
            @param object_image: the object image
            @param object_cave: the map
        """
        self.screen = screen
        self.object_image = object_image
        self.cave = object_cave
        self.position = self.legalStartPosition(position[0], position[1])


    def update(self, cave, position):
        """Update the game object
           @param cave: the map
           @param position: the new position
        """
        self.cave = cave
        self.position = self.legalStartPosition(position[0], position[1])

    def draw(self):
        """method for drawing object on screen"""
        self.screen.blit(self.object_image, self.position)

    def getXposition(self):
        """Get tile x postition
           @return: the X coordinate (in pixels)
        """
        return self.position[0]

    def getYposition(self):
        """Get tile y position
            @return: the y coordinate (in pixels)
        """
        return self.position[1]

    def getPosition(self):
        """Get the position in tuple
           @return: tuple of x and y coordinate (in pixels)
        """
        return (self.getXposition(), self.getYposition())

    def legalStartPosition(self, x, y):
        """Check if the position given is a valid start position. Recursice function
           @return: the position where it's ligal to start
           @return: call legalStartPosition-method again if it wasn't legal to start in that position
           """

        #Is this tile a wall, True if not, False if it is a wall
        if self.cave[y/16][x/16].isPassable():
            return (x, y)
        else:
            return self.legalStartPosition(random.randrange(0, len(self.cave[0])*16, 16), random.randrange(0,
                        len(self.cave)*16, 16))

class MovableCharacter(GameObject):
    """Class for movable objects"""

    def __init__(self, screen, position, object_image, object_cave, dungeon_level):
        """Constructor
           send all parameters to super-class GameObject
        """
        super(MovableCharacter, self).__init__(screen, position, object_image, object_cave)


    def move(self, x, y):
        """Monsters and the player can move around"""
        self.position = ((self.getXposition()+x), (self.getYposition()+y))

    def getHP(self):
        """Get hitpoint
           @return: Value hitpoint for monster or player
        """
        return self.hitPoints

    def getArmor(self):
        """Get armor
           @return: value of armoer for monster or player
        """
        return self.armor

    def getAttackPower(self):
        """Get attack power
           @return: Value of attack power for monster or player
        """
        return self.attackPower

    def increaseHP(self, amount):
        """Increase hitpoint with value of amount
        """
        self.hitPoints += amount

    def increaseArmor(self, amount):
        """Increase armor with value of amount
        """
        self.armor += amount

    def increaseAP(self, amount):
        """Increase attack power with value of amount
        """
        self.attackPower += amount

    def decreaseHP(self, amount):
        """Decrease hit power with amount, hitpower can't go lower than 0
        """

        #Does hitpoints get under 0?
        if (self.hitPoints - amount) <= 0:
            self.hitPoints = 0
        else:
            self.hitPoints -= amount

    def checkValidMove(self, y, x, monsterList, player):
        """Check if a move is legal
           @return: False, if it is a monster, player or a wall in postion x and y
           @return: True, if it is a legal move
        """

        for m in monsterList:
            if (m.getXposition() == x) and (m.getYposition() == y):
                return False

        if player is not None and ((player.getXposition() == x) and player.getYposition() == y):
            return False

        return self.cave[y/PIXELS][x/PIXELS].isPassable()

class Player(MovableCharacter):
    """Class for playable character"""

    def __init__(self, screen, position, object_image, object_cave, dungeon_level):
        """Constructor
           send all parameters to super-class MovableCharacter
        """
        super(Player, self).__init__(screen, position, object_image, object_cave, dungeon_level)
        self.hitPoints = 150    #HP
        self.armor = 3          #Armor reduces damage take
        self.attackPower = 10   #Attackpower increases damage done


    def handleKey(self, event, monsterList):
        """Handle the key-event when the user press down arrows. If it is a legal move, it move the player in that direction which user pressed (Arrows-keys)
        """
        if event.key == pygame.K_LEFT:
            if self.checkValidMove(self.getYposition(), (self.getXposition()-PIXELS), monsterList, None):
                self.move(-PIXELS, 0)
        elif event.key == pygame.K_RIGHT:
            if self.checkValidMove(self.getYposition(), (self.getXposition()+PIXELS), monsterList, None):
                self.move(PIXELS,0)
        elif event.key == pygame.K_UP:
            if self.checkValidMove((self.getYposition()-PIXELS), self.getXposition(), monsterList, None):
                self.move(0, -PIXELS)
        elif event.key == pygame.K_DOWN:
            if self.checkValidMove((self.getYposition()+PIXELS), self.getXposition(), monsterList, None):
                self.move(0, PIXELS)

class Monster(MovableCharacter):
    """A class for monsters/enemies"""

    def __init__(self, screen, position, object_image, object_cave, dungeon_level):
        """Constructor
           Send all parameters to super-class MovableCharacter
        """
        super(Monster, self).__init__(screen, position, object_image, object_cave, dungeon_level)
        self.direction = DIRECTION[random.randint(0, len(DIRECTION)-1)]
        self.hitPoints = 25 + (dungeon_level*4) #HP
        self.armor = 2 + (dungeon_level * 2)  #Armor reduces damage taken
        self.attackPower = 6 + (dungeon_level*2)  #Attackpower increases damage done

    def walk(self, monsterList, player):
        """Move a monster in a random direction, if it hit a wall or another monster, we choose a new random direction
        """
        if self.direction == 'L':
            if self.checkValidMove(self.getYposition(), (self.getXposition()-PIXELS), monsterList, player):
                self.move(-PIXELS, 0)
            else:
                self.direction = DIRECTION[random.randint(0, len(DIRECTION)-1)]

        elif self.direction == 'R':
            if self.checkValidMove(self.getYposition(), (self.getXposition()+PIXELS), monsterList, player):
                self.move(PIXELS,0)
            else:
                self.direction = DIRECTION[random.randint(0, len(DIRECTION)-1)]

        elif self.direction == 'U':
            if self.checkValidMove((self.getYposition()-PIXELS), self.getXposition(), monsterList, player):
                self.move(0, -PIXELS)
            else:
                self.direction = DIRECTION[random.randint(0, len(DIRECTION)-1)]

        elif self.direction == 'D':
            if self.checkValidMove((self.getYposition()+PIXELS), self.getXposition(), monsterList, player):
                self.move(0, PIXELS)
            else:
                self.direction = DIRECTION[random.randint(0, len(DIRECTION)-1)]


    def findPlayer(self, player, monsterList):
        """Find out if a player is in range for a monster, if a player is in range of max 5 tiles. The monster move towards the player to attack it
           @return: 1 if the player is in range
           @return: -1 if the player is not in range
        """

        #Find out how far the player is
        costFromMonsterToPlayer = (abs((self.getXposition()/PIXELS) - (player.getXposition()/PIXELS)) + abs((self.getYposition()/PIXELS) - (player.getYposition()/PIXELS)))

        #Move towards the player if the player is in rage
        if costFromMonsterToPlayer <= 5:

            #Are the player to the left or to the rigt of the monster
            if self.getXposition() > player.getXposition():
                dirX = -PIXELS
            elif self.getXposition() < player.getXposition():
                dirX = PIXELS
            else:
                dirX = 0

            #Are the player to the left  or to the rigt of the monster
            if self.getYposition() > player.getYposition():
                dirY = -PIXELS
            elif self.getYposition() < player.getYposition():
                dirY = PIXELS
            else:
                dirY = 0

            #Can we move to the new position?
            if self.checkValidMove(self.getYposition(), self.getXposition() + dirX, monsterList, player):
                    self.move(dirX, 0)
                    return 1
            elif self.checkValidMove(self.getYposition() + dirY, self.getXposition(), monsterList, player):
                    self.move(0, dirY)
                    return 1
        else:
             return -1

class Item(GameObject):
    """Class for items"""

    def __init__(self, screen, position, object_image, object_cave, name, value):
        """Constructor
           Send all parameter except name and value to super-class GameObject
        """
        super(Item, self).__init__(screen, position, object_image, object_cave)
        self.itemName = name
        self.itemValue = value

    def getPosition(self):
        """Get the position in tuple
           @return: tuple of x and y coordinate (in pixels)
        """
        return (self.getXposition(), self.getYposition())

    def useItem(self):
        """If a item is picked up
           @return: The value of that item
        """
        return self.itemValue

    def getItemName(self):
        """Get the name of the item
           @return: name of the item
        """
        return self.itemName


