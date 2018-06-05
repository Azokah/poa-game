import sys, pygame, numpy #Para el sistema
from random import randint #Para generar numeros random

#Constantes para PYGAME
SIZE = SCREEN_W, SCREEN_H = 1024, 768
SPEED = [2, 2]
BACKGROUND_COLOR = 0, 0, 0
#Constantes del JUEGO
TILE_W = 64
TILE_H = 64
MAP_W = 12 
MAP_H = 12
HERO_HP_MAX = 3
HERO_SPEED = 4

#Iniciamos modulos de pygame
pygame.init()
screen = pygame.display.set_mode(SIZE)

#Creamos el mapa
class Mapa:
    def __init__(self):
        self.mapa = numpy.loadtxt('resources/level1-12.txt',dtype=int,delimiter=',') #Cargamos el mapa desde el archivo txt
        #Cargamos las imagenes
        self.img = [pygame.image.load('resources/floor1.png'), pygame.image.load('resources/wall.png'),
            pygame.image.load('resources/floor2.png'), pygame.image.load('resources/floor3.png'),]
        self.imgRect = [self.img[0].get_rect(),self.img[1].get_rect(),self.img[2].get_rect(),self.img[3].get_rect()]

    def testColision(self,X,Y):
        X = int(X/TILE_W)
        Y = int(Y/TILE_H)
        if self.mapa[Y][X] == 1:
            return False
        return True
mapa = Mapa()
#Creamos al heroe
class Heroe:
    def __init__(self):
        self.img = pygame.image.load('resources/soupdungeon_2x/titan_2x.png')
        self.imgRect = self.img.get_rect()
        self.imgRect.x = 1*TILE_W
        self.imgRect.y = 0*TILE_H
        self.hp = HERO_HP_MAX
        self.speed = HERO_SPEED
        self.moving = False #Para saber si esta caminando o no
        self.gotoX = self.imgRect.x
        self.gotoY = self.imgRect.y

    #Metodos para setear destino
    def goTo(self,X,Y):
        self.gotoX = X
        self.gotoY = Y
        self.moving = True
    def moveUp(self,mapa):
        if mapa.testColision(self.gotoX,self.gotoY - TILE_H):
            self.gotoY -= TILE_H
            self.moving = True
    def moveDown(self,mapa):
        if mapa.testColision(self.gotoX,self.gotoY + TILE_H):
            self.gotoY += TILE_H
            self.moving = True
    def moveLeft(self,mapa):
        if mapa.testColision(self.gotoX - TILE_W,self.gotoY):
            self.gotoX -= TILE_W
            self.moving = True
    def moveRight(self,mapa):
        if mapa.testColision(self.gotoX + TILE_W,self.gotoY):
            self.gotoX += TILE_W
            self.moving = True

    #Metodo update del heroe
    def update(self):
        #Toda la frula para procesar el movimiento
        if self.imgRect.x == self.gotoX and self.imgRect.y == self.gotoY:
            self.moving = False
        elif self.gotoX != self.imgRect.x:
            if self.gotoX > self.imgRect.x:
                self.imgRect.x+=self.speed
            elif self.gotoX < self.imgRect.x:
                self.imgRect.x -= self.speed
        elif self.gotoY != self.imgRect.y:
            if self.gotoY > self.imgRect.y:
                self.imgRect.y += self.speed
            elif self.gotoY < self.imgRect.y:
                self.imgRect.y -= self.speed

    def damage(self):
        self.hp -= 1

heroe = Heroe() #Instanciamos al heroe


#El game loop simple
while 1:
    #Update de todas las entidades
    heroe.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                sys.exit()
            if event.key == pygame.K_UP:
                if heroe.moving == False:
                    heroe.moveUp(mapa)
            if event.key == pygame.K_DOWN:
                if heroe.moving == False:
                    heroe.moveDown(mapa)
            if event.key == pygame.K_LEFT:
                if heroe.moving == False:
                    heroe.moveLeft(mapa)
            if event.key == pygame.K_RIGHT:
                if heroe.moving == False:
                    heroe.moveRight(mapa)

    screen.fill(BACKGROUND_COLOR)#Pintamos pantalla de negro
    #Graficamos todo el mapa
    for w in range(0, 12):
        for  j in range(0, 12):
                mapa.imgRect[mapa.mapa[j][w]].x = w*TILE_W
                mapa.imgRect[mapa.mapa[j][w]].y = j*TILE_H
                screen.blit(mapa.img[mapa.mapa[j][w]], mapa.imgRect[mapa.mapa[j][w]])
    #Graficamos al heroe
    screen.blit(heroe.img, heroe.imgRect)

    pygame.display.flip() #Mostramos
        