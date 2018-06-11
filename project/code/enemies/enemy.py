import pygame  # Para el sistema

from config import constants as C


class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.img = pygame.image.load(C.ENEMY_1_IMAGE)
        self.imgRect = self.img.get_rect()
        self.imgRect.x = 1 * C.TILE_W
        self.imgRect.y = 0 * C.TILE_H
        self.scoreAdd = 0

    def update(self):
        pass
