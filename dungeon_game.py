import pygame
import sys
from os import path
from settings import *
from sprites import *
from tilemap import *

def draw_knight_health(surface, x, y, health_percentage):
    if health_percentage < 0:
        health_percentage = 0
    BAR_LENGTH = 100
    BAR_HEIGHT = 20
    fill = health_percentage * BAR_LENGTH
    outline_rect = pygame.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pygame.Rect(x, y, fill, BAR_HEIGHT)
    if health_percentage > .90:
        color = HEALTH_100
    elif health_percentage > .80:
        color = HEALTH_90
    elif health_percentage > .70:
        color = HEALTH_80
    elif health_percentage > .60:
        color = HEALTH_70
    elif health_percentage > .50:
        color = HEALTH_60
    elif health_percentage > .40:
        color = HEALTH_50
    elif health_percentage > .30:
        color = HEALTH_40
    elif health_percentage > .20:
        color = HEALTH_30
    elif health_percentage > .10:
        color = HEALTH_20
    elif health_percentage >= 0:
        color = HEALTH_10
    pygame.draw.rect(surface, color, fill_rect)
    pygame.draw.rect(surface, WHITE, outline_rect, 2)

class DungeonGame:
    '''A class to manage the game.'''
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()
        # When a key is held down, there is a .5 s delay before a KEYDOWN event is sent.
        # If the key is still held down after the initial delay, KEYDOWN events are sent every .1 s.
        pygame.key.set_repeat(500, 100)
        self.load_data()

    # Load all the maps and images needed for the game.
    def load_data(self):
        game_folder = path.dirname(__file__)
        image_folder = path.join(game_folder, 'image')
        map_folder = path.join(game_folder, 'maps')
        self.map = TiledMap(path.join(map_folder, 'Dungeon_Map.tmx'))
        self.map_image = self.map.make_map()
        self.map_rect = self.map_image.get_rect()
        self.knight_image = pygame.image.load(path.join(image_folder, KNIGHT_IMAGE)).convert_alpha()
        self.stone_image = pygame.image.load(path.join(image_folder, STONE_IMAGE)).convert_alpha()
        self.wizard_image = pygame.image.load(path.join(image_folder, WIZARD_IMAGE)).convert_alpha()
        self.wall_image = pygame.image.load(path.join(image_folder, WALL_IMAGE)).convert_alpha()

    def new(self):
        self.all_sprites = pygame.sprite.Group()
        self.walls = pygame.sprite.Group()
        self.wizards = pygame.sprite.Group()
        self.stones = pygame.sprite.Group()
        #for row, tiles in enumerate(self.map.data):
            #for col, tile in enumerate(tiles):
                # Determines where to build walls.
                #if tile == '1':
                    #Wall(self, col, row)
                # Determines where to spawn wizards.
                #if tile == 'M':
                    #Wizard(self, col, row)
                # Determines where to spawn the knight.
                #if tile == 'P':
                    #self.knight = Knight(self, col, row)
        for tile_object in self.map.tmxdata.objects:
            # Checks to see if name of the tile object is knight.
            # If so, the knight spawns at the location of the tile object.
            if tile_object.name == 'knight':
                self.knight = Knight(self, tile_object.x, tile_object.y)
            # Checks to see if the name of the tile object is wall.
            # If so, an obstacle spawns at the location of the tile object.
            if tile_object.name == 'wall':
                Obstacle(self, tile_object.x, tile_object.y, tile_object.width, tile_object.height)
            # Checks to see if the name of the tile object is wizard.
            # If so, a wizard spawns at the location of the tile object.
            if tile_object.name == 'wizard':
                Wizard(self, tile_object.x, tile_object.y)
        self.camera = Camera(self.map.width, self.map.height)
        self.draw_debug = False

    def run(self):
        self.playing = True
        while self.playing:
            self.dt = self.clock.tick(FPS) / 1000
            self.events()
            self.update()
            self.draw()

    # Exits the game window if the player hits the 'X' in the top right of the screen.
    def quit(self):
        pygame.quit()
        sys.exit()

    def update(self):
        # Update the game loop.
        self.all_sprites.update()
        self.camera.update(self.knight)

        # Finds collisions between the knight and wizards.
        hits = pygame.sprite.spritecollide(self.knight, self.wizards, False, collide_hit_rect)
        for hit in hits:
            # Subtracts 10 health points from the knight's total health each time it is hit by a wizard.
            self.knight.health -= WIZARD_DAMAGE
            # Pauses the movement of a wizard if it hits the knight.
            hit.vel = vec(0, 0)
            # Checks to see if the knight's health is equal to zero.
            if self.knight.health <= 0:
                # Ends the game if the knight's health is equal to zero.
                self.playing = False
        if hits:
            # Pushes the knight back if it is hit by a wizard.
            self.knight.pos += vec(WIZARD_MOVEBACK, 0).rotate(-hits[0].rot)

        # Finds collisions between the wizards and the stones.
        hits = pygame.sprite.groupcollide(self.wizards, self.stones, False, True)
        for hit in hits:
            # Subtracts 10 health points from a wizard's total health each time it is hit by a stone.
            hit.health -= STONE_DAMAGE
            # Pauses the movement of a wizard if it is hit by a stone.
            hit.vel = vec(0, 0)


# Not called in this version of game, was for earlier when I wanted to see the grid.
    def draw_grid(self):
        for x in range(0, WIDTH, TILESIZE):
            pygame.draw.line(self.screen, LIGHTGREY, (x, 0), (x, HEIGHT))
        for y in range(0, HEIGHT, TILESIZE):
            pygame.draw.line(self.screen, LIGHTGREY, (0, y), (WIDTH, y))

    def draw(self):
        #self.screen.fill(BGCOLOR)
        self.screen.blit(self.map_image, self.camera.apply_rect(self.map_rect))
        #self.draw_grid()
        for sprite in self.all_sprites:
            if isinstance(sprite, Wizard):
                sprite.draw_health()
            self.screen.blit(sprite.image, self.camera.apply(sprite))
            if self.draw_debug:
                pygame.draw.rect(self.screen, WHITE, self.camera.apply_rect(sprite.hit_rect), 1)
            if self.draw_debug:
                for wall in self.walls:
                    pygame.draw.rect(self.screen, WHITE, self.camera.apply_rect(wall.rect), 1)
        draw_knight_health(self.screen, 10, 10, self.knight.health / KNIGHT_HEALTH)
        pygame.display.flip()

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.quit()
                if event.key == pygame.K_z:
                    self.draw_debug = not self.draw_debug

    #def show_start_screen(self):
        #pass

    #def show_go_screen(self):
        #pass

dg = DungeonGame()
#dg.show_start_screen()
# Create a loop to run the game.
while True:
    dg.new()
    dg.run()
    #dg.show_go_screen()