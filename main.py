#This code is unreadable

#INITIALISE=====================================================================
import pygame
import pygame.font
pygame.init()
pygame.mixer.init()
music = pygame.mixer.music.load("assets/space magic.wav")
pygame.mixer.music.play(-1)
pygame.font.init()
font = pygame.font.SysFont('Consolas', 16)
bigfont = pygame.font.SysFont('Consolas', 32)
missile_sound =  pygame.mixer.Sound('assets/missile sound.wav')
laser_sound = pygame.mixer.Sound('assets/laser sound.wav')
explosion = pygame.mixer.Sound('assets/explosion.wav')
thunk = pygame.mixer.Sound('assets/thunk.wav')
zwoop = pygame.mixer.Sound('assets/powerup.wav')
fizzle = pygame.mixer.Sound('assets/fizzle.wav')
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
background = pygame.image.load('assets/background.png')



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
    def __init__(self, x, y, size, spd, img, hp):
        Target.__init__(self, x, y, size, spd, img)
        self.hp = hp
        self.missile_cooldown = 0
        self.ally_cooldown = 0
        self.shield_cooldown = 0
        self.nuke_cooldown = 0

#PARENT CLASS DRAW--------------------------------------------------------------
    def draw(self):
        return Target.draw(self)

#UPDATE-------------------------------------------------------------------------
    def update(self):
        global allies_count, shields_count, nukes_count, missiles_count
        Target.update(self)
        if pygame.key.get_pressed()[pygame.K_RIGHT]:
            self.rect.x = self.rect.x + self.spd
            self.rect.clamp_ip(screen_rect)
        elif pygame.key.get_pressed()[pygame.K_LEFT]:
            self.rect.x = self.rect.x - self.spd
            self.rect.clamp_ip(screen_rect)
        if pygame.key.get_pressed()[pygame.K_w] and self.a >= 24:
            fprojectiles.append(Laser(self.rect.centerx, self.rect.centery, 5, -5, 0, "assets/Laser.png"))
            fprojectiles_group.add(fprojectiles[len(fprojectiles) - 1])
            laser_sound.play()
            self.a = 0
        if pygame.key.get_pressed()[pygame.K_a] and self.missile_cooldown >= 240 and missiles_count > 0:
            if len(enemies) > 0:
                fprojectiles.append(Missile(self.rect.centerx, self.rect.centery, 5, -1, 4, 'assets/Missile.png', enemies[0]))
                fprojectiles_group.add(fprojectiles[len(fprojectiles) - 1])
                missile_sound.play()
                self.missile_cooldown = 0
                missiles_count = missiles_count - 1
        if pygame.key.get_pressed()[pygame.K_s] and self.ally_cooldown >= 240 and allies_count > 0:
            allies.append(Ally(self.rect.x, self.rect.y, 20, -1, 'assets/Ally.png'))
            allies_group.add(allies[len(allies) - 1])
            allies_count = allies_count - 1
            self.ally_cooldown = 0
        if pygame.key.get_pressed()[pygame.K_d] and self.shield_cooldown >= 240 and shields_count > 0:
            shields.append(Shield(self.rect.centerx, self.rect.centery, 40, 0, 'assets/Shield.png'))
            shields_group.add(shields[len(shields) - 1])
            shields_count = shields_count - 1
            self.shield_cooldown = 0
        if pygame.key.get_pressed()[pygame.K_e] and self.nuke_cooldown >= 1440 and nukes_count > 0:
            for i in range(120):
                for j in range(160):
                    fprojectiles.append(Laser(j * 3 + 1, 360 + i * 3, 5, -5, 0, "assets/Laser.png"))
                    fprojectiles_group.add(fprojectiles[len(fprojectiles) - 1])
                    laser_sound.play()
            nukes_count = nukes_count - 1
            self.nuke_cooldown = 0
        self.missile_cooldown = self.missile_cooldown + 1
        self.ally_cooldown = self.ally_cooldown + 1
        self.shield_cooldown = self.shield_cooldown + 1
        self.nuke_cooldown = self.nuke_cooldown + 1


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
        if self.a % 128 == 0:
            eprojectiles.append(Missile(self.rect.centerx, self.rect.centery, 5, 2, 2, "assets/Missile.png", player))
            eprojectiles_group.add(eprojectiles[len(eprojectiles) - 1])
            missile_sound.play()
            if self.a % 64 == 0:
                self.a = 0
        if self.a % 64 == 0:
            eprojectiles.append(Laser(self.rect.centerx, self.rect.centery, 5, 2, 0, "assets/Laser.png"))
            eprojectiles_group.add(eprojectiles[len(eprojectiles) - 1])
            laser_sound.play()

#DIE----------------------------------------------------------------------------
    def die(self):
        self.probability = random.randint(0, 99)
        if self.probability >= 99:
            powerups.append(Powerup(self.rect.centerx, self.rect.centery, 20, 1, 'assets/Bubble Nuke.png', 'nuke'))
            powerups_group.add(powerups[len(powerups) - 1])
        elif self.probability >= 95:
            powerups.append(Powerup(self.rect.centerx, self.rect.centery, 20, 1, 'assets/Bubble Ally.png', 'ally'))
            powerups_group.add(powerups[len(powerups) - 1])
        elif self.probability >= 90:
            powerups.append(Powerup(self.rect.centerx, self.rect.centery, 20, 1, 'assets/Bubble Shield.png', 'shield'))
            powerups_group.add(powerups[len(powerups) - 1])
        elif self.probability >= 75:
            powerups.append(Powerup(self.rect.centerx, self.rect.centery, 20, 1, 'assets/Bubble Heart.png', 'hp'))
            powerups_group.add(powerups[len(powerups) - 1])
        elif self.probability >= 50:
            powerups.append(Powerup(self.rect.centerx, self.rect.centery, 20, 1, 'assets/Bubble Missile.png', 'missile'))
            powerups_group.add(powerups[len(powerups) - 1])


#ALLY SUBCLASS==================================================================
class Ally(Target):
    """Computer controlled allies to help the player shoot enemies"""

#PARENT CLASS INIT--------------------------------------------------------------
    def __init__(self, x, y, size, spd, img):
        Target.__init__(self, x, y, size, spd, img)
        self.a = 23

#PARENT CLASS DRAW--------------------------------------------------------------
    def draw(self):
        return Target.draw(self)

#UPDATE-------------------------------------------------------------------------
    def update(self):
        Target.update(self)
        self.rect.centery = self.rect.centery + self.spd
        if self.a % 24 == 0:
            fprojectiles.append(Laser(self.rect.centerx, self.rect.centery, 5, -2, 2, "assets/Laser.png"))
            fprojectiles_group.add(fprojectiles[len(fprojectiles) - 1])
            fprojectiles.append(Laser(self.rect.centerx, self.rect.centery, 5, -2, -2, "assets/Laser.png"))
            fprojectiles_group.add(fprojectiles[len(fprojectiles) - 1])
            self.a = 0
            laser_sound.play()


#SHIELD SUBCLASS==================================================================
class Shield(Target):
    """Shield that follows player in order to block enemy projectiles"""

#PARENT CLASS INIT--------------------------------------------------------------
    def __init__(self, x, y, size, spd, img):
        Target.__init__(self, x, y, size, spd, img)
        self.rect.centerx = x
        self.rect.centery = y

#PARENT CLASS DRAW--------------------------------------------------------------
    def draw(self):
        return Target.draw(self)

#UPDATE-------------------------------------------------------------------------
    def update(self):
        Target.update(self)
        self.rect.centerx = player.rect.centerx



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
    def __init__(self, x, y, size, spd, dy, img):
        Projectile.__init__(self, x, y, size, spd, img)
        self.dy = dy

#PARENT CLASS DRAW--------------------------------------------------------------
    def draw(self):
        return Projectile.draw(self)

#UPDATE-------------------------------------------------------------------------
    def update(self):
        Projectile.update(self)
        self.rect.centerx = self.rect.centerx + self.dy


#MISSILE SUBCLASS===============================================================
class Missile(Projectile):
    """Subclass of projectile that seeks the player object"""

#PARENT CLASS INIT--------------------------------------------------------------
    def __init__(self, x, y, size, spd, dy, img, target):
        Projectile.__init__(self, x, y, size, spd, img)
        self.dy = dy
        self.target = target

#PARENT CLASS DRAW--------------------------------------------------------------
    def draw(self):
        return Projectile.draw(self)

#UPDATE-------------------------------------------------------------------------
    def update(self):
        Projectile.update(self)
        if self.target != player and len(enemies) > 0:
            self.target = enemies[0]
        if self.rect.centerx - self.dy > self.target.rect.centerx:
            self.rect.centerx = self.rect.centerx - self.dy
        elif self.rect.centerx + self.dy < self.target.rect.centerx:
            self.rect.centerx = self.rect.centerx + self.dy



#POWERUP AND SUBCLASSES#########################################################


#POWERUP PARENT CLASS===========================================================
class Powerup(pygame.sprite.Sprite):
    """Parent class for all powerups"""

#POWERUP INIT-------------------------------------------------------------------
    def __init__(self, x, y, size, spd, img, type):
        pygame.sprite.Sprite.__init__(self)
        self.size = size
        self.img = pygame.image.load(img)
        self.rect = self.img.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        self.mask = pygame.mask.from_surface(self.img)
        self.type = type

#POWERUP DRAW-------------------------------------------------------------------
    def draw(self):
        self.surface = pygame.Surface((self.size, self.size), pygame.SRCALPHA, 32)
        self.surface = self.surface.convert_alpha()
        self.surface.blit(self.img, (0, 0))
        return self.surface

#POWERUP UPDATE-----------------------------------------------------------------
    def update(self):
        self.rect.centery = self.rect.centery + 1

#POWERUP DIE--------------------------------------------------------------------
    def die(self):
        global allies_count, shields_count, score, nukes_count, missiles_count
        if self.type == 'nuke':
            nukes_count = nukes_count + 1
        elif self.type == 'hp':
            player.hp = player.hp + 1
        elif self.type == 'ally':
            allies_count = allies_count + 1
        elif self.type == 'shield':
            shields_count = shields_count + 1
        elif self.type == 'missile':
            missiles_count = missiles_count + 1


#DEFINING VARIABLES=============================================================
eprojectiles = []
eprojectiles_group = pygame.sprite.Group()
fprojectiles = []
fprojectiles_group = pygame.sprite.Group()
enemies = []
enemies_group = pygame.sprite.Group()
allies = []
allies_group = pygame.sprite.Group()
player = Player(230, 300, 20, 4, "assets/Ship.png", 3)
player_group = pygame.sprite.Group()
player_group.add(player)
powerups = []
powerups_group = pygame.sprite.Group()
shields = []
shields_group = pygame.sprite.Group()
a = 0
b = 200
score = 0
allies_count = 0
shields_count = 0
nukes_count = 0
missiles_count = 0


#MAIN LOOP======================================================================
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

    screen.fill(BLACK)
    screen.blit(background, (0, 0))

    if player.hp > 0:
        """Game loop if still alive"""

#DRAWING, UPDATING AND DELETING OBJECTS-----------------------------------------
        for i in powerups:
            screen.blit(i.draw(), (i.rect.x, i.rect.y))
            i.update()
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
        for i in shields:
            screen.blit(i.draw(), (i.rect.x, i.rect.y))
        screen.blit(player.draw(), (player.rect.x, player.rect.y))
        player.update()
        for i in shields:
            i.update()
            if i.a >= 240:
                shields.remove(i)
                shields_group.remove(i)
        for i in allies:
            screen.blit(i.draw(), (i.rect.x, i.rect.y))
            i.update()
            if i.rect.y < 0:
                allies.remove(i)
                allies_group.remove(i)
        for i in enemies:
            screen.blit(i.draw(), (i.rect.x, i.rect.y))
            i.update()
            if i.rect.y > 360:
                enemies.remove(i)
                enemies_group.remove(i)
                score = score - 10

#SPAWNING ENEMIES---------------------------------------------------------------
        if a % int(b) == 0:
            enemies.append(Enemy(random.randint(0, 460), -20, 20, 1, "assets/Enemy.png"))
            enemies_group.add(enemies[len(enemies) - 1])
            a = 0

#COLLISION DETECTION------------------------------------------------------------
        ef_collide = pygame.sprite.groupcollide(enemies_group, fprojectiles_group, True, True, pygame.sprite.collide_mask)
        ef_collide_enemies = ef_collide.keys()
        ef_collide_fprojectiles = ef_collide.values()
        for i in ef_collide_enemies:
            i.die()
            enemies.remove(i)
            score = score + 1
            explosion.play()
        for i in ef_collide_fprojectiles:
            fprojectiles.remove(i[0])
        ea_collide = pygame.sprite.groupcollide(enemies_group, allies_group, True, True, pygame.sprite.collide_mask)
        ea_collide_enemies = ea_collide.keys()
        ea_collide_allies = ea_collide.values()
        for i in ea_collide_enemies:
            i.die()
            enemies.remove(i)
            score = score + 1
            explosion.play()
        for i in ea_collide_allies:
            allies.remove(i[0])
        ae_collide = pygame.sprite.groupcollide(allies_group, eprojectiles_group, True, True, pygame.sprite.collide_mask)
        ae_collide_allies = ae_collide.keys()
        ae_collide_eprojectiles = ae_collide.values()
        for i in ae_collide_allies:
            allies.remove(i)
            explosion.play()
        for i in ae_collide_eprojectiles:
            eprojectiles.remove(i[0])
        es_collide = pygame.sprite.groupcollide(enemies_group, shields_group, True, False, pygame.sprite.collide_mask)
        es_collide_enemies = es_collide.keys()
        for i in es_collide_enemies:
            i.die()
            enemies.remove(i)
            score = score + 1
            explosion.play()
        se_collide = pygame.sprite.groupcollide(shields_group, eprojectiles_group, False, True, pygame.sprite.collide_mask)
        se_collide_eprojectiles = se_collide.values()
        for i in se_collide_eprojectiles:
            eprojectiles.remove(i[0])
            fizzle.play()
        pe_collide = pygame.sprite.groupcollide(player_group, eprojectiles_group, False, True, pygame.sprite.collide_mask)
        pe_collide_eprojectiles = pe_collide.values()
        for i in pe_collide_eprojectiles:
            player.hp = player.hp - 1
            if player.hp == 0:
                explosion.play()
            else:
                thunk.play()
            eprojectiles.remove(i[0])
        ep_collide = pygame.sprite.groupcollide(player_group, enemies_group, False, True, pygame.sprite.collide_mask)
        ep_collide_enemies = ep_collide.values()
        for i in ep_collide_enemies:
            i[0].die()
            player.hp = player.hp - 1
            if player.hp == 0:
                explosion.play()
            else:
                thunk.play()
            enemies.remove(i[0])
            explosion.play()
        pp_collide = pygame.sprite.groupcollide(player_group, powerups_group, False, True, pygame.sprite.collide_mask)
        pp_collide_powerups = pp_collide.values()
        for i in pp_collide_powerups:
            i[0].die()
            powerups.remove(i[0])
            zwoop.play()

#VARIABLES UPDATE---------------------------------------------------------------
        a = a + 1
        if b > 48:
            b = b - 0.01
        screen.blit(font.render('Lives: ' + str(player.hp), False, WHITE), (0, 0))
        screen.blit(font.render('Score: ' + str(score), False, WHITE), (0, 16))
        screen.blit(font.render('Allies: ' + str(allies_count), False, WHITE), (160, 0))
        screen.blit(font.render('Shields: ' + str(shields_count), False, WHITE), (160, 16))
        screen.blit(font.render('Missiles: ' + str(missiles_count), False, WHITE), (320, 0))
        screen.blit(font.render('Nukes: ' + str(nukes_count), False, WHITE), (320, 16))

#GAME OVER----------------------------------------------------------------------
    else:
        screen.blit(bigfont.render('Game Over', False, WHITE), (176, 148))
        screen.blit(font.render('Final score: ' + str(score), False, WHITE), (176, 180))
        if score <= 0:
            screen.blit(font.render('hAhA yOu SuCk', False, WHITE), (176, 196))

#LOOP UPDATE--------------------------------------------------------------------
    pygame.display.flip()
    clock.tick(60)

#EXIT GAME LOOP=================================================================
pygame.quit()
