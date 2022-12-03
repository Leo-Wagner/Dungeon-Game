import pygame

# Color settings
BROWN = (54, 35, 18)
WHITE = (255, 255, 255)
HEALTH_100 = (0, 255, 0)
HEALTH_90 = (102, 255, 102)
HEALTH_80 = (178, 255, 102)
HEALTH_70 = (204, 255, 153)
HEALTH_60 = (229, 255, 204)
HEALTH_50 = (255, 255, 204)
HEALTH_40 = (255, 255, 102)
HEALTH_30 = (255, 153, 153)
HEALTH_20 = (255, 102, 102)
HEALTH_10 = (255, 0, 0)
BLACK = (0, 0, 0)

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
WALL_IMAGE = 'tile_0058.png'

# Knight Settings
KNIGHT_HEALTH = 100
KNIGHT_SPEED = 250
KNIGHT_ROTATION_SPEED = 200
KNIGHT_IMAGE = 'tile_0096.png'
KNIGHT_HIT_RECT = pygame.Rect(0, 0, 24, 24)

# Stone Settings
STONE_IMAGE = 'tile_0101.png'
STONE_SPEED = 400
STONE_TIME = 2000
STONE_RATE = 100
STONE_DAMAGE = 10

# Wizard settings
WIZARD_IMAGE = 'tile_0111.png'
WIZARD_SPEED = [80, 90, 100, 110, 120]
WIZARD_HIT_RECT = pygame.Rect(0, 0, 24, 24)
WIZARD_HEALTH = 100
WIZARD_DAMAGE = 10
WIZARD_MOVEBACK = 20
AVOID_RADIUS = 50
CROSS = 'tile_0064.png'

# Collectibles settings
HEALTH = 'tile_0114.png'
HEALTH_PACK = 20

# Layer settings
KNIGHT_LAYER = 2
COLLECTIBLES_LAYER = 1

# Sounds settings
MUSIC = 'music.mp3'
KNIGHT_HIT_SOUND = {'knight': 'knight.mp3'}
WIZARD_HIT_SOUND = {'wizard': 'wizard.mp3'}
STONE_SOUND = {'stone': 'stone.mp3'}
HEALTH_SOUND = {'health': 'health.mp3'}