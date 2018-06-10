import json  # Para cargar los objetos
import sys

import pygame  # Para el sistema
from config import constants as C
from objects.gold import Gold
from objects.trap import Trap

from characters.gameObject import GameObject, mapObject


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
        self.mapa = mapObject().mapa  # Inicializamos mapa
        self.impotJsonObjects(C.OBJECT_LIST[self.mapa.actualMap])  # Cargamos los objetos del mapa
        self.heroe = GameObject()  # Instanciamos al heroe
        self.finish = False  # Variable que indica si el juego no ha terminado



        #De aca para abajo es todo HUD y GUI deberia tener su propia clase pero ya fue
        #Para control de FPS
        self.fps = 0 #FPS
        self.maxFps = self.fps
        self.fpsTick = pygame.time.get_ticks() #Reloj de FPS
        self.fpsSurface = self.font.render("Fps: " + str(self.maxFps), False,
                                             (255, 0, 0))

        
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
                    self.heroe.sprite.relocateTo(w,j)

    def checkIfPlayerDied(self):  # Metodo que consulta si el jugador murio
        if self.heroe.stats.hp <= 0:
            self.finish = True
            print("Has muerto!. Score: " + str(self.score))
            #Tirar losing surface

    def checkPickObjects(self):  # Metodo que consulta si el jugador colisiono con algun objeto
        y = int(self.heroe.sprite.imgRect.center[1] / C.TILE_H)
        x = int(self.heroe.sprite.imgRect.center[0] / C.TILE_W)

        for o in self.objects:
            if o.imgRect.colliderect(self.heroe.sprite.imgRect):
                self.score += o.scoreAdd
                if o.scoreAdd < 0:
                    self.heroe.stats.damage()
                    self.soundHurt.play()
                else:
                    self.soundCoin.play()
                self.objects.remove(o)

    def checkWinCondition(self):  # Metodo que consulta si el jugador se paró en la ultima casilla
        y = int(self.heroe.sprite.imgRect.center[1] / C.TILE_H)
        x = int(self.heroe.sprite.imgRect.center[0] / C.TILE_W)
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
                    self.heroe.phisics.walkUp()
                if event.key == pygame.K_DOWN:
                    self.heroe.phisics.walkDown()
                if event.key == pygame.K_LEFT:
                    self.heroe.phisics.walkLeft()
                if event.key == pygame.K_RIGHT:
                    self.heroe.phisics.walkRight()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_UP:
                    self.heroe.phisics.stopUp()
                if event.key == pygame.K_DOWN:
                    self.heroe.phisics.stopDown()
                if event.key == pygame.K_LEFT:
                    self.heroe.phisics.stopLeft()
                if event.key == pygame.K_RIGHT:
                    self.heroe.phisics.stopRight()

    def draw(self):
        self.screen.fill(C.BACKGROUND_COLOR)  # Pintamos pantalla de negro
        # Graficamos todo el mapa
        self.mapa.draw(self.screen)

        # Graficamos objetos
        for o in self.objects:
            o.draw(self.screen)

        # Graficamos al heroe
        self.heroe.sprite.draw(self.screen)

        # Graficamos GUI
        self.screen.blit(self.heartGuiImg[self.heroe.stats.hp-1],
                        (C.SCREEN_W - C.SCORE_TEXT_OFFSET - self.heartGuiImg[self.heroe.stats.hp-1].get_rect().width, C.FONT_SIZE*4))
        self.screen.blit(self.scoreSurface,
                         (C.SCREEN_W - C.SCORE_TEXT_OFFSET - self.scoreSurface.get_rect().width, C.FONT_SIZE))
        self.screen.blit(self.fpsSurface,
                         (C.SCREEN_W - C.SCORE_TEXT_OFFSET - self.fpsSurface.get_rect().width, C.FONT_SIZE*6))

        pygame.display.flip()  # Mostramos

    def updateScore(self):  # Metodo para actualizar el score
        if self.scoreTick + C.SCORE_TICK < pygame.time.get_ticks():
            self.score -= 1
            self.scoreTick = pygame.time.get_ticks()
            self.scoreSurface = self.font.render("Score: " + str(self.score), False, (255, 255, 255))

    def update(self):  # Update cicle del Game
        self.checkFPS()
        self.checkWinCondition()
        self.heroe.update(self.mapa)
        self.updateScore()
        self.checkPickObjects()
        self.checkIfPlayerDied()
