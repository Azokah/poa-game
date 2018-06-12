import pygame  # Para el sistema

from config import constants as C


class ObjectsFlyweight:
    def __init__(self):
        self.flyweights = {}

    def getFlyweight(self, key):
        try:
            flyweight = self.flyweights[key]
        except KeyError:
            if key == 'gold':
                flyweight = GoldFlyweight()
            elif key == 'trap':
                flyweight = TrapFlyweight()
            else:
                flyweight = None

            self.flyweights[key] = flyweight
        return flyweight


class GoldFlyweight:
    def __init__(self):
        self.score = C.GOLD_SCORE


class TrapFlyweight:
    def __init__(self):
        self.score = C.TRAP_SCORE
