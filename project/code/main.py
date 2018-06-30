import pygame

from config import constants as C
from game import Game

#Iniciamos modulos de pygame
pygame.init()
pygame.font.init()
pygame.mixer.music.load(C.MUSIC_PATH)
pygame.mixer.music.play(-1)

game = Game()  # Declaramos nuestro Game

# El game loop simple
while game.finish == False:
    # Input
    game.input()

    # Update de todas las entidades
    game.update()

    # Dibujamos
    game.draw()