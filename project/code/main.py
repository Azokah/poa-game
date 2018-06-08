import pygame

from project.code.config import constants as C
from project.code.game import Game

#Iniciamos modulos de pygame
pygame.init()
pygame.font.init()
pygame.mixer.music.load(C.MUSIC_PATH)
pygame.mixer.music.play(-1)

game = Game()  # Declaramos nuestro Game

# El game loop simple
while game.finish == False:
    # Update de todas las entidades
    game.update()

    # Input
    game.input()

    # Dibujamos
    game.draw()