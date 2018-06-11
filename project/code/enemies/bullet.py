import pygame  # Para el sistema

from config import constants as C


class Bullet(pygame.sprite.Sprite):
    def __init__(self, X, Y):
        pygame.sprite.Sprite.__init__(self)
        self.img = pygame.image.load(C.BULLET_IMAGE)
        self.imgRect = self.img.get_rect()
        self.imgRect.x = X * C.TILE_W
        self.imgRect.y = Y * C.TILE_H

    def update(self):
        self.imgRect.x += C.BULLET_MOVE_X