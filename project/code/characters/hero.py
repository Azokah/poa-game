import pygame  # Para el sistema

from project.code.characters.animator import Animator
from project.code.config import constants as C


# Creamos al heroe
class Heroe(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.cargarFramesAnimacion()
        self.imgRect = self.img.get_rect()
        self.imgRect.x = 1 * C.TILE_W
        self.imgRect.y = 0 * C.TILE_H
        self.hp = C.HERO_HP_MAX
        self.speed = C.HERO_SPEED
        self.status = C.HERO_IDLE
        self.gotoX = self.imgRect.x
        self.gotoY = self.imgRect.y
        self.movingDown = self.movingUp = self.movingRight = self.movingLeft = False
        self.anim = Animator(self)
        self.anim.startAnimation(self.framesIdle)

    def cargarFramesAnimacion(self):
        self.img = pygame.image.load(C.HERO_SURFACE_RUNNING_PATH)
        self.framesCorriendo = []
        for w in range(0, C.HERO_RUNNING_FRAMES):
            self.framesCorriendo.append(self.img.subsurface((C.HERO_SIZE_W * w, 0, C.HERO_SIZE_W, C.HERO_SIZE_H)))
        self.img = pygame.image.load(C.HERO_SURFACE_IDLE_PATH)
        self.framesIdle = []
        for w in range(0, C.HERO_IDLE_FRAMES):
            self.framesIdle.append(self.img.subsurface((C.HERO_SIZE_W * w, 0, C.HERO_SIZE_W, C.HERO_SIZE_H)))
        self.img = pygame.image.load(C.HERO_SURFACE_HURT_PATH)
        self.framesHurt = []
        for w in range(0, C.HERO_HURT_FRAMES):
            self.framesHurt.append(self.img.subsurface((C.HERO_SIZE_W * w, 0, C.HERO_SIZE_W, C.HERO_SIZE_H)))
        self.img = self.framesIdle[0]

    def walkUp(self):
        self.movingUp = True

    def walkDown(self):
        self.movingDown = True

    def walkLeft(self):
        self.movingLeft = True

    def walkRight(self):
        self.movingRight = True

    def stopUp(self):
        self.movingUp = False

    def stopDown(self):
        self.movingDown = False

    def stopLeft(self):
        self.movingLeft = False

    def stopRight(self):
        self.movingRight = False

    # Metodo update del heroe
    def update(self, mapa):
        # Toda la frula para procesar el movimiento
        if self.movingUp:
            if mapa.testColision(self.imgRect.left + C.HERO_COLISION_OFFSET,
                                 self.imgRect.top + C.HERO_COLISION_OFFSET - self.speed,
                                 self.imgRect.right - C.HERO_COLISION_OFFSET,
                                 self.imgRect.top + C.HERO_COLISION_OFFSET - self.speed):
                self.imgRect.y -= self.speed
        if self.movingDown:
            if mapa.testColision(self.imgRect.left + C.HERO_COLISION_OFFSET,
                                 self.imgRect.bottom - C.HERO_COLISION_OFFSET + self.speed,
                                 self.imgRect.right - C.HERO_COLISION_OFFSET,
                                 self.imgRect.bottom - C.HERO_COLISION_OFFSET + self.speed):
                self.imgRect.y += self.speed
        if self.movingRight:
            if mapa.testColision(self.imgRect.right - C.HERO_COLISION_OFFSET + self.speed,
                                 self.imgRect.top + C.HERO_COLISION_OFFSET,
                                 self.imgRect.right - C.HERO_COLISION_OFFSET + self.speed,
                                 self.imgRect.bottom - C.HERO_COLISION_OFFSET):
                self.imgRect.x += self.speed
        if self.movingLeft:
            if mapa.testColision(self.imgRect.left + C.HERO_COLISION_OFFSET - self.speed,
                                 self.imgRect.top + C.HERO_COLISION_OFFSET,
                                 self.imgRect.left + C.HERO_COLISION_OFFSET - self.speed,
                                 self.imgRect.bottom - C.HERO_COLISION_OFFSET):
                self.imgRect.x -= self.speed

        # Cambiar status del heroe
        if self.status == C.HERO_HURT:  # El status de "lastimado" dura 1 segundo
            if self.hpTick + C.HURT_ANIMATION_TICKRATE < pygame.time.get_ticks():
                self.status = C.HERO_IDLE
        elif self.movingLeft or self.movingRight or self.movingDown or self.movingUp:  # Si no esta lastimado, se chequea si esta caminando
            self.status = C.HERO_RUN
        else:
            self.status = C.HERO_IDLE  # Sino esta idle

        # Cambiar animaciones segun status
        if self.status == C.HERO_HURT:
            if self.anim.status != C.HERO_HURT:
                self.anim.status = C.HERO_HURT
                self.anim.startAnimation(self.framesHurt, reset=True)
        elif self.status == C.HERO_RUN:
            if self.anim.status != C.HERO_RUN:
                self.anim.status = C.HERO_RUN
                self.anim.startAnimation(self.framesCorriendo, reset=True)
        elif self.status == C.HERO_IDLE:
            if self.anim.status != C.HERO_IDLE:
                self.anim.status = C.HERO_IDLE
                self.anim.startAnimation(self.framesIdle, reset=True)

        # Update del animador
        self.anim.update()

    def damage(self):  # Metodo para quitarle una vida al heroe
        self.hp -= 1
        self.hpTick = pygame.time.get_ticks()
        self.status = C.HERO_HURT
