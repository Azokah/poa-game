import sys, pygame, numpy #Para el sistema
from random import randint #Para generar numeros random
import json #Para cargar los objetos

#Constantes para PYGAME
SIZE = SCREEN_W, SCREEN_H = 1024, 768
SPEED = [2, 2]
FONT_SIZE = 30
BACKGROUND_COLOR = 0, 0, 0
#Constantes del JUEGO
TILE_W = 64
TILE_H = 64
TILE_WALL = 1
TILE_FLOOR = 0
TILE_ENTRY = 2
TILE_EXIT = 3
MAP_W = 12 
MAP_H = 12
HERO_HP_MAX = 3
HERO_SPEED = 4
HERO_COLISION_OFFSET = 12
HERO_SIZE_W = 32
HERO_SIZE_H = 32
MAX_SCORE = 1000 
SCORE_TICK = 250 #Milisegundos en los que tarda en bajar 1 punto de score
SCORE_TEXT_OFFSET = 16
MAP1_PATH = 'resources/level1.txt'
OBJECTS1_PATH = 'resources/level1-objects.json'
TILE_FLOOR1_PATH = 'resources/floor1.png'
TILE_WALL_PATH = 'resources/wall.png'
TILE_FLOOR2_PATH = 'resources/floor2.png'
TILE_FLOOR3_PATH = 'resources/floor3.png'
HERO_SURFACE_RUNNING_PATH = 'resources/sheet_hero_walk.png'
HERO_RUNNING_FRAMES = 3
HERO_SURFACE_IDLE_PATH = 'resources/sheet_hero_idle.png'
HERO_IDLE_FRAMES = 8
HERO_SURFACE_HURT_PATH = 'resources/sheet_hero_hurt.png'
HERO_HURT_FRAMES = 4
HURT_ANIMATION_TICKRATE = 1000
#Enum de estados de heroe
HERO_IDLE = 0
HERO_RUN = 1
HERO_HURT = 2
FONT_TYPE = 'Arial'
OBJECT_GOLD_PATH = 'resources/soupdungeon_2x/gold_pile_16_2x.png'
OBJECT_TRAP_PATH = 'resources/soupdungeon_2x/crystal_wall_lightred_2x.png'
ANIMATION_TICKRATE = 150


#Iniciamos modulos de pygame
pygame.init()
pygame.font.init()

#Creamos el mapa
class Mapa:
    def __init__(self):
        self.mapa = numpy.loadtxt(MAP1_PATH,dtype=int,delimiter=',') #Cargamos el mapa desde el archivo txt
        #Cargamos las imagenes
        self.img = [pygame.image.load(TILE_FLOOR1_PATH), pygame.image.load(TILE_WALL_PATH),
            pygame.image.load(TILE_FLOOR2_PATH), pygame.image.load(TILE_FLOOR3_PATH),]
        self.imgRect = [self.img[0].get_rect(),self.img[1].get_rect(),self.img[2].get_rect(),self.img[3].get_rect()]

    def testColision(self,X,Y,XX,YY): #Para testear si colisiona el jugador con alguna casilla tipo pared
        X = int(X/TILE_W)
        Y = int(Y/TILE_H)
        XX = int(XX/TILE_W)
        YY = int(YY/TILE_H)
        if self.mapa[Y][X] == TILE_WALL:
            return False
        elif self.mapa[YY][XX] == TILE_WALL:
            return False
        elif self.mapa[YY][X] == TILE_WALL:
            return False
        elif self.mapa[Y][XX] == TILE_WALL:
            return False
        return True


#Creamos un animador para efectos de animacion
class Animator:
    def __init__(self,object):
        self.animationTick = pygame.time.get_ticks()
        self.currentFrame = 0
        self.status = HERO_IDLE
        self.object = object

    def startAnimation(self, sequence, reset = False):
        if reset == True:
            self.currentFrame = 0
        self.sequence = sequence
        

    def update(self):
        self.object.img = self.sequence[self.currentFrame]
        if self.animationTick+ANIMATION_TICKRATE < pygame.time.get_ticks():
            self.currentFrame+=1
            self.animationTick = pygame.time.get_ticks()
        if self.currentFrame >= len(self.sequence)-1:
            self.currentFrame = 0


#Creamos al heroe
class Heroe(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.cargarFramesAnimacion()
        self.imgRect = self.img.get_rect()
        self.imgRect.x = 1*TILE_W
        self.imgRect.y = 0*TILE_H
        self.hp = HERO_HP_MAX
        self.speed = HERO_SPEED
        self.status = HERO_IDLE
        self.gotoX = self.imgRect.x
        self.gotoY = self.imgRect.y
        self.movingDown = self.movingUp = self.movingRight = self.movingLeft = False
        self.anim = Animator(self)
        self.anim.startAnimation(self.framesIdle)

    def cargarFramesAnimacion(self):
        self.img = pygame.image.load(HERO_SURFACE_RUNNING_PATH)
        self.framesCorriendo = []
        for w in range(0,HERO_RUNNING_FRAMES):
            self.framesCorriendo.append(self.img.subsurface((HERO_SIZE_W*w,0,HERO_SIZE_W,HERO_SIZE_H)))
        self.img = pygame.image.load(HERO_SURFACE_IDLE_PATH)
        self.framesIdle = []
        for w in range(0,HERO_IDLE_FRAMES):
            self.framesIdle.append(self.img.subsurface((HERO_SIZE_W*w,0,HERO_SIZE_W,HERO_SIZE_H)))
        self.img = pygame.image.load(HERO_SURFACE_HURT_PATH)
        self.framesHurt = []
        for w in range(0,HERO_HURT_FRAMES):
            self.framesHurt.append(self.img.subsurface((HERO_SIZE_W*w,0,HERO_SIZE_W,HERO_SIZE_H)))
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
    
    #Metodo update del heroe
    def update(self,mapa):
        #Toda la frula para procesar el movimiento
        if self.movingUp:
            if mapa.testColision(self.imgRect.left+HERO_COLISION_OFFSET,self.imgRect.top+HERO_COLISION_OFFSET - self.speed,
                                 self.imgRect.right-HERO_COLISION_OFFSET,self.imgRect.top+HERO_COLISION_OFFSET - self.speed):
                self.imgRect.y -= self.speed
        if self.movingDown:
            if mapa.testColision(self.imgRect.left+HERO_COLISION_OFFSET,self.imgRect.bottom-HERO_COLISION_OFFSET + self.speed,
                                 self.imgRect.right-HERO_COLISION_OFFSET, self.imgRect.bottom-HERO_COLISION_OFFSET + self.speed):
                self.imgRect.y += self.speed
        if self.movingRight:
            if mapa.testColision(self.imgRect.right-HERO_COLISION_OFFSET + self.speed,self.imgRect.top+HERO_COLISION_OFFSET,
                                 self.imgRect.right-HERO_COLISION_OFFSET + self.speed,self.imgRect.bottom-HERO_COLISION_OFFSET):
                self.imgRect.x += self.speed
        if self.movingLeft:
            if mapa.testColision(self.imgRect.left+HERO_COLISION_OFFSET - self.speed,self.imgRect.top+HERO_COLISION_OFFSET,
                                 self.imgRect.left+HERO_COLISION_OFFSET - self.speed,self.imgRect.bottom-HERO_COLISION_OFFSET):
                self.imgRect.x -= self.speed

        #Cambiar status del heroe
        if self.status == HERO_HURT: #El status de "lastimado" dura 1 segundo
            if self.hpTick+HURT_ANIMATION_TICKRATE < pygame.time.get_ticks(): 
                self.status = HERO_IDLE
        elif self.movingLeft or self.movingRight or self.movingDown or self.movingUp: #Si no esta lastimado, se chequea si esta caminando
            self.status = HERO_RUN
        else:
            self.status = HERO_IDLE #Sino esta idle
        
        #Cambiar animaciones segun status
        if self.status == HERO_HURT:
            if self.anim.status != HERO_HURT:
                self.anim.status = HERO_HURT
                self.anim.startAnimation(self.framesHurt,reset = True)
        elif self.status == HERO_RUN:
            if self.anim.status != HERO_RUN:
                self.anim.status = HERO_RUN
                self.anim.startAnimation(self.framesCorriendo,reset = True)
        elif self.status == HERO_IDLE:
            if self.anim.status != HERO_IDLE:
                self.anim.status = HERO_IDLE
                self.anim.startAnimation(self.framesIdle,reset = True)

        #Update del animador
        self.anim.update()


    def damage(self): #Metodo para quitarle una vida al heroe
        self.hp -= 1
        self.hpTick = pygame.time.get_ticks()
        self.status = HERO_HURT


class Object(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.img = pygame.image.load(OBJECT_GOLD_PATH)
        self.imgRect = self.img.get_rect()
        self.imgRect.x = 1*TILE_W
        self.imgRect.y = 0*TILE_H
        self.scoreAdd = 0

class Gold(Object):
    def __init__(self,X,Y,SCORE):
        super()
        self.img = pygame.image.load(OBJECT_GOLD_PATH)
        self.imgRect = self.img.get_rect()
        self.imgRect.x = X*TILE_W
        self.imgRect.y = Y*TILE_H
        self.scoreAdd = SCORE

class Trap(Object):
    def __init__(self,X,Y,SCORE):
        super()
        self.img = pygame.image.load(OBJECT_TRAP_PATH)
        self.imgRect = self.img.get_rect()
        self.imgRect.x = X*TILE_W
        self.imgRect.y = Y*TILE_H
        self.scoreAdd = SCORE
        
class Game:
    def impotJsonObjects(self,path):
        self.objects = []
        with open(path) as f:
            data = json.load(f)

        for g in data:
            if g["type"] == "gold":
                x = int(g["x"])
                y = int(g["y"])
                score = int(g["scoreAdd"])
                self.objects.append(Gold(x,y,score))
            if g["type"] == "trap":
                x = int(g["x"])
                y = int(g["y"])
                score = int(g["scoreAdd"])
                self.objects.append(Trap(x,y,score))
        

    def __init__(self):
        self.screen = pygame.display.set_mode(SIZE)
        self.font = pygame.font.SysFont(FONT_TYPE, FONT_SIZE)
        self.mapa = Mapa() #Inicializamos mapa
        self.heroe = Heroe() #Instanciamos al heroe
        self.finish = False
        self.score = MAX_SCORE
        self.scoreTick = pygame.time.get_ticks()
        self.scoreSurface = self.font.render("Score: "+str(self.score), False, (255, 255, 255))
        self.impotJsonObjects(OBJECTS1_PATH)

    
    def checkIfPlayerDied(self):#Metodo que consulta si el jugador murio
        if self.heroe.hp <= 0:
            self.finish = True
            print("Has muerto!. Score: "+ str(self.score))
    
    def checkPickObjects(self):#Metodo que consulta si el jugador colisiono con algun objeto
        y = int(self.heroe.imgRect.center[1]/TILE_H)
        x = int(self.heroe.imgRect.center[0]/TILE_W)

        for o in self.objects:
            if o.imgRect.colliderect(self.heroe.imgRect):
                self.score += o.scoreAdd
                if o.scoreAdd < 0:
                    self.heroe.damage()
                self.objects.remove(o)

    def checkWinCondition(self):#Metodo que consulta si el jugador se paró en la ultima casilla
        y = int(self.heroe.imgRect.center[1]/TILE_H)
        x = int(self.heroe.imgRect.center[0]/TILE_W)
        if self.mapa.mapa[y][x] == TILE_EXIT:
            self.finish = True
            print("Felicidades, ganaste!. Score: "+ str(self.score))
            
    def input(self):#Input del juego
        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    sys.exit()
                if event.key == pygame.K_UP:
                    self.heroe.walkUp()
                if event.key == pygame.K_DOWN:
                        self.heroe.walkDown()
                if event.key == pygame.K_LEFT:
                        self.heroe.walkLeft()
                if event.key == pygame.K_RIGHT:
                        self.heroe.walkRight()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_UP:
                        self.heroe.stopUp()
                if event.key == pygame.K_DOWN:
                        self.heroe.stopDown()
                if event.key == pygame.K_LEFT:
                        self.heroe.stopLeft()
                if event.key == pygame.K_RIGHT:
                        self.heroe.stopRight()

    def draw(self):
        self.screen.fill(BACKGROUND_COLOR)#Pintamos pantalla de negro
        #Graficamos todo el mapa
        for w in range(0, 12):
            for  j in range(0, 12):
                    self.mapa.imgRect[self.mapa.mapa[j][w]].x = w*TILE_W
                    self.mapa.imgRect[self.mapa.mapa[j][w]].y = j*TILE_H
                    self.screen.blit(self.mapa.img[self.mapa.mapa[j][w]], self.mapa.imgRect[self.mapa.mapa[j][w]])

        #Graficamos objetos
        for o in self.objects:
            self.screen.blit(o.img,o.imgRect)

        #Graficamos al heroe
        self.screen.blit(self.heroe.img, self.heroe.imgRect)
        
        #Graficamos GUI
        self.screen.blit(self.scoreSurface,(SCREEN_W-SCORE_TEXT_OFFSET-self.scoreSurface.get_rect().width,FONT_SIZE))
        pygame.display.flip() #Mostramos

    def updateScore(self):#Metodo para actualizar el score
        if self.scoreTick+SCORE_TICK < pygame.time.get_ticks():
            self.score -= 1
            self.scoreTick = pygame.time.get_ticks()
            self.scoreSurface = self.font.render("Score: " + str(self.score), False, (255, 255, 255))

    def update(self): #Update cicle del Game
        self.checkWinCondition()
        self.heroe.update(self.mapa)
        self.updateScore()
        self.checkPickObjects()
        self.checkIfPlayerDied()

game = Game()#Declaramos nuestro Game

#El game loop simple
while game.finish == False:
    #Update de todas las entidades
    game.update()
    
    #Input
    game.input()

    #Dibujamos
    game.draw()