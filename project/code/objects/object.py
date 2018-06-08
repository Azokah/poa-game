import pygame  # Para el sistema

from config import constants as C


class Object(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.img = pygame.image.load(C.OBJECT_GOLD_PATH)
        self.imgRect = self.img.get_rect()
        self.imgRect.x = 1 * C.TILE_W
        self.imgRect.y = 0 * C.TILE_H
        self.scoreAdd = 0
