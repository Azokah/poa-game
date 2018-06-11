from enemies.bullet import Bullet
from config import constants as C


class BulletsPool:
    def __init__(self):
        self.bullets = []

        for i in range(0, C.BULLET_POOL_SIZE):
            self.bullets.append(Bullet(i))
            print("Creo Bullet: " + str(i))

    def getBullet(self):
        for i in range(0, C.BULLET_POOL_SIZE):
            if not self.bullets[i].isInUse:
                print("Get Bullet: " + str(self.bullets[i].id))
                self.bullets[i].isInUse = True
                return self.bullets[i]

        print("Get Bullet: None")
        return None

    def freeBullet(self, ID):
        for i in range(0, C.BULLET_POOL_SIZE):
            if self.bullets[i].id == ID:
                print("Free Bullet: " + str(self.bullets[i].id))
                self.bullets[i].isInUse = False