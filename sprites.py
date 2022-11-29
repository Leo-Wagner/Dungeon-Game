import pygame
from settings import *
from tilemap import collide_hit_rect
vec = pygame.math.Vector2

# A function to determine if a knight or wizard hits a wall.
def collide_with_walls(sprite, group, dir):
    if dir == 'x':
        hits = pygame.sprite.spritecollide(sprite, group, False, collide_hit_rect)
        if hits:
            if sprite.vel.x > 0:
                sprite.pos.x = hits[0].rect.left - sprite.hit_rect.width / 2
            if sprite.vel.x < 0:
                sprite.pos.x = hits[0].rect.right + sprite.hit_rect.width / 2
            sprite.vel.x = 0
            sprite.hit_rect.centerx = sprite.pos.x
    if dir == 'y':
        hits = pygame.sprite.spritecollide(sprite, group, False, collide_hit_rect)
        if hits:
            if sprite.vel.y > 0:
                sprite.pos.y = hits[0].rect.top - sprite.hit_rect.height / 2
            if sprite.vel.y < 0:
                sprite.pos.y = hits[0].rect.bottom + sprite.hit_rect.height / 2
            sprite.vel.y = 0
            sprite.hit_rect.centery = sprite.pos.y

class Knight(pygame.sprite.Sprite):
    '''A class to manage the knight'''
    def __init__(self, game, x, y):
        self.groups = game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.knight_img
        self.rect = self.image.get_rect()
        self.hit_rect = KNIGHT_HIT_RECT
        self.hit_rect.center = self.rect.center
        self.vel = vec(0, 0)
        self.pos = vec(x, y) * TILESIZE
        self.rot = 0
        self.last_shot = 0

# A function to determine how the knight should respond if certain keys are pressed.
    def get_keys(self):
        self.rot_speed = 0
        self.vel = vec(0, 0)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rot_speed = KNIGHT_ROT_SPEED
        if keys[pygame.K_RIGHT]:
            self.rot_speed = -KNIGHT_ROT_SPEED
        if keys[pygame.K_UP]:
            self.vel = vec(KNIGHT_SPEED, 0).rotate(-self.rot)
        if keys[pygame.K_DOWN]:
            self.vel = vec(-KNIGHT_SPEED / 2, 0).rotate(-self.rot)
        if keys[pygame.K_SPACE]:
            now = pygame.time.get_ticks()
            if now - self.last_shot > STONE_RATE:
                self.last_shot = now
                dir = vec(1, 0).rotate(-self.rot)
                Stone(self.game, self.pos, dir)

    def update(self):
        self.get_keys()
        self.rot = (self.rot + self.rot_speed * self.game.dt % 360)
        self.image = pygame.transform.rotate(self.game.knight_img, self.rot)
        self.rect = self.image.get_rect()
        self.rect.center = self.pos
        self.pos += self.vel * self.game.dt
        self.hit_rect.centerx = self.pos.x
        collide_with_walls(self, self.game.walls, 'x')
        self.hit_rect.centery = self.pos.y
        collide_with_walls(self, self.game.walls, 'y')
        self.rect.center = self.hit_rect.center

class Wizard(pygame.sprite.Sprite):
    '''A class to manage wizards'''
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.wizards
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.wizard_img
        self.rect = self.image.get_rect()
        self.hit_rect = WIZARD_HIT_RECT.copy()
        self.hit_rect.center = self.rect.center
        self.pos = vec(x, y) * TILESIZE
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        self.rect.center = self.pos
        self.rot = 0

    def update(self):
        self.rot = (self.game.knight.pos - self.pos).angle_to(vec(1, 0))
        self.image = pygame.transform.rotate(self.game.wizard_img, self.rot)
        self.rect = self.image.get_rect()
        self.rect.center = self.pos
        self.acc = vec(WIZARD_SPEED, 0).rotate(-self.rot)
        self.acc += self.vel * -1
        self.vel += self.acc * self.game.dt
        self.pos += self.vel * self.game.dt + .5 * self.acc * self.game.dt ** 2
        self.hit_rect.centerx = self.pos.x
        collide_with_walls(self, self.game.walls, 'x')
        self.hit_rect.centery = self.pos.y
        collide_with_walls(self, self.game.walls, 'y')
        self.rect.center = self.hit_rect.center

class Stone(pygame.sprite.Sprite):
    '''A class to manage stones'''
    def __init__(self, game, pos, dir):
        self.groups = game.all_sprites, game.stones
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.stone_img
        self.rect = self.image.get_rect()
        self.pos = vec(pos)
        self.rect.center = pos
        self.vel = dir * STONE_SPEED
        self.spawn_time = pygame.time.get_ticks()

    def update(self):
        self.pos += self.vel * self.game.dt
        self.rect.center = self.pos
        # Deletes stones if the stone hits a wall.
        if pygame.sprite.spritecollideany(self, self.game.walls):
            self.kill()
        # Deletes stones if the stone has existed for longer than 2 seconds.
        if pygame.time.get_ticks() - self.spawn_time > STONE_TIME:
            self.kill()

class Wall(pygame.sprite.Sprite):
    '''A class to manage walls.'''
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.walls
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.wall_img
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE

    # Does not require an 'update' as wall does not move.