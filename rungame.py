# -*- coding: utf-8 -*-
"""This file starts the program"""

from src import startgame

#Constants for the playable field. Must be dividable with 16 (tile size in pixels)
MAP_HEIGHT = 512
MAP_WIDTH = 1024

startgame.set_up(MAP_WIDTH, MAP_HEIGHT)
