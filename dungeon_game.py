import pygame
import sys
from os import path
from settings import *
from sprites import *
from tilemap import *

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

    def load_data(self):
        game_folder = path.dirname(__file__)
        img_folder = path.join(game_folder, 'img')
        self.map = Map(path.join(game_folder, 'map2.txt'))
        self.knight_img = pygame.image.load(path.join(img_folder, KNIGHT_IMG)).convert_alpha()
        self.stone_img = pygame.image.load(path.join(img_folder, STONE_IMG)).convert_alpha()
        self.wizard_img = pygame.image.load(path.join(img_folder, WIZARD_IMG)).convert_alpha()
        self.wall_img = pygame.image.load(path.join(img_folder, WALL_IMG)).convert_alpha()

    def new(self):
        self.all_sprites = pygame.sprite.Group()
        self.walls = pygame.sprite.Group()
        self.wizards = pygame.sprite.Group()
        self.stones = pygame.sprite.Group()
        for row, tiles in enumerate(self.map.data):
            for col, tile in enumerate(tiles):
                # Determines where to build walls.
                if tile == '1':
                    Wall(self, col, row)
                # Determines where to spawn wizards.
                if tile == 'M':
                    Wizard(self, col, row)
                # Determines where to spawn the knight.
                if tile == 'P':
                    self.knight = Knight(self, col, row)
        self.camera = Camera(self.map.width, self.map.height)

    def run(self):
        self.playing = True
        while self.playing:
            self.dt = self.clock.tick(FPS) / 1000
            self.events()
            self.update()
            self.draw()

    def quit(self):
        pygame.quit()
        sys.exit()

    def update(self):
        # Update the game loop.
        self.all_sprites.update()
        self.camera.update(self.knight)
        # Finds collisions between the wizards and the stones.
        hits = pygame.sprite.groupcollide(self.wizards, self.stones, False, True)
        # Deletes a wizard if it has been hit by a stone.
        for hit in hits:
            hit.kill()

# Not called in this version of game, was for earlier when I wanted to see the grid.
    def draw_grid(self):
        for x in range(0, WIDTH, TILESIZE):
            pygame.draw.line(self.screen, LIGHTGREY, (x, 0), (x, HEIGHT))
        for y in range(0, HEIGHT, TILESIZE):
            pygame.draw.line(self.screen, LIGHTGREY, (0, y), (WIDTH, y))

    def draw(self):
        self.screen.fill(BGCOLOR)
        #self.draw_grid()
        for sprite in self.all_sprites:
            self.screen.blit(sprite.image, self.camera.apply(sprite))
        pygame.display.flip()

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.quit()

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