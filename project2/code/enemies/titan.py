import pygame  # Para el sistema
from config import constants as C
from enemies.enemy import Enemy


class Titan(Enemy):
    def __init__(self, X, Y, SCORE, MAP, HERO, BULLETS_AMOUNT, BULLETS_POOL):
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
        self.bulletsPool = BULLETS_POOL
        self.bulletsAmount = BULLETS_AMOUNT


    def objectsToDraw(self):
        return self.bullets

    def createBullet(self):
        if self.timer == C.BULLET_SPAWN_TIME:
            if len(self.bullets) < self.bulletsAmount:
                bullet = self.bulletsPool.getBullet()
                if bullet is not None:
                    bullet.setPosition(self.x + 1, self.y)
                    self.bullets.append(bullet)
                else:
                    return

        updatedBullets = []
        for b in self.bullets:
            b.update()

            mapCollision = self.testMapCollision(b)
            heroCollision = self.testHeroCollision(b)

            if not mapCollision and not heroCollision:
                updatedBullets.append(b)
            else:
                self.bulletsPool.freeBullet(b.id)

            if heroCollision:
                self.hero.stats.damage()
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
        if b.imgRect.colliderect(self.hero.sprite.imgRect):
            return True

        return False

    def update(self):
        self.createBullet()

        if self.timer == C.BULLET_SPAWN_TIME:
            self.timer = 0
        self.timer += 1

    def clear(self):
        for b in self.bullets:
            self.bulletsPool.freeBullet(b.id)
