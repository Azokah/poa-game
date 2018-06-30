import json  # Para cargar los objetos
import sys

import pygame  # Para el sistema
from config import constants as C
from map.map import Mapa
from objects.gold import Gold
from objects.trap import Trap

from characters.hero import Heroe
from enemies.titan import Titan

class Game:

    def importJson(self, path):
        self.objects = []
        self.enemies = []

        with open(path) as f:
            data = json.load(f)

        for g in data:
            self.importJsonObjects(g)  # Cargamos los objetos del mapa
            self.importJsonEnemies(g)  # Cargamos los enemigos del mapa

    def importJsonObjects(self, g):
        if g["type"] == "gold":
            x = int(g["x"])
            y = int(g["y"])
            score = int(g["scoreAdd"])
            self.objects.append(Gold(x, y, score))
        if g["type"] == "trap":
            x = int(g["x"])
            y = int(g["y"])
            score = int(g["scoreAdd"])
            self.objects.append(Trap(x, y, score))

    def importJsonEnemies(self, g):
        if g["type"] == "titan":
            x = int(g["x"])
            y = int(g["y"])
            score = int(g["scoreAdd"])
            self.enemies.append(Titan(x, y, score, self.mapa, self.heroe))

    def __init__(self):
        self.screen = pygame.display.set_mode(C.SIZE)
        self.font = pygame.font.SysFont(C.FONT_TYPE, C.FONT_SIZE)
        self.mapa = Mapa()  # Inicializamos mapa
        self.heroe = Heroe()  # Instanciamos al heroe. Necesito cargarlo antes del json
        self.importJson(C.OBJECT_LIST[self.mapa.actualMap])

        self.finish = False  # Variable que indica si el juego no ha terminado

        #Para control de FPS
        self.fps = 0 #FPS
        self.maxFps = self.fps
        self.fpsTick = pygame.time.get_ticks() #Reloj de FPS
        self.fpsSurface = self.font.render("Fps: " + str(self.maxFps), False,
                                             (255, 0, 0))

        #De aca para abajo es todo HUD y GUI
        self.score = C.MAX_SCORE  # Puntaje
        self.scoreTick = pygame.time.get_ticks()  # Reloj del puntaje
        self.scoreSurface = self.font.render("Score: " + str(self.score), False,
                                             (255, 255, 255))  # Surface del texto para graficar puntaje
        self.soundHurt = pygame.mixer.Sound(C.SOUND_HURT_PATH)  # Cargamos sonido  hurt
        self.soundCoin = pygame.mixer.Sound(C.SOUND_COIN_PATH)  # Cargamos sonido Coin
        self.heartGuiImg = []
        self.heartGuiImg.append(pygame.image.load(C.HEART_1_SURFACE))
        self.heartGuiImg.append(pygame.image.load(C.HEART_2_SURFACE))
        self.heartGuiImg.append(pygame.image.load(C.HEART_3_SURFACE))


    def checkFPS(self):
        if self.fpsTick+1000 > pygame.time.get_ticks():
            self.fps += 1
        else:
            self.maxFps = self.fps
            self.fpsSurface = self.font.render("Fps: " + str(self.maxFps), False,
                                             (255, 0, 0))
            self.fpsTick = pygame.time.get_ticks()
            self.fps = 0
        

    def relocateHero(self):
        for w in range(0, C.MAP_W):
            for j in range(0, C.MAP_H):
                if self.mapa.mapa[j][w] == C.TILE_ENTRY:
                    self.heroe.imgRect.x = w*C.TILE_W
                    self.heroe.imgRect.y = j*C.TILE_H

    def checkIfPlayerDied(self):  # Metodo que consulta si el jugador murio
        if self.heroe.hp <= 0:
            self.finish = True
            print("Has muerto!. Score: " + str(self.score))
            #Tirar losing surface

    def checkPickObjects(self):  # Metodo que consulta si el jugador colisiono con algun objeto
        y = int(self.heroe.imgRect.center[1] / C.TILE_H)
        x = int(self.heroe.imgRect.center[0] / C.TILE_W)

        for o in self.objects:
            if o.imgRect.colliderect(self.heroe.imgRect):
                self.score += o.scoreAdd
                if o.scoreAdd < 0:
                    self.heroe.damage()
                    self.soundHurt.play()
                else:
                    self.soundCoin.play()
                self.objects.remove(o)

        for o in self.enemies:
            if o.imgRect.colliderect(self.heroe.imgRect):
                self.score += o.scoreAdd
                if o.scoreAdd < 0:
                    self.heroe.damage()
                    self.soundHurt.play()
                else:
                    self.soundCoin.play()
                self.enemies.remove(o)

    def checkWinCondition(self):  # Metodo que consulta si el jugador se paró en la ultima casilla
        y = int(self.heroe.imgRect.center[1] / C.TILE_H)
        x = int(self.heroe.imgRect.center[0] / C.TILE_W)
        if self.mapa.mapa[y][x] == C.TILE_EXIT:
            if self.mapa.nextMap() == False: #Si no hay mas mapas
                self.finish = True #Terminamos
                print("Felicidades, ganaste!. Score: " + str(self.score))
            else:
                self.objects.clear() #Eliminamos si quedaron objetos que no agarro el usuario
                self.enemies.clear() #Eliminamos los enemigos
                self.importJson(C.OBJECT_LIST[self.mapa.actualMap]) #Cargamos nuevos objetos
                self.relocateHero()# Reallocamos al heroe

    def input(self):  # Input del juego
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
        self.screen.fill(C.BACKGROUND_COLOR)  # Pintamos pantalla de negro
        # Graficamos todo el mapa
        for w in range(0, C.MAP_W):
            for j in range(0, C.MAP_H):
                self.mapa.imgRect[self.mapa.mapa[j][w]].x = w * C.TILE_W
                self.mapa.imgRect[self.mapa.mapa[j][w]].y = j * C.TILE_H
                self.screen.blit(self.mapa.img[self.mapa.mapa[j][w]], self.mapa.imgRect[self.mapa.mapa[j][w]])

        # Graficamos objetos
        for o in self.objects:
            self.screen.blit(o.img, o.imgRect)

        # Graficamos enemigos
        for o in self.enemies:
            self.screen.blit(o.img, o.imgRect)
            for i in o.objectsToDraw():
                self.screen.blit(i.img, i.imgRect)

        # Graficamos al heroe
        self.screen.blit(self.heroe.img, self.heroe.imgRect)

        # Graficamos GUI
        self.screen.blit(self.heartGuiImg[self.heroe.hp-1],
                        (C.SCREEN_W - C.SCORE_TEXT_OFFSET - self.heartGuiImg[self.heroe.hp-1].get_rect().width, C.FONT_SIZE*4))
        self.screen.blit(self.scoreSurface,
                         (C.SCREEN_W - C.SCORE_TEXT_OFFSET - self.scoreSurface.get_rect().width, C.FONT_SIZE))
        self.screen.blit(self.fpsSurface,
                         (C.SCREEN_W - C.SCORE_TEXT_OFFSET - self.fpsSurface.get_rect().width, C.FONT_SIZE*6))


    def updateScore(self):  # Metodo para actualizar el score
        if self.scoreTick + C.SCORE_TICK < pygame.time.get_ticks():
            self.score -= 1
            self.scoreTick = pygame.time.get_ticks()
            self.scoreSurface = self.font.render("Score: " + str(self.score), False, (255, 255, 255))

    def update(self):  # Update cicle del Game
        self.checkFPS()
        self.checkWinCondition()
        self.heroe.update(self.mapa)
        for e in self.enemies:
            e.update()
        self.updateScore()
        self.checkPickObjects()
        self.checkIfPlayerDied()
        pygame.display.flip()  # Mostramos
