#INITIALISE=====================================================================
import pygame
import pygame.font
pygame.init()
pygame.font.init()
import random


#SETUP==========================================================================
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



#TARGET AND SUBCLASSES##########################################################


#TARGET PARENT CLASS============================================================
class Target(pygame.sprite.Sprite):
    """Parent class for all shootable objects"""

#PARENT CLASS INIT--------------------------------------------------------------
    def __init__(self, x, y, size, spd, img):
        pygame.sprite.Sprite.__init__(self)
        self.size = size
        self.spd = spd
        self.img = pygame.image.load(img)
        self.a = 0
        self.rect = self.img.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.mask = pygame.mask.from_surface(self.img)

#PARENT CLASS DRAW--------------------------------------------------------------
    def draw(self):
        self.surface = pygame.Surface((self.size, self.size), pygame.SRCALPHA, 32)
        self.surface = self.surface.convert_alpha()
        self.surface.blit(self.img, (0, 0))
        return self.surface

#PARENT CLASS UPDATE------------------------------------------------------------
    def update(self):
        self.a = self.a + 1


#PLAYER SUBCLASS================================================================
class Player(Target):
    """Subclass of target to be controlled by player"""

#PARENT CLASS INIT--------------------------------------------------------------
    def __init__(self, x, y, size, spd, img):
        Target.__init__(self, x, y, size, spd, img)

#PARENT CLASS DRAW--------------------------------------------------------------
    def draw(self):
        return Target.draw(self)

#UPDATE-------------------------------------------------------------------------
    def update(self):
        Target.update(self)
        if pygame.key.get_pressed()[pygame.K_RIGHT]:
            self.rect.x = self.rect.x + self.spd
            self.rect.clamp_ip(screen_rect)
        elif pygame.key.get_pressed()[pygame.K_LEFT]:
            self.rect.x = self.rect.x - self.spd
            self.rect.clamp_ip(screen_rect)
        if pygame.key.get_pressed()[pygame.K_w] and self.a >= 24:
            fprojectiles.append(Laser(self.rect.centerx, self.rect.centery, 5, -5, "assets/Laser.png"))
            fprojectiles_group.add(fprojectiles[len(fprojectiles) - 1])
            self.a = 0


#ENEMY SUBCLASS=================================================================
class Enemy(Target):
    """Computer controlled enemies to be shot by player"""

#PARENT CLASS INIT--------------------------------------------------------------
    def __init__(self, x, y, size, spd, img):
        Target.__init__(self, x, y, size, spd, img)

#PARENT CLASS DRAW--------------------------------------------------------------
    def draw(self):
        return Target.draw(self)

#UPDATE-------------------------------------------------------------------------
    def update(self):
        Target.update(self)
        self.rect.y = self.rect.y + self.spd
        if self.a % 200 == 0:
            eprojectiles.append(Missile(self.rect.centerx, self.rect.centery, 5, 2, "assets/Missile.png"))
            eprojectiles_group.add(eprojectiles[len(eprojectiles) - 1])
            self.a = 0
        elif self.a % 50 == 0:
            eprojectiles.append(Laser(self.rect.centerx, self.rect.centery, 5, 4, "assets/Laser.png"))
            eprojectiles_group.add(eprojectiles[len(eprojectiles) - 1])


#ALLY SUBCLASS==================================================================
class Ally(Target):

#PARENT CLASS INIT--------------------------------------------------------------
    def __init__(self):
        pass



#PROJECTILE AND SUBCLASSES######################################################


#PROJECTILE PARENT CLASS========================================================
class Projectile(pygame.sprite.Sprite):
    """Parent class for all shot projectiles"""

#PROJECTILE INIT----------------------------------------------------------------
    def __init__(self, x, y, size, spd, img):
        pygame.sprite.Sprite.__init__(self)
        self.size = size
        self.spd = spd
        self.img = pygame.image.load(img)
        self.rect = self.img.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        self.mask = pygame.mask.from_surface(self.img)

#PROJECTILE DRAW----------------------------------------------------------------
    def draw(self):
        self.surface = pygame.Surface((self.size, self.size), pygame.SRCALPHA, 32)
        self.surface = self.surface.convert_alpha()
        self.surface.blit(self.img, (0, 0))
        return self.surface

#PROJECTILE UPDATE--------------------------------------------------------------
    def update(self):
        self.rect.y = self.rect.y + self.spd


#LASER SUBCLASS=================================================================
class Laser(Projectile):
    """Subclass of projectile that travels vertically"""

#PARENT CLASS INIT--------------------------------------------------------------
    def __init__(self, x, y, size, spd, img):
        Projectile.__init__(self, x, y, size, spd, img)

#PARENT CLASS DRAW--------------------------------------------------------------
    def draw(self):
        return Projectile.draw(self)

#UPDATE-------------------------------------------------------------------------
    def update(self):
        Projectile.update(self)


#MISSILE SUBCLASS===============================================================
class Missile(Projectile):
    """Subclass of projectile that seeks the player object"""

#PARENT CLASS INIT--------------------------------------------------------------
    def __init__(self, x, y, size, spd, img):
        Projectile.__init__(self, x, y, size, spd, img)

#PARENT CLASS DRAW--------------------------------------------------------------
    def draw(self):
        return Projectile.draw(self)

#UPDATE-------------------------------------------------------------------------
    def update(self):
        Projectile.update(self)
        if self.rect.centerx > player.rect.centerx:
            self.rect.centerx = self.rect.centerx - self.spd
        elif self.rect.centerx < player.rect.centerx:
            self.rect.centerx = self.rect.centerx + self.spd


#class Misc(object):


#DEFINING VARIABLES=============================================================
eprojectiles = []
eprojectiles_group = pygame.sprite.Group()
fprojectiles = []
fprojectiles_group = pygame.sprite.Group()
enemies = []
enemies_group = pygame.sprite.Group()
allies = []
player = Player(230, 300, 20, 5, "assets/Ship.png")
a = 0
b = 200


#MAIN LOOP======================================================================
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

    screen.fill(BLACK)

#DRAWING, UPDATING AND DELETING OBJECTS-----------------------------------------
    for i in eprojectiles:
        screen.blit(i.draw(), (i.rect.x, i.rect.y))
        i.update()
        if i.rect.y > 360:
            eprojectiles.remove(i)
            eprojectiles_group.remove(i)
    for i in fprojectiles:
        screen.blit(i.draw(), (i.rect.x, i.rect.y))
        i.update()
        if i.rect.y < 0:
            fprojectiles.remove(i)
            fprojectiles_group.remove(i)
    screen.blit(player.draw(), (player.rect.x, player.rect.y))
    player.update()
    for i in allies:
        screen.blit(i.draw(), (i.rect.x, i.rect.y))
        i.update()
    for i in enemies:
        screen.blit(i.draw(), (i.rect.x, i.rect.y))
        i.update()
        if i.rect.y > 360:
            enemies.remove(i)
            enemies_group.remove(i)

#SPAWNING ENEMIES---------------------------------------------------------------
    if a % int(b) == 0:
        enemies.append(Enemy(random.randint(0, 460), -20, 20, 1, "assets/Enemy.png"))
        enemies_group.add(enemies[len(enemies) - 1])
        a = 0

#COLLISION DETECTION------------------------------------------------------------
    ef_collide = pygame.sprite.groupcollide(enemies_group, fprojectiles_group, True, True)
    ef_collide_enemies = ef_collide.keys()
    ef_collide_fprojectiles = ef_collide.values()
    for i in ef_collide_enemies:
        enemies.remove(i)
    for i in ef_collide_fprojectiles:
        fprojectiles.remove(i[0])

#LOOP VARIABLES UPDATE----------------------------------------------------------
    a = a + 1
    if b > 48:
        b = b - 0.01
    pygame.display.flip()
    clock.tick(60)


#EXIT GAME LOOP=================================================================
pygame.quit()
