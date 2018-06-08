import pygame  # Para el sistema
from project.code.objects.object import Object

from project.code.config import constants as C


class Gold(Object):
    def __init__(self, X, Y, SCORE):
        super()
        self.img = pygame.image.load(C.OBJECT_GOLD_PATH)
        self.imgRect = self.img.get_rect()
        self.imgRect.x = X * C.TILE_W
        self.imgRect.y = Y * C.TILE_H
        self.scoreAdd = SCORE
