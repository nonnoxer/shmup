import pygame
import pygame.font
pygame.init()
pygame.font.init()
import random

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

size = (480, 360)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Shmup")

done = False

clock = pygame.time.Clock()

#TARGET AND SUBCLASSES
class Target(object):
    def __init__(self, x, y, size, spd):
        self.x = x
        self.y = y
        self.size = size
        self.spd = spd
        self.a = 0
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
        if pygame.key.get_pressed()[pygame.K_RIGHT] and self.x + self.spd <= 460:
            self.x = self.x + self.spd
        if pygame.key.get_pressed()[pygame.K_LEFT] and self.x - self.spd >= 0:
            self.x = self.x - self.spd

class Enemy(Target):
    def __init__(self, x, y, size, spd):
        Target.__init__(self, x, y, size, spd)
    def draw(self):
        return Target.draw(self)
    def update(self):
        self.y = self.y + self.spd
        self.a = self.a + 1
        if self.a % 200 == 0:
            projectiles.append(Missile(self.x + self.size // 2, self.y, 5, 2))
            self.a = 0
        elif self.a % 50 == 0:
            projectiles.append(Laser(self.x + self.size // 2, self.y, 5, 5))

class Ally(Target):
    def __init__(self):
        pass

#PROJECTILE AND SUBCLASSES
class Projectile(object):
    def __init__(self, x, y, size, spd):
        self.x = x
        self.y = y
        self.size = size
        self.spd = spd
    def draw(self):
        self.bg = pygame.Surface((self.size, self.size), pygame.SRCALPHA, 32)
        self.bg = self.bg.convert_alpha()
        return self.bg
    def update(self):
        self.y = self.y + self.spd

class Laser(Projectile):
    def __init__(self, x, y, size, spd):
        Projectile.__init__(self, x, y, size, spd)
        self.img = pygame.image.load("assets/Laser.png")
    def draw(self):
        self.bg = Projectile.draw(self)
        self.bg.blit(self.img, (0, 0))
        return self.bg
    def update(self):
        Projectile.update(self)

class Missile(Projectile):
    def __init__(self, x, y, size, spd):
        Projectile.__init__(self, x, y, size, spd)
        self.img = pygame.image.load("assets/Missile.png")
    def draw(self):
        self.bg = Projectile.draw(self)
        self.bg.blit(self.img, (0, 0))
        return self.bg
    def update(self):
        Projectile.update(self)
        if self.x > player.x:
            self.x = self.x - self.spd
        elif self.x < player.x:
            self.x = self.x + self.spd


projectiles = []
enemies = []
player = Player(230, 300, 20, 5)
a = 0

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

    screen.fill(WHITE)

    screen.blit(player.draw(), (player.x, player.y))
    player.update()
    for i in enemies:
        screen.blit(i.draw(), (i.x, i.y))
        i.update()
    for i in projectiles:
        screen.blit(i.draw(), (i.x, i.y))
        i.update()

    if a % 100 == 0:
        enemies.append(Enemy(random.randint(0, 460), -20, 20, 0.5))
        a = 0

    a = a + 1
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
