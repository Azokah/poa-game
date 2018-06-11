import pygame  # Para el sistema
from enemies.enemy import Enemy
from enemies.bullet import Bullet

from config import constants as C


class Titan(Enemy):
    def __init__(self, X, Y, SCORE, MAP, HERO):
        self.x = X
        self.y = Y
        self.scoreAdd = SCORE
        self.map = MAP
        self.img = pygame.image.load(C.ENEMY_1_IMAGE)
        self.imgRect = self.img.get_rect()
        self.imgRect.x = self.x * C.TILE_W
        self.imgRect.y = self.y * C.TILE_H
        self.bullets = []
        self.createBulletEvent = pygame.USEREVENT + 1
        self.timer = C.BULLET_SPAWN_TIME
        self.hero = HERO
        self.soundHurt = pygame.mixer.Sound(C.SOUND_HURT_PATH)


    def objectsToDraw(self):
        return self.bullets

    def createBullet(self):
        if self.timer == C.BULLET_SPAWN_TIME:
            if len(self.bullets) < C.BULLETS_AMOUNT:
                bullet = Bullet(self.x + 1, self.y)
                self.bullets.append(bullet)

        updatedBullets = []
        for b in self.bullets:
            b.update()

            mapCollision = self.testMapCollision(b)
            heroCollision = self.testHeroCollision(b)

            if not mapCollision and not heroCollision:
                updatedBullets.append(b)

            if heroCollision:
                self.hero.damage()
                self.soundHurt.play()

            self.bullets = updatedBullets

    def testMapCollision(self, b):
        # Al parecer de esta forma funciona
        if not self.map.testColision(b.imgRect.right - C.HERO_COLISION_OFFSET,
                                 b.imgRect.top + C.HERO_COLISION_OFFSET,
                                 b.imgRect.right - C.HERO_COLISION_OFFSET,
                                 b.imgRect.bottom - C.HERO_COLISION_OFFSET):
            return True

        return False

    def testHeroCollision(self, b):
        if b.imgRect.colliderect(self.hero.imgRect):
            return True

        return False

    def update(self):
        self.createBullet()

        if self.timer == C.BULLET_SPAWN_TIME:
            self.timer = 0
        self.timer += 1
