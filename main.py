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
screen_rect = screen.get_rect()
pygame.display.set_caption("Shmup")

done = False

clock = pygame.time.Clock()

#TARGET AND SUBCLASSES
class Target(object):
    def __init__(self, x, y, size, spd, img):
        self.size = size
        self.spd = spd
        self.img = pygame.image.load(img)
        self.a = 0

        self.rect = self.img.get_rect()
        self.rect.x = x
        self.rect.y = y
    def draw(self):
        self.surface = pygame.Surface((self.size, self.size), pygame.SRCALPHA, 32)
        self.surface = self.surface.convert_alpha()
        self.surface.blit(self.img, (0, 0))
        return self.surface
    def update(self):
        self.a = self.a + 1

class Player(Target):
    def __init__(self, x, y, size, spd, img):
        Target.__init__(self, x, y, size, spd, img)
    def draw(self):
        return Target.draw(self)
    def update(self):
        Target.update(self)
        if pygame.key.get_pressed()[pygame.K_RIGHT]:
            self.rect.x = self.rect.x + self.spd
            self.rect.clamp_ip(screen_rect)
        elif pygame.key.get_pressed()[pygame.K_LEFT]:
            self.rect.x = self.rect.x - self.spd
            self.rect.clamp_ip(screen_rect)
        if pygame.key.get_pressed()[pygame.K_SPACE] and self.a >= 24:
            fprojectiles.append(Laser(self.rect.centerx, self.rect.centery, 5, -5, "assets/Laser.png"))
            self.a = 0

class Enemy(Target):
    def __init__(self, x, y, size, spd, img):
        Target.__init__(self, x, y, size, spd, img)
    def draw(self):
        return Target.draw(self)
    def update(self):
        Target.update(self)
        self.rect.y = self.rect.y + self.spd
        if self.a % 200 == 0:
            eprojectiles.append(Missile(self.rect.x + self.size // 2, self.rect.y, 5, 2, "assets/Missile.png"))
            self.a = 0
        elif self.a % 50 == 0:
            eprojectiles.append(Laser(self.rect.x + self.size // 2, self.rect.y, 5, 4, "assets/Laser.png"))

class Ally(Target):
    def __init__(self):
        pass

#PROJECTILE AND SUBCLASSES
class Projectile(object):
    def __init__(self, x, y, size, spd, img):
        self.size = size
        self.spd = spd
        self.img = pygame.image.load(img)

        self.rect = self.img.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
    def draw(self):
        self.surface = pygame.Surface((self.size, self.size), pygame.SRCALPHA, 32)
        self.surface = self.surface.convert_alpha()
        self.surface.blit(self.img, (0, 0))
        return self.surface
    def update(self):
        self.rect.y = self.rect.y + self.spd

class Laser(Projectile):
    def __init__(self, x, y, size, spd, img):
        Projectile.__init__(self, x, y, size, spd, img)
    def draw(self):
        self.surface = Projectile.draw(self)
        return self.surface
    def update(self):
        Projectile.update(self)

class Missile(Projectile):
    def __init__(self, x, y, size, spd, img):
        Projectile.__init__(self, x, y, size, spd, img)
    def draw(self):
        self.surface = Projectile.draw(self)
        return self.surface
    def update(self):
        Projectile.update(self)
        if self.rect.centerx > player.rect.centerx:
            self.rect.centerx = self.rect.centerx - self.spd
        elif self.rect.centerx < player.rect.centerx:
            self.rect.centerx = self.rect.centerx + self.spd


#class Misc(object):

#DEFINING OBJECTS
eprojectiles = []
fprojectiles = []
enemies = []
player = Player(230, 300, 20, 5, "assets/Ship.png")
a = 0
b = 200

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

    screen.fill(BLACK)

    #DRAWING, UPDATING AND DELETING OBJECTS
    screen.blit(player.draw(), (player.rect.x, player.rect.y))
    player.update()
    for i in enemies:
        screen.blit(i.draw(), (i.rect.x, i.rect.y))
        i.update()
        if i.rect.top > 360:
            del i
    for i in eprojectiles:
        screen.blit(i.draw(), (i.rect.x, i.rect.y))
        i.update()
        if i.rect.bottom < 0:
            del i
    for i in fprojectiles:
        screen.blit(i.draw(), (i.rect.x, i.rect.y))
        i.update()
        if i.rect.top > 360:
            del i

    if a % int(b) == 0:
        enemies.append(Enemy(random.randint(0, 460), -20, 20, 1, "assets/Enemy.png"))
        a = 0

    a = a + 1
    b = b - 0.1
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
