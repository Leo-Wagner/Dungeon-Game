import pygame
from random import choice
from settings import *
from tilemap import collide_hit_rect
vec = pygame.math.Vector2

# A function to determine if a knight or wizard hits a wall.
def collide_with_walls(sprite, group, direction):
    if direction == 'x':
        hits = pygame.sprite.spritecollide(sprite, group, False, collide_hit_rect)
        if hits:
            # Places the sprite at the left edge of whatever it hit.
            if hits[0].rect.centerx > sprite.hit_rect.centerx:
                sprite.position.x = hits[0].rect.left - sprite.hit_rect.width / 2
            # Places the sprite at the right edge of whatever it hit.
            if hits[0].rect.centerx < sprite.hit_rect.centerx:
                sprite.position.x = hits[0].rect.right + sprite.hit_rect.width / 2
            # Stops the x-velocity from increasing while the sprite is hitting a wall.
            sprite.velocity.x = 0
            sprite.hit_rect.centerx = sprite.position.x
    if direction == 'y':
        hits = pygame.sprite.spritecollide(sprite, group, False, collide_hit_rect)
        if hits:
            # Places the sprite at the top edge of whatever it hit.
            if hits[0].rect.centery > sprite.hit_rect.centery:
                sprite.position.y = hits[0].rect.top - sprite.hit_rect.height / 2
            # Places the sprite at the bottom edge of whatever it hit.
            if hits[0].rect.centery < sprite.hit_rect.centery:
                sprite.position.y = hits[0].rect.bottom + sprite.hit_rect.height / 2
            # Stops the y-velocity from increasing while the sprite is hitting a wall.
            sprite.velocity.y = 0
            sprite.hit_rect.centery = sprite.position.y

class Knight(pygame.sprite.Sprite):
    '''A class to manage the knight'''
    def __init__(self, game, x, y):
        # Sets the layer of the knight so that it goes above other layers (specifically for the health potion collectible).
        self._layer = KNIGHT_LAYER
        self.groups = game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.knight_image
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.hit_rect = KNIGHT_HIT_RECT
        self.hit_rect.center = self.rect.center
        # 2-dimensional velocity of the knight.
        self.velocity = vec(0, 0)
        # 2-dimensional position of the knight.
        self.position = vec(x, y)
        # Sets the knight's initial rotation at 0.
        self.rotation = 0
        self.last_shot = 0
        self.health = KNIGHT_HEALTH

# A function to determine how the knight should respond if certain keys are pressed.
    def get_keys(self):
        # Knight is not rotating if keys are not pressed down.
        self.rotation_speed = 0
        # Knight is not moving if keys are not pressed down.
        self.velocity = vec(0, 0)
        keys = pygame.key.get_pressed()
        # Rotates the knight left at a set speed if left arrow key is pressed.
        if keys[pygame.K_LEFT]:
            self.rotation_speed = KNIGHT_ROTATION_SPEED
        # Rotates the knight right at a set speed if right arrow key is pressed.
        if keys[pygame.K_RIGHT]:
            self.rotation_speed = -KNIGHT_ROTATION_SPEED
        # Knight moves forward at the knight speed in the direction it is facing.
        if keys[pygame.K_UP]:
            self.velocity = vec(KNIGHT_SPEED, 0).rotate(-self.rotation)
        # Knight moves backward at the knight speed in the direction it is facing.
        if keys[pygame.K_DOWN]:
            self.velocity = vec(-KNIGHT_SPEED / 2, 0).rotate(-self.rotation)
        # The knight throws a stone if the space bar is pressed.
        if keys[pygame.K_SPACE]:
            now = pygame.time.get_ticks()
            # Allows for a stone to be thrown every .1 s (STONE_RATE)
            if now - self.last_shot > STONE_RATE:
                self.last_shot = now
                direction = vec(1, 0).rotate(-self.rotation)
                Stone(self.game, self.position, direction)
                # Plays a specific sound effect each time the space bar is pressed.
                self.game.stone_sound['stone'].play()

    def update(self):
        self.get_keys()
        # Updates the rotation with the knight's current rotation (% 360 to keep the angle between 1 and 360).
        self.rotation = (self.rotation + self.rotation_speed * self.game.time % 360)
        # Rotates the knight image to match the rotation input by the arrow keys.
        self.image = pygame.transform.rotate(self.game.knight_image, self.rotation)
        self.rect = self.image.get_rect()
        self.rect.center = self.position
        # Determines the knight's position by measuring how long it has travelled in a distance at a set speed.
        self.position += self.velocity * self.game.time
        self.hit_rect.centerx = self.position.x
        collide_with_walls(self, self.game.walls, 'x')
        self.hit_rect.centery = self.position.y
        collide_with_walls(self, self.game.walls, 'y')
        self.rect.center = self.hit_rect.center

    def add_health(self, amount):
        self.health += amount
        # Ensures that health cannot exceed a maximum amount specified in the Settings file.
        if self.health > KNIGHT_HEALTH:
            self.health = KNIGHT_HEALTH

class Wizard(pygame.sprite.Sprite):
    '''A class to manage wizards'''
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.wizards
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.wizard_image
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.hit_rect = WIZARD_HIT_RECT.copy()
        self.hit_rect.center = self.rect.center
        # 2-dimensional position of wizards.
        self.position = vec(x, y)
        # 2-dimensional velocity of wizards.
        self.velocity = vec(1, 1)
        # 2-dimensional acceleration of wizards.
        # Ensures that the wizard does not immediately change direction if the knight passes by it.
        self.acceleration = vec(0, 0)
        self.rect.center = self.position
        self.rotation = 0
        # Sets the health of the wizard to 100
        self.health = WIZARD_HEALTH
        # Sets different speeds for different wizards.
        self.speed = choice(WIZARD_SPEED)

    # A function that stops the wizards from clumping together into one image.
    # They always began to overlap with each other once they had been chasing the knight for 15 or 20 seconds.
    def avoid_wizards(self):
        for wizard in self.game.wizards:
            if wizard != self:
                dist = self.position - wizard.position
                if 0 < dist.length() < AVOID_RADIUS:
                    self.acceleration += dist.normalize()

    def update(self):
        # Points the wizard in the direction of the knight.
        self.rotation = (self.game.knight.position - self.position).angle_to(vec(1, 0))
        # Rotates a wizard the image by rotation
        self.image = pygame.transform.rotate(self.game.wizard_image, self.rotation)
        self.rect = self.image.get_rect()
        self.rect.center = self.position
        self.acceleration = vec(1, 0).rotate(-self.rotation)
        self.avoid_wizards()
        # Does not change direction of the vector, only alters magnitude.
        self.acceleration.scale_to_length(self.speed)
        self.acceleration += self.velocity * -1
        self.velocity += self.acceleration * self.game.time
        self.position += self.velocity * self.game.time + .5 * self.acceleration * self.game.time ** 2
        self.hit_rect.centerx = self.position.x
        collide_with_walls(self, self.game.walls, 'x')
        self.hit_rect.centery = self.position.y
        collide_with_walls(self, self.game.walls, 'y')
        self.rect.center = self.hit_rect.center
        # Checks to see if a wizard's health is 0.
        if self.health <= 0:
            # Deletes a wizard.
            self.kill()
            # Draws a cross where the wizard died.
            self.game.map_image.blit(self.game.cross, self.position - vec(12, 12))

    def draw_health(self):
    # Checks to see the amount of health the wizard has remaining,
    # and sets the health bar of the wizard to a corresponding color.
        if self.health > 90:
            color = HEALTH_100
        elif self.health > 80:
            color = HEALTH_90
        elif self.health > 70:
            color = HEALTH_80
        elif self.health > 60:
            color = HEALTH_70
        elif self.health > 50:
            color = HEALTH_60
        elif self.health > 40:
            color = HEALTH_50
        elif self.health > 30:
            color = HEALTH_40
        elif self.health > 20:
            color = HEALTH_30
        elif self.health > 10:
            color = HEALTH_20
        elif self.health >= 0:
            color = HEALTH_10
        # Creates a rectangle to display the wizard health.
        width = int(self.rect.width * self.health / WIZARD_HEALTH)
        self.health_bar = pygame.Rect(0, 0, width, 4)
        if self.health < WIZARD_HEALTH:
            pygame.draw.rect(self.image, color, self.health_bar)

class Stone(pygame.sprite.Sprite):
    '''A class to manage stones which the knight throws.'''
    def __init__(self, game, position, direction):
        self.groups = game.all_sprites, game.stones
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.stone_image
        self.rect = self.image.get_rect()
        self.hit_rect = self.rect
        # Sets the position of the stone as the position of the knight.
        self.position = vec(position)
        self.rect.center = position
        # Projects the stone in the direction which the knight is facing with a set speed.
        self.velocity = direction * STONE_SPEED
        # Measures how long it has been since the stone has been thrown.
        self.spawn_time = pygame.time.get_ticks()

    def update(self):
        # Sets the position of the stone by seeing how long it has travelled in a distance at a set speed.
        self.position += self.velocity * self.game.time
        self.rect.center = self.position
        # Deletes stones if the stone hits a wall.
        if pygame.sprite.spritecollideany(self, self.game.walls):
            self.kill()
        # Deletes stones if the stone has existed for longer than 2 seconds.
        if pygame.time.get_ticks() - self.spawn_time > STONE_TIME:
            self.kill()

class Obstacle(pygame.sprite.Sprite):
    '''A class to manage walls.'''
    def __init__(self, game, x, y, width, height):
        self.groups = game.walls
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.rect = pygame.Rect(x, y, width, height)
        self.x = x
        self.y = y
        self.rect.x = x
        self.rect.y = y

        # The obstacle class does not require an update function because none of the walls move or change appearance.

class Collectible(pygame.sprite.Sprite):
    def __init__(self, game, x, y, type):
        # Sets the layer of collectibles to under the layer of the knight.
        self._collectible = COLLECTIBLES_LAYER
        self.groups = game.all_sprites, game.collectibles
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.image = game.health
        self.rect = self.image.get_rect()
        self.type = type
        self.rect.center = (x, y)
        # Creates a 2-dimensional vector for any collectibles' position.
        self.position = vec(x,y)