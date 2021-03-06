import pygame  # Para el sistema
import numpy  # Para el sistema
from config import constants as C


# Creamos un animador para efectos de animacion
class Animator:
    def __init__(self):
        self.animationTick = pygame.time.get_ticks()
        self.currentFrame = 0
        self.status = C.HERO_IDLE

    def startAnimation(self, sequence, reset=False):
        if reset == True:
            self.currentFrame = 0
        self.sequence = sequence

    def update(self,stats,sprite):
        sprite.img = self.sequence[self.currentFrame]
        if self.animationTick + C.ANIMATION_TICKRATE < pygame.time.get_ticks():
            self.currentFrame += 1
            self.animationTick = pygame.time.get_ticks()
        if self.currentFrame >= len(self.sequence) - 1:
            self.currentFrame = 0

        
        # Cambiar animaciones segun status
        if stats.status == C.HERO_HURT:
            if self.status != C.HERO_HURT:
                self.status = C.HERO_HURT
                self.startAnimation(sprite.framesHurt, reset=True)
        elif stats.status == C.HERO_RUN:
            if self.status != C.HERO_RUN:
                self.status = C.HERO_RUN
                self.startAnimation(sprite.framesCorriendo, reset=True)
        elif stats.status == C.HERO_IDLE:
            if self.status != C.HERO_IDLE:
                self.status = C.HERO_IDLE
                self.startAnimation(sprite.framesIdle, reset=True)


class Sprite(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.cargarFramesAnimacion()
        self.imgRect = self.img.get_rect()
        self.imgRect.x = 1 * C.TILE_W
        self.imgRect.y = 0 * C.TILE_H

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

    def relocateTo(self, x, y):
        self.imgRect.x = x*C.TILE_W
        self.imgRect.y = y*C.TILE_H

    
    def draw(self, screen):
        # Graficamos al heroe
        screen.blit(self.img, self.imgRect)

class Stats:
    def __init__(self):
        self.hp = C.HERO_HP_MAX
        self.status = C.HERO_IDLE

    def damage(self):  # Metodo para quitarle una vida al heroe
        self.hp -= 1
        self.hpTick = pygame.time.get_ticks()
        self.status = C.HERO_HURT
    
    
    def update(self,phisics):
        # Cambiar status del heroe
        if self.status == C.HERO_HURT:  # El status de "lastimado" dura 1 segundo
            if self.hpTick + C.HURT_ANIMATION_TICKRATE < pygame.time.get_ticks():
                self.status = C.HERO_IDLE
        elif phisics.movingLeft or phisics.movingRight or phisics.movingDown or phisics.movingUp:  # Si no esta lastimado, se chequea si esta caminando
            self.status = C.HERO_RUN
        else:
            self.status = C.HERO_IDLE  # Sino esta idle


class Phisics:
    def __init__(self,x,y):
        self.speed = C.HERO_SPEED
        self.gotoX = x
        self.gotoY = y
        self.movingDown = self.movingUp = self.movingRight = self.movingLeft = False
        
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
    def update(self, sprite,mapa):
        # Toda la frula para procesar el movimiento
        if self.movingUp:
            if mapa.testColision(sprite.imgRect.left + C.HERO_COLISION_OFFSET,
                                 sprite.imgRect.top + C.HERO_COLISION_OFFSET - self.speed,
                                 sprite.imgRect.right - C.HERO_COLISION_OFFSET,
                                 sprite.imgRect.top + C.HERO_COLISION_OFFSET - self.speed):
                sprite.imgRect.y -= self.speed
        if self.movingDown:
            if mapa.testColision(sprite.imgRect.left + C.HERO_COLISION_OFFSET,
                                 sprite.imgRect.bottom - C.HERO_COLISION_OFFSET + self.speed,
                                 sprite.imgRect.right - C.HERO_COLISION_OFFSET,
                                 sprite.imgRect.bottom - C.HERO_COLISION_OFFSET + self.speed):
                sprite.imgRect.y += self.speed
        if self.movingRight:
            if mapa.testColision(sprite.imgRect.right - C.HERO_COLISION_OFFSET + self.speed,
                                 sprite.imgRect.top + C.HERO_COLISION_OFFSET,
                                 sprite.imgRect.right - C.HERO_COLISION_OFFSET + self.speed,
                                 sprite.imgRect.bottom - C.HERO_COLISION_OFFSET):
                sprite.imgRect.x += self.speed
        if self.movingLeft:
            if mapa.testColision(sprite.imgRect.left + C.HERO_COLISION_OFFSET - self.speed,
                                 sprite.imgRect.top + C.HERO_COLISION_OFFSET,
                                 sprite.imgRect.left + C.HERO_COLISION_OFFSET - self.speed,
                                 sprite.imgRect.bottom - C.HERO_COLISION_OFFSET):
                sprite.imgRect.x -= self.speed


class Mapa:
    def __init__(self):
        self.mapaList = []
        for m in range(0, len(C.MAP_LIST)):
            self.mapaList.append(numpy.loadtxt(C.MAP_LIST[m], dtype=int, delimiter=','))  # Cargamos el mapa desde el archivo txt
        self.actualMap = 0
        self.mapa = self.mapaList[self.actualMap]
        # Cargamos las imagenes
        self.img = [pygame.image.load(C.TILE_FLOOR1_PATH), pygame.image.load(C.TILE_WALL_PATH),
                    pygame.image.load(C.TILE_FLOOR2_PATH), pygame.image.load(C.TILE_FLOOR3_PATH), ]
        self.imgRect = [self.img[0].get_rect(), self.img[1].get_rect(), self.img[2].get_rect(), self.img[3].get_rect()]

    #Metodo que cambia de mapa y devuelve True si lo hace
    #Devuelve false si no hay mas mapas en la lista
    def nextMap(self):
        self.actualMap += 1
        if self.actualMap < len(C.MAP_LIST):
            self.mapa = self.mapaList[self.actualMap]
            return True
        return False
    
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

    def draw(self,screen):
        for w in range(0, C.MAP_W):
            for j in range(0, C.MAP_H):
                self.imgRect[self.mapa[j][w]].x = w * C.TILE_W
                self.imgRect[self.mapa[j][w]].y = j * C.TILE_H
                screen.blit(self.img[self.mapa[j][w]], self.imgRect[self.mapa[j][w]])