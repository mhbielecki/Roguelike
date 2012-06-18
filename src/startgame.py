"""
   This is the file where all the magic happens. It contains methods for setting up
   and running the game, aswell as creating different game objects.
"""

import pygame, sys, random, os, time
from mapgenerator import mapgen
from gameobjects_and_movement import GameObject
from gamescreen import Gamescreen
from battlesystem import battlecalc

"""Game constants"""
MONSTER_COUNT = 15
STATS_BOX_WIDTH = 200
MESSAGE_BOX_HEIGHT = 64
STATS_BOX_OFFSET = 10
dungeonLevel = 1 #dungeon level starts at 1


def set_up(MAP_WIDTH, MAP_HEIGHT):
    """This method initializes and sets up the game
       @param MAP_WIDTH: the map(playable area) width
       @param MAP_HEIGHT: the map(playable area) height
    """

    global dungeonLevel

    #initializa pygame modules
    pygame.init()

    #Get a screen object to draw on
    #Total screen size is MAP_WIDTH + 265 (stats box) and MAP_HEIGHT + 128 (message box)
    screen = pygame.display.set_mode((MAP_WIDTH + STATS_BOX_WIDTH, MAP_HEIGHT + MESSAGE_BOX_HEIGHT), 0, 32)

    pygame.display.set_caption("INF3331 Roguelike Project")

    # Create the first cave. This can take a couple of seconds to make
    cave = mapgen.run_mapgen(MAP_WIDTH, MAP_HEIGHT, screen)

    #load monster images
    monster_images = [
        'graphics/Ikoner/giant_cockroach.png',
        'graphics/Ikoner/brain_worm.png',
        'graphics/Ikoner/mummy.png',
        'graphics/Ikoner/ogre_mage.png',
        'graphics/Ikoner/red_dragon.png',
    ]

    monster_tiles = [pygame.image.load(img).convert_alpha() for img in monster_images]

    #Load item images
    door_image = 'graphics/Ikoner/wooden_door.png'
    armor_image = 'graphics/Ikoner/armor.png'
    food_image = 'graphics/Ikoner/potion.png'
    weapon_image = 'graphics/Ikoner/sword.png'

    armor_tile = pygame.image.load(armor_image).convert_alpha()
    food_tile = pygame.image.load(food_image).convert_alpha()
    weapon_tile = pygame.image.load(weapon_image).convert_alpha()
    door_tile = pygame.image.load(door_image).convert_alpha()

    #create player object
    player_image = pygame.image.load('graphics/Ikoner/player.png').convert_alpha()
    player = GameObject.Player(screen, position=(random.randrange(0, MAP_WIDTH, 16), random.randrange(0, MAP_HEIGHT,
                    16)), object_image=player_image, object_cave=cave, dungeon_level=dungeonLevel)

    #Run game
    run_game(screen, cave, player, monster_tiles, armor_tile, food_tile, weapon_tile, door_tile, MAP_HEIGHT, MAP_WIDTH)

def make_items(screen, cave, MAP_WIDTH, MAP_HEIGHT, armor_tile, food_tile, weapon_tile, door_tile):
    """Creates the different items and put them in a list
       @param screen: the game screen to draw
       @param cave: the map
       @param MAP_WIDTH: the map width (playable area) in pixels
       @param MAP_HEIGHT: the map heith (playable area) in pixels
       @param armor_tile: armor image
       @param food_tile: potion image
       @param weapon_tile: weapon image
       @param door_tile: door image
       @return: list of items
    """
    items = []

    for i in range(3):
        #Make armor item
        items.append(GameObject.Item(
                screen,
                position=(random.randrange(0, MAP_WIDTH, 16), random.randrange(0, MAP_HEIGHT, 16)),
                object_image=armor_tile,
                object_cave=cave,
                name="armor",
                value=1))

        #Make weapon item
        items.append(GameObject.Item(
                screen,
                position=(random.randrange(0, MAP_WIDTH, 16), random.randrange(0, MAP_HEIGHT, 16)),
                object_image=weapon_tile,
                object_cave=cave,
                name="weapon",
                value=1))

    #Make food item
    for i in range(4):
        items.append(GameObject.Item(
                screen,
                position=(random.randrange(0, MAP_WIDTH, 16), random.randrange(0, MAP_HEIGHT, 16)),
                object_image=food_tile,
                object_cave=cave,
                name="food",
                value=20))

    #make door
    items.append(GameObject.Item(
            screen,
            position=(random.randrange(0, MAP_WIDTH, 16), random.randrange(0, MAP_HEIGHT, 16)),
            object_image=door_tile,
            object_cave=cave,
            name="wooden door",
            value=0))

    return items

def make_monsters(screen, cave, MAP_WIDTH, MAP_HEIGHT, monster_tiles, dungeonLevel):
    """Monsters change their stats and are killed in each level, so create new monsters when a new level is started
       @param screen: the game screen to draw
       @param cave: the map
       @param MAP_WIDTH: the map width (playable area) in pixels
       @param MAP_HEIGHT: the map heith (playable area) in pixels
       @param monster_tiles: monster images
       @param dungeonLevel: the current dungeon level
       @return: list of monsters
    """

    monsters = []

    for i in range(MONSTER_COUNT):
        monsters.append(GameObject.Monster(
            screen,
            position=(random.randrange(0, MAP_WIDTH, 16), random.randrange(0, MAP_HEIGHT, 16)),
            object_image=monster_tiles[random.randint(0, len(monster_tiles)-1)],
            object_cave=cave,
            dungeon_level=dungeonLevel))

    return monsters

def removeMonster(monsters):
    """Remove dead monsters from the monster list
       @param monsters: list of monsters
    """

    for m in monsters:
        if m.getHP() <= 0:
            monsters.remove(m)

def run_game(screen, cave, player, monster_tiles, armor_tile, food_tile, weapon_tile, door_tile, MAP_HEIGHT, MAP_WIDTH):
    """Run the game and the contains the main game loop
       @param screen: the game screen to draw
       @param cave: the map
       @param player: the player object
       @param monster_tiles: monster images
       @param armor_tile: armor image
       @param food_tile: potion image
       @param weapon_tile: weapon image
       @param door_tile: door image
       @param MAP_HEIGHT: the map heith (playable area) in pixels
       @param MAP_WIDTH: the map width (playable area) in pixels
    """

    global dungeonLevel

    #Make list of monsters
    monsters = make_monsters(screen, cave, MAP_WIDTH, MAP_HEIGHT, monster_tiles, dungeonLevel)
    items = make_items(screen, cave, MAP_WIDTH, MAP_HEIGHT, armor_tile, food_tile, weapon_tile, door_tile)

    #get clock so we can control frames per second
    clock = pygame.time.Clock()
    gameMessage = ""

    #Main game loop - should probably be refactored (if time)
    while True:

        clock.tick(5) #Limit the screen to 5 FPS

        #go through events
        for event in pygame.event.get():

            #player clicked close button
            if event.type == pygame.QUIT:
                exit_game()

            #a key has been pressed
            if event.type == pygame.KEYDOWN:

                #move player
                if event.key == pygame.K_DOWN or \
                    event.key == pygame.K_UP or \
                    event.key == pygame.K_LEFT or \
                    event.key == pygame.K_RIGHT:
                        player.handleKey(event, monsters)
                        gameMessage = monsterMoveAndAttack(monsters, player, screen, MAP_HEIGHT, MAP_WIDTH, MESSAGE_BOX_HEIGHT)

                elif event.key == pygame.K_s:
                    #Use item
                    gameMessage = monsterMoveAndAttack(monsters, player, screen, MAP_HEIGHT, MAP_WIDTH, MESSAGE_BOX_HEIGHT)

                    for item in items:
                        if item.getPosition() == player.getPosition():
                            if item.getItemName() == "wooden door":
                                #Increase dungeonlevel
                                dungeonLevel += 1
                                #make new cave
                                cave = mapgen.run_mapgen(MAP_WIDTH, MAP_HEIGHT, screen)
                                #update player object
                                player.update(cave, (random.randrange(0, MAP_WIDTH, 16), random.randrange(0,
                                                MAP_HEIGHT, 16)))
                                #make new monster list
                                monsters = make_monsters(screen, cave, MAP_WIDTH, MAP_HEIGHT, monster_tiles, dungeonLevel)
                                items = make_items(screen, cave, MAP_WIDTH, MAP_HEIGHT, armor_tile, food_tile, weapon_tile, door_tile)
                                gameMessage = "New dungeon level! " + gameMessage

                            elif item.getItemName() == "weapon":
                                player.increaseAP(item.useItem())
                                gameMessage = "You picked up a sword! Attack power increased by " + str(item.useItem()) \
                                               + "! " + gameMessage
                                items.remove(item)

                            elif item.getItemName() == "armor":
                                player.increaseArmor(item.useItem())
                                gameMessage = "You picked up a shiny piece of armor! Armor increased by " + str(item.useItem()) \
                                               + "! " + gameMessage
                                items.remove(item)

                            elif item.getItemName() == "food":
                                player.increaseHP(item.useItem())
                                gameMessage = "You picked up a potion! Hit points increased by " + str(item.useItem()) \
                                               + "! " + gameMessage

                                items.remove(item)


                #player attack (A key pressed)
                elif event.key == pygame.K_a:

                    attackDir = 'D' #DEFAULT DIRECTION

                    Gamescreen.make_message_box(screen, MAP_HEIGHT, MESSAGE_BOX_HEIGHT, MAP_WIDTH, "Where do you want to attack?")
                    pygame.display.flip()
                    pygame.event.set_blocked(pygame.KEYUP)      #Block KEYUP so its not added to the event queue
                    attackWhere = pygame.event.wait()           #Wait for an event

                    #get attack direction
                    if attackWhere.key == pygame.K_DOWN:
                        attackDir = 'D'

                    elif attackWhere.key == pygame.K_UP:
                        attackDir = 'U'

                    elif attackWhere.key == pygame.K_LEFT:
                        attackDir = 'L'

                    elif attackWhere.key == pygame.K_RIGHT:
                        attackDir = 'R'

                    #calculate battle outcome
                    battleresult = battlecalc.playerAttack(monsters, player, attackDir)
                    monsterAttackMessage = monsterMoveAndAttack(monsters, player, screen, MAP_HEIGHT, MAP_WIDTH, MESSAGE_BOX_HEIGHT)

                    if battleresult[0]:
                        gameMessage = "You hit the monster for " + str(battleresult[1]) + "! You killed the monster! " + \
                        monsterAttackMessage
                    elif battleresult[1] == 0:
                        gameMessage = "Nothing to hit here! " + monsterAttackMessage
                    else:
                        gameMessage = "You hit the monster for " + str(battleresult[1]) + "! " + monsterAttackMessage

                    removeMonster(monsters)

                #Dig down wall(D key pressed)
                elif event.key == pygame.K_d:

                    Gamescreen.make_message_box(screen, MAP_HEIGHT, MESSAGE_BOX_HEIGHT, MAP_WIDTH, "Where do you want to dig?")
                    pygame.display.flip()

                    pygame.event.set_blocked(pygame.KEYUP) #Block KEYUP so its not added to the event queue
                    digWhere = pygame.event.wait()         #Wait for an event

                    try:
                        if digWhere.key == pygame.K_DOWN:
                            mapgen.updateCave(screen, cave, 'D', player.getXposition(), player.getYposition())
                            gameMessage = "You dig down"

                        elif digWhere.key == pygame.K_UP:
                            mapgen.updateCave(screen, cave, 'U', player.getXposition(), player.getYposition())
                            gameMessage = "You dig up"

                        elif digWhere.key == pygame.K_LEFT:
                            mapgen.updateCave(screen, cave, 'L', player.getXposition(), player.getYposition())
                            gameMessage = "You dig left"

                        elif digWhere.key == pygame.K_RIGHT:
                            mapgen.updateCave(screen, cave, 'R', player.getXposition(), player.getYposition())
                            gameMessage = "You dig right"

                        gameMessage = monsterMoveAndAttack(monsters, player, screen, MAP_HEIGHT, MAP_WIDTH, MESSAGE_BOX_HEIGHT)
                    except:
                        print "DEBUG: Event bugged out"

                break #only one event is handled at a time, so break out of the event loop after one event is finished

        #Divide by 16 to get correct tile index
        for y in range(0, MAP_HEIGHT / 16):
            for x in range(0, MAP_WIDTH / 16):
                cave[y][x].draw()

        #draw player, monsters and items
        player.draw()

        for m in monsters:
            m.draw()

        for i in items:
            i.draw()

        #Make stats box and display it
        Gamescreen.make_stats_box(screen, player, dungeonLevel, MAP_WIDTH, MAP_HEIGHT, STATS_BOX_WIDTH)
        Gamescreen.make_message_box(screen, MAP_HEIGHT, MESSAGE_BOX_HEIGHT, MAP_WIDTH, gameMessage)

        #Display
        pygame.display.flip()

def monsterMoveAndAttack(monsters, player, screen, MAP_HEIGHT, MAP_WIDTH, MESSAGE_BOX_HEIGHT):
    """Monsters can move and attack the player
       @param monsters: list of monsters
       @param player: the played object
       @param screen: the screen to draw on
       @param MAP_HEIGHT: the mapheight(playable area) in pixels
       @param MAP_WIDTH: the mapwidth(playable area) in pixels
       @param MESSAGE_BOX_HEIGHT: the height of the message box rectangle
    """

    global dungeonLevel

    #go through the monsters one at a time
    for m in monsters:
        checkIfFoundPlayer = m.findPlayer(player, monsters)

        #if -1 is returned, the player is not nearby
        if checkIfFoundPlayer == -1:
            m.walk(monsters, player)

    #Monster attack!
    monsterAttackResult = battlecalc.monsterAttack(monsters, player)

    #player died
    if monsterAttackResult[0]:

        Gamescreen.make_stats_box(screen, player, dungeonLevel, MAP_WIDTH, MAP_HEIGHT, STATS_BOX_WIDTH)
        Gamescreen.make_message_box(screen, MAP_HEIGHT, MESSAGE_BOX_HEIGHT, MAP_WIDTH, "The monster(s) around you " \
                "slaughtered you for " + str(monsterAttackResult[1]) + " damage! You died!")
        pygame.display.flip()
        game_over()
    #player still alive
    else:
        if monsterAttackResult[1] != 0:
            return "The monster(s) around you hit you for " + str(monsterAttackResult[1]) + " damage!"
        else:
            return ""

def game_over():
    """This is called when a player dies. Wait 5 seconds before quitting the program"""
    time.sleep(5)
    exit_game()

def exit_game():
    """Exit the game"""
    sys.exit()

