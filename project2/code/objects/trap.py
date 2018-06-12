import pygame  # Para el sistema
from objects.object import Object

from config import constants as C


class Trap(Object):
    def __init__(self, X, Y, OBJECTS_FLYWEIGHT):
        super()
        self.objectsFlyweight = OBJECTS_FLYWEIGHT
        self.img = pygame.image.load(C.OBJECT_TRAP_PATH)
        self.imgRect = self.img.get_rect()
        self.imgRect.x = X * C.TILE_W
        self.imgRect.y = Y * C.TILE_H

        self.flyweight = self.objectsFlyweight.getFlyweight('trap')
        #print(self.flyweight)
        self.scoreAdd = self.flyweight.score
