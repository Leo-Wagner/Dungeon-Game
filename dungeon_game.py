import pygame
import sys
from os import path
from settings import *
from sprites import *
from tilemap import *

# A function which displays the amount of health the knight has remaining.
# A rectangle appears in the top left side of the screen and changes color and gets shorter as the knight loses health.
def draw_knight_health(surface, x, y, health_percentage):
    # Makes sure the knight doesn't have negative health.
    if health_percentage < 0:
        health_percentage = 0
    BAR_LENGTH = 100
    BAR_HEIGHT = 20
    # Sets the length of the health bar as a proportion of the knight's health.
    fill = health_percentage * BAR_LENGTH
    # Creates an outline for the health bar.
    outline_rect = pygame.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    # Fills the entire length of the rectangle with color.
    fill_rect = pygame.Rect(x, y, fill, BAR_HEIGHT)
    # Checks the health percentage of the knight and sets the color accordingly.
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
    # Draws the colored part of the health bar.
    pygame.draw.rect(surface, color, fill_rect)
    # Draws the outline of the health bar.
    pygame.draw.rect(surface, WHITE, outline_rect, 2)

class DungeonGame:
    '''A class to manage the game.'''
    def __init__(self):
        pygame.init()
        # Sets the screen dimensions.
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        # Sets caption at top of screen.
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()
        # When a key is held down, there is a .5 s delay before a KEYDOWN event is sent.
        # If the key is still held down after the initial delay, KEYDOWN events are sent every .1 s.
        pygame.key.set_repeat(500, 100)
        self.load_data()

    # A function which displays text onto the screen when the game is paused.
    def draw_text(self, text, font_name, size, color, x, y, align):
        font = pygame.font.Font(font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        if align == 'top':
            text_rect.midbottom = (x, y)
        self.screen.blit(text_surface, text_rect)

    # Load all the maps, images, and sounds needed for the game.
    def load_data(self):
        game_folder = path.dirname(__file__)
        image_folder = path.join(game_folder, 'image')
        map_folder = path.join(game_folder, 'maps')
        music_folder = path.join(game_folder, 'music')
        sound_folder = path.join(game_folder, 'sounds')
        self.font = path.join(image_folder, 'DUNGEON.TTF')
        self.dim_screen = pygame.Surface(self.screen.get_size()).convert_alpha()
        self.dim_screen.fill((0, 0, 0, 120))
        self.map = TiledMap(path.join(map_folder, 'Dungeon_Map.tmx'))
        self.map_image = self.map.make_map()
        self.map_rect = self.map_image.get_rect()
        self.knight_image = pygame.image.load(path.join(image_folder, KNIGHT_IMAGE)).convert_alpha()
        self.knight_image = pygame.transform.scale(self.knight_image, (24, 24))
        self.stone_image = pygame.image.load(path.join(image_folder, STONE_IMAGE)).convert_alpha()
        self.wizard_image = pygame.image.load(path.join(image_folder, WIZARD_IMAGE)).convert_alpha()
        self.wizard_image = pygame.transform.scale(self.wizard_image, (24, 24))
        self.wall_image = pygame.image.load(path.join(image_folder, WALL_IMAGE)).convert_alpha()
        self.cross = pygame.image.load(path.join(image_folder, CROSS)).convert_alpha()
        self.cross = pygame.transform.scale(self.cross, (24, 24))
        self.health = pygame.image.load(path.join(image_folder, HEALTH)).convert_alpha()
        self.health = pygame.transform.scale(self.health, (24, 24))
        pygame.mixer.music.load(path.join(music_folder, MUSIC))
        self.health_sound = {}
        for type in HEALTH_SOUND:
            self.health_sound[type] = pygame.mixer.Sound(path.join(sound_folder, HEALTH_SOUND[type]))
        self.stone_sound = {}
        for type in STONE_SOUND:
            self.stone_sound[type] = pygame.mixer.Sound(path.join(sound_folder, STONE_SOUND[type]))
        self.wizard_hit_sound = {}
        for type in WIZARD_HIT_SOUND:
            self.wizard_hit_sound[type] = pygame.mixer.Sound(path.join(sound_folder, WIZARD_HIT_SOUND[type]))
        self.knight_hit_sound = {}
        for type in KNIGHT_HIT_SOUND:
            self.knight_hit_sound[type] = pygame.mixer.Sound(path.join(sound_folder, KNIGHT_HIT_SOUND[type]))

    def new(self):
        # Was needed to ensure that the knight goes over the health potion when they collide.
        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.walls = pygame.sprite.Group()
        self.wizards = pygame.sprite.Group()
        self.stones = pygame.sprite.Group()
        self.collectibles = pygame.sprite.Group()
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
            # Checks to see if the name of the tile object is health.
            # If so, a health potion spawns at the location of the tile object.
            if tile_object.name in ['health']:
                Collectible(self, tile_object.x, tile_object.y, tile_object.name)
        # Total area that the camera can occupy.
        self.camera = Camera(self.map.width, self.map.height)
        self.paused = False

    def run(self):
        self.playing = True
        # Loops the background music after the song ends.
        pygame.mixer.music.play(loops=-1)
        while self.playing:
            self.time = self.clock.tick(FPS) / 1000
            self.events()
            if not self.paused:
                self.update()
            self.draw()

    # Exits the game window if the player hits the 'X' in the top right of the screen.
    def quit(self):
        pygame.quit()
        sys.exit()

    def update(self):
        # Update the game loop.
        self.all_sprites.update()
        # Updates the camera while tracking the knight.
        self.camera.update(self.knight)

        # Finds collisions between the knight and collectibles.
        hits = pygame.sprite.spritecollide(self.knight, self.collectibles, False)
        for hit in hits:
            if hit.type == 'health' and self.knight.health < KNIGHT_HEALTH:
                # Deletes the health pack from the screen.
                hit.kill()
                # Plays a sound for the knight collecting a health pack.
                self.health_sound['health'].play()
                # Adds a set amount of health to the knight's health.
                self.knight.add_health(HEALTH_PACK)

        # Finds collisions between the knight and wizards.
        hits = pygame.sprite.spritecollide(self.knight, self.wizards, False, collide_hit_rect)
        for hit in hits:
            # Plays a sound for a wizard hitting the knight.
            self.knight_hit_sound['knight'].play()
            # Subtracts 10 health points from the knight's total health each time it is hit by a wizard.
            self.knight.health -= WIZARD_DAMAGE
            # Pauses the movement of a wizard if it hits the knight.
            hit.velocity = vec(0, 0)
            # Checks to see if the knight's health is equal to zero.
            if self.knight.health <= 0:
                # Ends the game if the knight's health is equal to zero.
                self.playing = False
        if hits:
            # Pushes the knight back if it is hit by a wizard.
            self.knight.position += vec(WIZARD_MOVEBACK, 0).rotate(-hits[0].rotation)

        # Finds collisions between the wizards and the stones.
        hits = pygame.sprite.groupcollide(self.wizards, self.stones, False, True)
        for hit in hits:
            # Plays a sound for a stone hitting a wizard.
            self.wizard_hit_sound['wizard'].play()
            # Subtracts 10 health points from a wizard's total health each time it is hit by a stone.
            hit.health -= STONE_DAMAGE
            # Pauses the movement of a wizard if it is hit by a stone.
            hit.velocity = vec(0, 0)


    def draw(self):
        # Draws the map onto the game surface and sets a shifting rectangle for the map.
        self.screen.blit(self.map_image, self.camera.apply_rect(self.map_rect))
        for sprite in self.all_sprites:
            if isinstance(sprite, Wizard):
                sprite.draw_health()
            self.screen.blit(sprite.image, self.camera.apply(sprite))
        # Calls the function which draws the knight health onto the screen.
        draw_knight_health(self.screen, 10, 10, self.knight.health / KNIGHT_HEALTH)
        # Checks to see if the game is paused.
        if self.paused:
            # Places a grey tint on the screen so that it looks dim.
            self.screen.blit(self.dim_screen, (0, 0))
            # Writes 'PAUSED' in Dungeon font on the screen.
            self.draw_text('PAUSED', self.font, 105, WHITE, WIDTH / 2, HEIGHT /2, align = 'top')
        pygame.display.flip()

    def events(self):
        for event in pygame.event.get():
            # Exits the game if the player clicks on the 'X'
            if event.type == pygame.QUIT:
                self.quit()
                # Exits the fame if the player presses the 'esc' key.
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.quit()
            # Pauses the game if the mouse is clicked.
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.paused = not self.paused

    # Creates a black screen with white text when the knight dies.
    def game_over_screen(self):
        # Fills the screen with black.
        self.screen.fill(BLACK)
        # Writes 'GAME OVER' in dungeon font on the screen.
        self.draw_text("GAME OVER", self.font, 100, WHITE,
                       WIDTH / 2, HEIGHT / 2, align='top')
        # Writes 'CLICK MOUSE TO RESTART' in dungeon font on the screen.
        self.draw_text("CLICK MOUSE TO RESTART", self.font, 60, WHITE,
                       WIDTH / 2, HEIGHT * 3 / 4, align='top')
        pygame.display.flip()
        self.game_over_key()

    def game_over_key(self):
        # The game waits to see if either the 'X' or the mouse is clicked.
        pygame.event.wait()
        waiting = True
        while waiting:
            self.clock.tick(FPS)
            for event in pygame.event.get():
                # Closes the screen if the player clicks 'X'
                if event.type == pygame.QUIT:
                    waiting = False
                    self.quit()
                # Restarts the game if the player clicks on the screen with the mouse.
                if event.type == pygame.MOUSEBUTTONDOWN:
                    waiting = False

dungeon_game = DungeonGame()

# A loop to run the game.
while True:
    dungeon_game.new()
    dungeon_game.run()
    dungeon_game.game_over_screen()