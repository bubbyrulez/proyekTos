import pygame as pg
import os
import pygame
import random
from os import path
vec = pg.math.Vector2
import inputbox

game_title = "Lompat sek nou!"


#colors
WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
YELLOW = (255,255,0)
LIGHTBLUE = (135,206,250)
BGCOLOR = LIGHTBLUE

#player properties
PLAYER_ACCL = 0.5
PLAYER_FRICTION = -0.1
PLAYER_GRAV = 0.5
PLAYER_JUMP = 16

#settings
WIDTH = 480
HEIGHT = 600
FPS = 60
FONT_NAME = 'arial'
TOKEN = []

#game properties
BOOST_POWER = 60
BOOSS_SPAWN_PCT = 8

#platform list
PLATFORM_LIST = [(0,HEIGHT-40),
                 (WIDTH/2-50,HEIGHT*3/4-50),
                 (125,HEIGHT-350),
                 (350,200),
                 (175,100)]

#assets
GAME_FOLDER = path.dirname(__file__)
ASSETS_FOLDER = path.join(GAME_FOLDER,"assets")
SPRITESHEET_FOLDER = path.join(ASSETS_FOLDER,"Sprites")
SPRITESHEET_FILE_1 = path.join(SPRITESHEET_FOLDER,"spritesheet_jumper.png")
SPRITESHEET_FILE_2 = path.join(SPRITESHEET_FOLDER,"p2_spritesheet.png")
SOUND_FOLDER = path.join(ASSETS_FOLDER,"Sounds")
BGM_1 = path.join(SOUND_FOLDER,"happy_adveture.ogg")
BGM_2 = path.join(SOUND_FOLDER,"DayAndNight.ogg")
BGM_3 = path.join(SOUND_FOLDER,"Explorer.ogg")
JUMP_SOUND_1 = path.join(SOUND_FOLDER,"Jump.wav")
PUP_SOUND_1 = path.join(SOUND_FOLDER,"Powerup.wav")
SCORE_FILE = path.join(ASSETS_FOLDER,"highscore.txt")
