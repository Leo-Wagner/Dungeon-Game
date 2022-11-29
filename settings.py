import pygame

# Color settings
BROWN = (54, 35, 18)

# Screen settings
WIDTH = 960
HEIGHT = 640
FPS = 60
TITLE = "Dungeon Game"
BGCOLOR = BROWN

# Grid settings
TILESIZE = 16
GRIDWIDTH = WIDTH / TILESIZE
GRIDHEIGHT = HEIGHT / TILESIZE

# Wall settings
WALL_IMG = 'tile_0058.png'

# Knight Settings
KNIGHT_SPEED = 150
KNIGHT_ROT_SPEED = 420
KNIGHT_IMG = 'tile_0096.png'
KNIGHT_HIT_RECT = pygame.Rect(0, 0, 16, 16)

# Stone Settings
STONE_IMG = 'tile_0101.png'
STONE_SPEED = 300
STONE_TIME = 2000
STONE_RATE = 100

# Wizard settings
WIZARD_IMG = 'tile_0111.png'
WIZARD_SPEED = 100
WIZARD_HIT_RECT = pygame.Rect(0, 0, 16, 16)
