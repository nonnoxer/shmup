import pygame
pygame.init()

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

class Target(object):
    def __init__(self, x, y, size, spd):
        self.x = x
        self.y = y
        self.size = size
        self.spd = spd
    def draw(self):
        self.bg = pygame.Surface((self.size, self.size), pygame.SRCALPHA, 32)
        self.bg = self.bg.convert_alpha()
        pygame.draw.circle(self.bg, BLACK, (self.size // 2, self.size // 2), self.size, 0)
        return self.bg

class Player(Target):
    def __init__(self, x, y, size, spd):
        Target.__init__(self, x, y, size, spd)
    def draw(self):
        return Target.draw(self)
    def update(self):
        if pygame.key.get_pressed()[pygame.K_RIGHT] and self.x + self.spd <= 960 - self.size:
            self.x = self.x + self.spd
        if pygame.key.get_pressed()[pygame.K_LEFT] and self.x - self.spd >= 0:
            self.x = self.x - self.spd

class Enemy(Target):
    def __init__(self):
        pass

class Ally(Target):
    def __init__(self):
        pass
