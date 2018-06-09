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
    ticks = pygame.time.get_ticks() #Obtener ticks para limitar FPS
    # Input
    game.input()

    # Update de todas las entidades
    game.update()

    # Dibujamos
    game.draw()

    pygame.time.delay(int((1000/C.DESIRED_FPS)-(pygame.time.get_ticks()-ticks))) #Limitamos FPS a C.DESIRED_FPS(60 default)