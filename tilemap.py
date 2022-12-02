import pygame
import pytmx
from settings import *

# Check for
def collide_hit_rect(one, two):
    return one.hit_rect.colliderect(two.rect)

class TiledMap:
    '''A class to manage my Tiled dungeon map.'''
    def __init__(self, filename):
        tiled_map = pytmx.load_pygame(filename, pixelalpha=True)
        self.width = tiled_map.width * tiled_map.tilewidth
        self.height = tiled_map.height * tiled_map.tileheight
        self.tmxdata = tiled_map

    # Draws the four layers of my Tiled map onto the surface of my game.
    def render(self, surface):
        tile_image = self.tmxdata.get_tile_image_by_gid
        for layer in self.tmxdata.visible_layers:
            if isinstance(layer, pytmx.TiledTileLayer):
                for x, y, gid, in layer:
                    tile = tile_image(gid)
                    if tile:
                        surface.blit(tile, (x * self.tmxdata.tilewidth, y * self.tmxdata.tileheight))

    def make_map(self):
        temporary_surface = pygame.Surface((self.width, self.height))
        self.render(temporary_surface)
        return temporary_surface

class Camera:
    '''A class to shift the screen of view as the knight moves.'''
    def __init__(self, width, height):
        self.camera = pygame.Rect(0, 0, width, height)
        self.width = width
        self.height = height

    # Applies the camera offset to a sprite
    def apply(self, entity):
        return entity.rect.move(self.camera.topleft)

    # Applies the camera offset to a rectangle.
    def apply_rect(self, rect):
        return rect.move(self.camera.topleft)

    def update(self, target):
        x = -target.rect.centerx + int(WIDTH / 2)
        y = -target.rect.centery + int(HEIGHT/ 2)

        # Restricts the camera shift to the size of the map (960 * 640 tiles)
        x = min(0, x)
        y = min(0, y)
        x = max(-(self.width - WIDTH), x)
        y = max(-(self.height - HEIGHT), y)

        self.camera = pygame.Rect(x, y, self.width, self.height)