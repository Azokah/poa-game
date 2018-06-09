import json  # Para cargar los objetos
import sys

import pygame  # Para el sistema
from config import constants as C
from map.map import Mapa
from objects.gold import Gold
from objects.trap import Trap

from characters.hero import Heroe


class Game:
    def impotJsonObjects(self, path):
        self.objects = []
        with open(path) as f:
            data = json.load(f)

        for g in data:
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

    def __init__(self):
        self.screen = pygame.display.set_mode(C.SIZE)
        self.font = pygame.font.SysFont(C.FONT_TYPE, C.FONT_SIZE)
        self.mapa = Mapa()  # Inicializamos mapa
        self.impotJsonObjects(C.OBJECT_LIST[self.mapa.actualMap])  # Cargamos los objetos del mapa
        self.heroe = Heroe()  # Instanciamos al heroe
        self.finish = False  # Variable que indica si el juego no ha terminado

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

    def checkWinCondition(self):  # Metodo que consulta si el jugador se paró en la ultima casilla
        y = int(self.heroe.imgRect.center[1] / C.TILE_H)
        x = int(self.heroe.imgRect.center[0] / C.TILE_W)
        if self.mapa.mapa[y][x] == C.TILE_EXIT:
            if self.mapa.nextMap() == False: #Si no hay mas mapas
                self.finish = True #Terminamos
                print("Felicidades, ganaste!. Score: " + str(self.score))
            else:
                self.objects.clear() #Eliminamos si quedaron objetos que no agarro el usuario
                self.impotJsonObjects(C.OBJECT_LIST[self.mapa.actualMap]) #Cargamos nuevos objetos
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

        # Graficamos al heroe
        self.screen.blit(self.heroe.img, self.heroe.imgRect)

        # Graficamos GUI
        self.screen.blit(self.heartGuiImg[self.heroe.hp-1],
                        (C.SCREEN_W - C.SCORE_TEXT_OFFSET - self.heartGuiImg[self.heroe.hp-1].get_rect().width, C.FONT_SIZE*4))
        self.screen.blit(self.scoreSurface,
                         (C.SCREEN_W - C.SCORE_TEXT_OFFSET - self.scoreSurface.get_rect().width, C.FONT_SIZE))
        pygame.display.flip()  # Mostramos

    def updateScore(self):  # Metodo para actualizar el score
        if self.scoreTick + C.SCORE_TICK < pygame.time.get_ticks():
            self.score -= 1
            self.scoreTick = pygame.time.get_ticks()
            self.scoreSurface = self.font.render("Score: " + str(self.score), False, (255, 255, 255))

    def update(self):  # Update cicle del Game
        self.checkWinCondition()
        self.heroe.update(self.mapa)
        self.updateScore()
        self.checkPickObjects()
        self.checkIfPlayerDied()
