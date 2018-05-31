import sys, pygame

pygame.init()
size = width, height = 1024, 768
speed = [2, 2]
black = 0, 0, 0

screen = pygame.display.set_mode(size)

img = pygame.image.load("resources/wall.png")
imgRect = img.get_rect()

while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                sys.exit()

    screen.fill(black)
    screen.blit(img, imgRect)
    pygame.display.flip()
        