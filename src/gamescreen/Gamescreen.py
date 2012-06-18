# -*- coding: utf-8 -*-
"""
    This file contains methods for drawing the rectangle areas displaying the stats and game messages.
"""
from pygame import Rect, font, Color

def make_stats_box(screen, player, dungeon_level, box_x_start, box_heigth, box_width):
    """Create the box displaying the stats
       @param screen: the screen to draw on
       @param player: the player object
       @param dungeon_level: the current dungeon level
       @param box_x_start: rectangle upper left corner x-coordinate 
       @param box_heigth: height of rectangle
       @param box_width: width of rectangle
    """

    #create the rectangle
    stats_box = Rect(box_x_start, 0, box_width, box_heigth)
    #set font type
    stats_font = font.SysFont('arial', 20)
    #render game info
    player_HP = stats_font.render("Hit Points: " + str(player.getHP()), True, Color('white'))
    player_AP = stats_font.render("Attack Power: " + str(player.getAttackPower()), True, Color('white'))
    player_Armor = stats_font.render("Armor: " + str(player.getArmor()), True, Color('white'))
    level = stats_font.render("Dungeon Level: " + str(dungeon_level), True, Color('white'))

    #For each line of text, draw it on the screen and move the rectangle for the next line
    screen.fill(Color('Black'), stats_box)
    screen.blit(player_HP, stats_box)
    screen.blit(player_AP, stats_box.move(0, player_HP.get_height()))
    screen.blit(player_Armor, stats_box.move(0, player_HP.get_height() + player_AP.get_height()))
    screen.blit(level, stats_box.move(0, player_HP.get_height() + player_AP.get_height() + player_Armor.get_height()))

def make_message_box(screen, box_y_start, box_heigth, box_width, gameMessage):
    """Make the box/rectangle displaying the game messages
       @param screen: the screen to draw on
       @param box_y_start: rectangle upper left y-coordinate
       @param box_heigth: message rectangle height
       @param box_width: message rectangle width
       @gameMessage: the message to display
    """

    #Create rectangle
    message_box = Rect(0, box_y_start, box_width, box_heigth)
    #set font type
    message_font = font.SysFont('arial', 20)
    #render message
    message = message_font.render(gameMessage, True, Color('White'))
    #display
    screen.fill(Color('Black'), message_box)
    screen.blit(message, message_box)
