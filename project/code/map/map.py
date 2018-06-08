import numpy  # Para el sistema
import pygame

from project.code.config import constants as C


# Creamos el mapa
class Mapa:
    def __init__(self):
        self.mapa = numpy.loadtxt(C.MAP1_PATH, dtype=int, delimiter=',')  # Cargamos el mapa desde el archivo txt
        # Cargamos las imagenes
        self.img = [pygame.image.load(C.TILE_FLOOR1_PATH), pygame.image.load(C.TILE_WALL_PATH),
                    pygame.image.load(C.TILE_FLOOR2_PATH), pygame.image.load(C.TILE_FLOOR3_PATH), ]
        self.imgRect = [self.img[0].get_rect(), self.img[1].get_rect(), self.img[2].get_rect(), self.img[3].get_rect()]

    def testColision(self, X, Y, XX, YY):  # Para testear si colisiona el jugador con alguna casilla tipo pared
        X = int(X / C.TILE_W)
        Y = int(Y / C.TILE_H)
        XX = int(XX / C.TILE_W)
        YY = int(YY / C.TILE_H)
        if self.mapa[Y][X] == C.TILE_WALL:
            return False
        elif self.mapa[YY][XX] == C.TILE_WALL:
            return False
        elif self.mapa[YY][X] == C.TILE_WALL:
            return False
        elif self.mapa[Y][XX] == C.TILE_WALL:
            return False
        return True
