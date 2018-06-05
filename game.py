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


#Cargamos el mapa desde el archivo txt
mapa = numpy.loadtxt('resources/level1-12.txt',dtype=int,delimiter=',')
print(mapa)

#Iniciamos modulos de pygame
pygame.init()
screen = pygame.display.set_mode(SIZE)

#Cargamos las imagenes
mapImg = [pygame.image.load('resources/floor1.png'), pygame.image.load('resources/wall.png'),
    pygame.image.load('resources/floor2.png'), pygame.image.load('resources/floor3.png'),]
mapImgRect = [mapImg[0].get_rect(),mapImg[1].get_rect(),mapImg[2].get_rect(),mapImg[3].get_rect()]

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
    def goTo(X,Y):
        self.gotoX = X
        self.gotoY = Y
        self.moving = True
    def moveUp(self):
        self.gotoY -= TILE_H
        self.moving = True
    def moveDown(self):
        self.gotoY += TILE_H
        self.moving = True
    def moveLeft(self):
        self.gotoX -= TILE_W
        self.moving = True
    def moveRight(self):
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
                heroe.moveUp()
            if event.key == pygame.K_DOWN:
                heroe.moveDown()
            if event.key == pygame.K_LEFT:
                heroe.moveLeft()
            if event.key == pygame.K_RIGHT:
                heroe.moveRight()

    screen.fill(BACKGROUND_COLOR)#Pintamos pantalla de negro
    #Graficamos todo el mapa
    for w in range(0, 12):
        for  j in range(0, 12):
                mapImgRect[mapa[j][w]].x = w*TILE_W
                mapImgRect[mapa[j][w]].y = j*TILE_H
                screen.blit(mapImg[mapa[j][w]], mapImgRect[mapa[j][w]])
    #Graficamos al heroe
    screen.blit(heroe.img, heroe.imgRect)

    pygame.display.flip() #Mostramos
        