import pygame  # Para el sistema

from config import constants as C


# Creamos un animador para efectos de animacion
class Animator:
    def __init__(self, object):
        self.animationTick = pygame.time.get_ticks()
        self.currentFrame = 0
        self.status = C.HERO_IDLE
        self.object = object

    def startAnimation(self, sequence, reset=False):
        if reset == True:
            self.currentFrame = 0
        self.sequence = sequence

    def update(self):
        self.object.img = self.sequence[self.currentFrame]
        if self.animationTick + C.ANIMATION_TICKRATE < pygame.time.get_ticks():
            self.currentFrame += 1
            self.animationTick = pygame.time.get_ticks()
        if self.currentFrame >= len(self.sequence) - 1:
            self.currentFrame = 0
