import pygame  # Para el sistema

from characters.components import *
from config import constants as C



class GameObject():
    def __init__(self):
        self.sprite = Sprite()
        self.stats = Stats()
        self.phisics = Phisics(self.sprite.imgRect.x,self.sprite.imgRect.y)
        self.anim = Animator()
        self.anim.startAnimation(self.sprite.framesIdle)

   

    # Metodo update del heroe
    def update(self, mapa):
        self.phisics.update(self.sprite,mapa)
        self.stats.update(self.phisics)
        self.anim.update(self.stats,self.sprite)


class mapObject():
    def __init__(self):
        self.mapa = Mapa()