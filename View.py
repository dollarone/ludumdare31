import math
import pygame
import random
import inspect
from pygame.locals import *
import time

class Building:

    def __init__(self, pos, hp=300, rect=None, image=None, viewModifier=-20, name="Unnamed Building"):
        self.name = name
        self.hp = hp
        self.hpmax = self.hp
        self.status = states.ALIVE
        self.regen = 1
        self.canAttack = False
        self.pos = pos
        self.offsetPos = pos
        self.radius = 10
        self.rect = rect
        self.image = image
        self.viewModifier = viewModifier
        self.armor = 15
        self.xp = 0

    def damage(self, dam):
        self.hp -= dam
        if self.hp <= 0:
            self.status = states.DEAD
            return True
        return False

    def draw(self, scr, col):
        pass

class Tower(Building):

    def __init__(self, pos, rect, image, viewModifier=-20, name="Tower"):
        hp = 1600
        super(Tower, self).__init__(pos, hp, rect, image, viewModifier, name)
        self.canAttack = True
        self.attackRange = 40
        self.readyToAttack = True
        self.maxAttack = 122
        self.minAttack = 182
        self.attackCooldown = 50
        self.currentAttackCooldown = 0
        self.armor = 25
        self.bounty = 280
        self.bountyDenied = 140

    def resetAttackCooldown(self):
        self.readyToAttack = False
        self.currentAttackCooldown = self.attackCooldown

    def attack(self):
        global rand
        return rand.randrange(self.minAttack, self.maxAttack)

    def newTurn(self):
        if self.currentAttackCooldown > 0:
            self.currentAttackCooldown -= 1
        if self.currentAttackCooldown == 0:
            self.readyToAttack = True

    def draw(self, scr, col):
        pygame.draw.circle(scr, col, (self.pos[0] + 12, self.pos[1] + 12), self.attackRange, 1)


class Lvl1Tower(Tower):

    def __init__(self, pos, rect, image, viewModifier=-20, name="Lvl 1 Tower"):
        super(Lvl1Tower, self).__init__(pos, rect, image, viewModifier, name)
        self.hp = 1300
        self.hpmax = self.hp
        self.armor = 20
        self.maxAttack = 120
        self.minAttack = 100
        self.attackCooldown = 60
        self.bounty = 160
        self.bountyDenied = 80

class Lvl2Tower(Tower):

    def __init__(self, pos, rect, image, viewModifier=-20, name="Lvl 2 Tower"):
        super(Lvl2Tower, self).__init__(pos, rect, image, viewModifier, name)
        self.hp = 1600
        self.hpmax = self.hp
        self.armor = 25
        self.maxAttack = 140
        self.minAttack = 120
        self.attackCooldown = 57 # BAT = 0.95
        self.bounty = 200
        self.bountyDenied = 100

class Lvl3Tower(Tower):

    def __init__(self, pos, rect, image, viewModifier=-20, name="Lvl 3 Tower"):
        super(Lvl3Tower, self).__init__(pos, rect, image, viewModifier, name)
        self.hp = 1600
        self.hpmax = self.hp
        self.armor = 25
        self.maxAttack = 182
        self.minAttack = 122
        self.attackCooldown = 57
        self.bounty = 240
        self.bountyDenied = 120

class Lvl4Tower(Tower):

    def __init__(self, pos, rect, image, viewModifier=-20, name="Lvl 4 Tower"):
        super(Lvl4Tower, self).__init__(pos, rect, image, viewModifier, name)
        self.hp = 1600
        self.hpmax = self.hp
        self.armor = 30
        self.maxAttack = 182
        self.minAttack = 122
        self.attackCooldown = 57
        self.bounty = 280
        self.bountyDenied = 140



class Ancient(Building):

    def __init__(self, pos, rect, image, viewModifier=-20, name="Ancient"):
        hp = 4250
        super(Ancient, self).__init__(pos, hp, rect, image, viewModifier, name)
        self.radius = 100
        self.regen = 3

class Unit:
    def __init__(self, path=[], rect=None, image=None, name="Unknown"):
        global rand
        self.name = name
        self.path = path
        self.rect = rect
        self.hp = 300
        self.hpmax = self.hp
        self.maxAttack = 23
        self.minAttack = 19
        self.pathPos = 0
        if len(path) > 0:
            self.pos = path[0]
        else:
            self.pos = None
        self.prevPos = self.pos #used for checking if the creep is stuck
        self.offsetPos = self.pos
        self.attackRange = 10
        self.readyToAttack = True
        self.attackCooldown = 60
        self.currentAttackCooldown = 0
        self.radius = 10
        self.randomDirection = rand.sample([-1,1],1)[0]
        self.paused = False
        self.standingStillCounter = 0
        self.image = image
        self.viewModifier = 0
        self.status = states.ALIVE
        self.offset = 0
        self.armor = 2
        self.xp = 0
        self.xp_range = 50
        self.xp_bounty = 20

    def resetAttackCooldown(self):
        self.readyToAttack = False
        self.currentAttackCooldown = self.attackCooldown

    def newTurn(self):
        if self.status == states.ALIVE:
            if self.currentAttackCooldown > 0:
                self.currentAttackCooldown -= 1
            if self.currentAttackCooldown == 0:
                self.readyToAttack = True
            # find out where the creep is heading
            if len(self.path) > 0:
                prevPathPos = self.path[self.pathPos-1]
                targetPathPos = prevPathPos
                if len(self.path) > self.pathPos:
                    targetPathPos = self.path[self.pathPos]
            else:
                prevPathPos = self.path[self.pathPos]
                targetPathPos = self.path[self.pathPos+1]
            targetx = targetPathPos[0] - prevPathPos[0]
            targety = targetPathPos[1] - prevPathPos[1]
            if targetx != 0:
                self.offsetPos = (self.pos[0], self.pos[1] + self.offset)
            if targety != 0:
                self.offsetPos = (self.pos[0] + self.offset, self.pos[1])

    def move(self):
        #print("len(self.path):" + str(len(self.path)) + " self.pathPos + 1: " + str(self.pathPos + 1))

        if len(self.path) > self.pathPos:
            #print("self.pos[0]: " + str(self.pos[0]) + " self.path[self.pathPos + 1][0]: " + str(self.path[self.pathPos][0]))
            #print("self.pos[1]: " + str(self.pos[1]) + " self.path[self.pathPos + 1][1]: " + str(self.path[self.pathPos][1]))
            if self.pos[0] == self.path[self.pathPos][0] and self.pos[1] == self.path[self.pathPos][1]:
                self.pathPos += 1
                #print("self.pathPos += 1 - new val: " + str(self.pathPos))
        if len(self.path) > self.pathPos:
            movex = 0
            movey = 0
            #print(" PATH: " + str(self.pos[0]) + " " + str(self.path[self.pathPos][0]))
            #print(" PATH: " + str(self.pos[1]) + " " + str(self.path[self.pathPos][1]))

            if self.pos[0] > self.path[self.pathPos][0]:
                #print("movex = -1")
                movex = -1
            elif self.pos[0] < self.path[self.pathPos][0]:
                #print("movex = 1")
                movex = 1
            if self.pos[1] > self.path[self.pathPos][1]:
                #print("movey = -1")
                movey = -1
            elif self.pos[1] < self.path[self.pathPos][1]:
                #print("movey = 1")
                movey = 1

            self.pos = (self.pos[0] + movex, self.pos[1] + movey)
            #print(str(self.pos) + " " + str(movex) + " " + str(movey))

    def damage(self, dam):
        self.hp -= dam
        if self.hp <= 0:
            self.status = states.DEAD
            return True
        return False

    def attack(self):
#        global rand
        return rand.randrange(self.minAttack, self.maxAttack)

class Hero(Unit):
    def __init__(self, path=[], rect=None, image=None, name="Unknown"):
        super(Hero, self).__init__(path, rect, image, name)
        self.status = states.QUEUING
        self.respawn_timer = 110
        self.faction = "Unknown"
        self.level = 1

    def draw(self, scr, col, hero_number, faction, gradient):
        if self.status == states.ALIVE:
            scr.blit(self.image, self.offsetPos)
            pygame.draw.rect(scr, black, (self.offsetPos[0] - 1 - self.hpmax / 40, self.offsetPos[1] - self.radius +
                                          self.viewModifier, self.hpmax / 15 + 3, 8), 0)

            if self.hp > 0:
                pygame.draw.rect(scr, colours[self.faction][hero_number], (self.offsetPos[0] + 1 - self.hpmax / 40, self.offsetPos[1] - self.radius + 1 +  #+ #1*c.viewModifier, c.hp/15, 6), 0)
                                        self.viewModifier, self.hp / 15, 6), 0)

            pygame.draw.circle(scr, col, (self.pos[0] + 12, self.pos[1] + 12), self.attackRange, 1)
            #circle(Surface, color, pos, radius, width=0

        if self.status == states.QUEUING:
            self.drawPortrait(scr, self, faction, hero_number, gradient)
        elif self.status == states.DEAD:
            self.drawPortrait(scr, self, faction, hero_number)
        elif self.status == states.ALIVE:
            self.drawPortrait(scr, self, faction, hero_number)

    def drawPortrait(self, screen, hero, side, hero_number, alphaMod=128):
        if self.status == states.ALIVE:
            self.profile.set_alpha(255)
            tmp = self.profile
        elif self.status == states.QUEUING:
            self.profile.set_alpha(150 + alphaMod)
            tmp = self.profile
        elif hero.status == states.DEAD:
            tmp = self.get_alpha_surface(self.profile, 80, 255, 128, 128, pygame.BLEND_RGBA_MULT)

        x = 1
        if self.faction == factions.DIRE:
            x = 1040
            tmp = pygame.transform.flip(tmp, True, False)

        #pygame.draw.rect(screen, colours[self.faction][hero_number], (x, hero_number * 144, 240, 144), 0)
        screen.blit(tmp, (x + 1, hero_number * 144 + 1), Rect(1, 1, 238, 142)) #256, 144
#        pygame.draw.rect(screen, darkBlue, (x, hero_number * 144, 240, 144), 0)

        #pygame.draw.rect(scr, black, (c.offsetPos[0] - 1 - c.hpmax/40, c.offsetPos[1] - c.radius + 1*c.viewModifier, c.hpmax/15 + 3, 8), 0)

    def get_alpha_surface(self, surf, alpha=128, red=128, green=128, blue=128, mode=pygame.BLEND_RGBA_MULT):
        """
        Allocate a new surface with user-defined values (0-255)
        for red, green, blue and alpha.

        Thanks to Claudio Canepa <ccanepacc@gmail.com>.
        """

        tmp = pygame.Surface( surf.get_size(), pygame.SRCALPHA, 32)
        tmp.fill( (red,green,blue,alpha) )
        tmp.blit(surf, (0,0), surf.get_rect(), mode)
        return tmp


    def damage(self, dam):
        self.hp -= dam
        if self.hp <= 0:
            self.status = states.DEAD
            self.respawn_timer = 50 + self.level * 15 # TODO: move to game settings
            print(self.name + " dedd")
            return True
        return False

    def newTurn(self):
        super(Hero, self).newTurn()

        #print(self.name + " " + str(self.status))

        if self.respawn_timer <= 0 and self.status == states.DEAD:
            self.reset()
            print(self.name + " back in the queue!")
        if self.status == states.DEAD:
            self.respawn_timer -= 1
            #print(self.name + " " + str(self.respawn_timer))


    def reset(self):
        self.status = states.QUEUING

    def spawnHero(self, lane):
        self.status = states.ALIVE
        self.hp = self.hpmax
        self.path = lane
        self.pos = self.path[0]
#        self.offset = 2 * self.randomDirection
        self.prevPos = self.pos
        self.offsetPos = self.pos
        self.pathPos = 0

        self.readyToAttack = True
        self.attackCooldown = 60
        self.currentAttackCooldown = 0
        self.paused = False

        self.standingStillCounter = 0

        self.viewModifier = 0

        self.offset = 0
        self.armor = 2




class Ursa(Hero):
    hero_image = pygame.image.load("ursa.png")
    hero_image.set_colorkey(( 255, 255, 255))
    hero_image_rect = hero_image.get_rect()

    hero_profile = pygame.image.load("ursa_profile.png")
    hero_profile_rect = hero_image.get_rect()

    def __init__(self, path=[], rect=None, image=None, name="Ursa"):
        super(Ursa, self).__init__(path, rect, image, name)
        self.attackRange = 20
        self.hp = 587
        self.hpmax = 587
        self.image = Ursa.hero_image.convert()
        self.rect = Ursa.hero_image_rect
        self.profile = Ursa.hero_profile.convert()
        self.profile_rect = Ursa.hero_profile_rect
        self.maxAttack = 49
        self.minAttack = 45
        self.armor = 5.52
        self.attackCooldown = 102 # 1.7 BAT


class Sven(Hero):
    hero_image = pygame.image.load("sven.png")
    hero_image.set_colorkey(( 255, 255, 255))
    hero_image_rect = hero_image.get_rect()

    hero_profile = pygame.image.load("sven_profile.png")
    hero_profile_rect = hero_image.get_rect()

    def __init__(self, path=[], rect=None, image=None, name="Sven"):
        super(Sven, self).__init__(path, rect, image, name)
        self.attackRange = 20
        self.hp = 587
        self.hpmax = 587
        self.image = Sven.hero_image.convert()
        self.rect = Sven.hero_image_rect
        self.profile = Sven.hero_profile.convert()
        self.profile_rect = Sven.hero_profile_rect
        self.maxAttack = 49
        self.minAttack = 45
        self.armor = 5.52
        self.attackCooldown = 102 # 1.7 BAT


class Wraith_King(Hero):
    hero_image = pygame.image.load("wraith_king.png")
    hero_image.set_colorkey(( 255, 255, 255))
    hero_image_rect = hero_image.get_rect()

    hero_profile = pygame.image.load("wraith_king_profile.png")
    hero_profile_rect = hero_image.get_rect()

    def __init__(self, path=[], rect=None, image=None, name="Wraith King"):
        super(Wraith_King, self).__init__(path, rect, image, name)
        self.attackRange = 20
        self.hp = 587
        self.hpmax = 587
        self.image = Wraith_King.hero_image.convert()
        self.rect = Wraith_King.hero_image_rect
        self.profile = Wraith_King.hero_profile.convert()
        self.profile_rect = Wraith_King.hero_profile_rect
        self.maxAttack = 49
        self.minAttack = 45
        self.armor = 5.52
        self.attackCooldown = 102 # 1.7 BAT


class Tidehunter(Hero):
    hero_image = pygame.image.load("tidehunter.png")
    hero_image.set_colorkey(( 255, 255, 255))
    hero_image_rect = hero_image.get_rect()

    hero_profile = pygame.image.load("tidehunter_profile.png")
    hero_profile_rect = hero_image.get_rect()

    def __init__(self, path=[], rect=None, image=None, name="Tidehunter"):
        super(Tidehunter, self).__init__(path, rect, image, name)
        self.attackRange = 20
        self.hp = 587
        self.hpmax = 587
        self.image = Tidehunter.hero_image.convert()
        self.rect = Tidehunter.hero_image_rect
        self.profile = Tidehunter.hero_profile.convert()
        self.profile_rect = Tidehunter.hero_profile_rect
        self.maxAttack = 49
        self.minAttack = 45
        self.armor = 5.52
        self.attackCooldown = 102 # 1.7 BAT


class Furion(Hero):
    hero_image = pygame.image.load("furion.png")
    hero_image.set_colorkey(( 255, 255, 255))
    hero_image_rect = hero_image.get_rect()

    hero_profile = pygame.image.load("furion_profile.png")
    hero_profile_rect = hero_image.get_rect()

    def __init__(self, path=[], rect=None, image=None, name="Furion"):
        super(Furion, self).__init__(path, rect, image, name)
        self.attackRange = 20
        self.hp = 587
        self.hpmax = 587
        self.image = Furion.hero_image.convert()
        self.rect = Furion.hero_image_rect
        self.profile = Furion.hero_profile.convert()
        self.profile_rect = Furion.hero_profile_rect
        self.maxAttack = 49
        self.minAttack = 45
        self.armor = 5.52
        self.attackCooldown = 102 # 1.7 BAT


class Sandking(Hero):
    hero_image = pygame.image.load("sandking.png")
    hero_image.set_colorkey(( 255, 255, 255))
    hero_image_rect = hero_image.get_rect()

    hero_profile = pygame.image.load("sandking_profile.png")
    hero_profile_rect = hero_image.get_rect()

    def __init__(self, path=[], rect=None, image=None, name="Sand King"):
        super(Sandking, self).__init__(path, rect, image, name)
        self.attackRange = 20
        self.hp = 587
        self.hpmax = 587
        self.image = Sandking.hero_image.convert()
        self.rect = Sandking.hero_image_rect
        self.profile = Sandking.hero_profile.convert()
        self.profile_rect = Sandking.hero_profile_rect
        self.maxAttack = 49
        self.minAttack = 45
        self.armor = 5.52
        self.attackCooldown = 102 # 1.7 BAT

class OgreMagi(Hero):
    hero_image = pygame.image.load("ogremagi.png")
    hero_image.set_colorkey(( 255, 255, 255))
    hero_image_rect = hero_image.get_rect()

    hero_profile = pygame.image.load("ogre_magi_profile.png")
    hero_profile_rect = hero_image.get_rect()

    def __init__(self, path=[], rect=None, image=None, name="Ogre Magi"):
        super(OgreMagi, self).__init__(path, rect, image, name)
        self.attackRange = 20
        self.hp = 587
        self.hpmax = 587
        self.image = OgreMagi.hero_image.convert()
        self.rect = OgreMagi.hero_image_rect
        self.profile = OgreMagi.hero_profile.convert()
        self.profile_rect = OgreMagi.hero_profile_rect
        self.maxAttack = 49
        self.minAttack = 45
        self.armor = 5.52
        self.attackCooldown = 102 # 1.7 BAT

class Warlock(Hero):
    hero_image = pygame.image.load("warlock.png")
    hero_image.set_colorkey(( 255, 255, 255))
    hero_image_rect = hero_image.get_rect()

    hero_profile = pygame.image.load("warlock_profile.png")
    hero_profile_rect = hero_image.get_rect()

    def __init__(self, path=[], rect=None, image=None, name="Warlock"):
        super(Warlock, self).__init__(path, rect, image, name)
        self.attackRange = 20
        self.hp = 587
        self.hpmax = 587
        self.image = Warlock.hero_image.convert()
        self.rect = Warlock.hero_image_rect
        self.profile = Warlock.hero_profile.convert()
        self.profile_rect = Warlock.hero_profile_rect
        self.maxAttack = 49
        self.minAttack = 45
        self.armor = 5.52
        self.attackCooldown = 102 # 1.7 BAT

class Zeus(Hero):
    hero_image = pygame.image.load("zeus.png")
    hero_image.set_colorkey(( 255, 255, 255))
    hero_image_rect = hero_image.get_rect()

    hero_profile = pygame.image.load("zeus_profile.png")
    hero_profile_rect = hero_image.get_rect()

    def __init__(self, path=[], rect=None, image=None, name="Zeus"):
        super(Zeus, self).__init__(path, rect, image, name)
        self.attackRange = 20
        self.hp = 587
        self.hpmax = 587
        self.image = Zeus.hero_image.convert()
        self.rect = Zeus.hero_image_rect
        self.profile = Zeus.hero_profile.convert()
        self.profile_rect = Zeus.hero_profile_rect
        self.maxAttack = 49
        self.minAttack = 45
        self.armor = 5.52
        self.attackCooldown = 102 # 1.7 BAT

class WitchDoctor(Hero):
    hero_image = pygame.image.load("witch_doctor.png")
    hero_image.set_colorkey(( 255, 255, 255))
    hero_image_rect = hero_image.get_rect()

    hero_profile = pygame.image.load("witch_doctor_profile.png")
    hero_profile_rect = hero_image.get_rect()

    def __init__(self, path=[], rect=None, image=None, name="Witch Doctor"):
        super(WitchDoctor, self).__init__(path, rect, image, name)
        self.attackRange = 20
        self.hp = 587
        self.hpmax = 587
        self.image = WitchDoctor.hero_image.convert()
        self.rect = WitchDoctor.hero_image_rect
        self.profile = WitchDoctor.hero_profile.convert()
        self.profile_rect = WitchDoctor.hero_profile_rect
        self.maxAttack = 49
        self.minAttack = 45
        self.armor = 5.52
        self.attackCooldown = 102 # 1.7 BAT


class Creep(Unit):
    def __init__(self, path=[], rect=None, image=None, name="Unknown"):
        super(Creep, self).__init__(path, rect, image, name)

    def draw(self, scr, col):
        pygame.draw.circle(scr, col, (self.pos[0] + 12, self.pos[1] + 12), self.attackRange, 1)



class MeleeCreep(Creep):

    melee_image = pygame.image.load("meleecreep.png")    # didn't convert. is that bad?'
    melee_image.set_colorkey(( 255, 255, 255))
    melee_image_rect = melee_image.get_rect()

    def __init__(self, path, rect=None, image=None):
        super(MeleeCreep, self).__init__(path, rect, image, "Melee Creep")
        self.hp = 550
        self.hpmax = 550
        self.image = MeleeCreep.melee_image.convert()
        self.rect = MeleeCreep.melee_image_rect

class RangedCreep(Creep):
    ranged_image = pygame.image.load("rangedcreep2.png")
    ranged_image.set_colorkey((255, 255, 255))
    ranged_image_rect = ranged_image.get_rect()

    def __init__(self, path, rect=None, image=None):
        super(RangedCreep, self).__init__(path, rect, image, "Ranged Creep")
        self.attackRange = 30
        self.hp = 300
        self.image = RangedCreep.ranged_image.convert()
        self.rect = RangedCreep.ranged_image_rect
        self.maxAttack = 26
        self.minAttack = 21
        self.armor = 0



def enum(**enums):
    return type('Enum', (), enums)

class BasicAI:
    def __init__(self, cgi):
        #self.heroes = heroes
        self.cgi = cgi
        self.player_code = "not yet set"
        self.counter = 0

    def tick(self):
        #print("AI will try to spawn hero in mid with access code " + self.player_code)
        #for h in heroes:
        #    if h.status == states.QUEUING:
        if self.counter % 100 == 0:
            try:
                r = rand.randrange(1, 3) # not working
                r = self.counter % 3 + 1
                if r == 1:
                    self.cgi.press(self.player_code, keys.SPAWN_HERO_IN_TOP_LANE)
                elif r == 2:
                    self.cgi.press(self.player_code, keys.SPAWN_HERO_IN_MID_LANE)
                elif r == 3:
                    self.cgi.press(self.player_code, keys.SPAWN_HERO_IN_BOT_LANE)
            except InvalidPlayerCodeError as e:
                print(str(e))
        self.counter += 1

class CGI:

    def __init__(self, view):
        global keys
        keys = enum(SPAWN_HERO_IN_TOP_LANE=1, SPAWN_HERO_IN_MID_LANE=2, SPAWN_HERO_IN_BOT_LANE=3)
        self.view = view
        self.radiant_player_registered = False
        self.dire_player_registered = False
        self.radiant_player_code = " "
        self.dire_player_code = " "
        self.radiant_heroes_set = False
        self.dire_heroes_set = False


    def register(self, faction, name="anon", callback=None):
        if faction == factions.RADIANT:
            if self.radiant_player_registered:
                raise FactionTakenError("Another player has already claimed " + faction)
            else:
                self.radiant= name
                self.radiant_player_registered = True
                self.radiant_player_code = "1b"  #token_generator.generate()
                self.radiant_callback = callback
                return self.radiant_player_code

        if faction == factions.DIRE:
            if self.dire_player_registered:
                raise FactionTakenError("Another player has already claimed " + faction)
            else:
                self.dire = name
                self.dire_player_registered = True
                self.dire_player_code = "1e" # token_generator.generate()
                self.dire_callback = callback
                return self.dire_player_code

    def set_heroes(self, player_code, heroes):
        if player_code == self.radiant_player_code:
            self.radiant_heroes = heroes
            self.radiant_heroes_set = True

        elif player_code == self.dire_player_code:
            self.dire_heroes = heroes
            self.dire_heroes_set = True

    def ready_to_play(self):
        return self.radiant_player_registered and self.dire_player_registered and self.radiant_heroes_set and self.dire_heroes_set

    def press(self, player_code, key):
        if player_code == self.radiant_player_code:
            self.spawn_hero(player_code, key)
        elif player_code == self.dire_player_code:
            self.spawn_hero(player_code, key)
        else:
            raise InvalidPlayerCodeError("Fail: " + str(player_code))

    def spawn_hero(self, player_code, key):
        if player_code == self.radiant_player_code:
            for h in self.view.radiantHeroes:
                if h.status == states.QUEUING:
                    if key == keys.SPAWN_HERO_IN_TOP_LANE:
                        h.spawnHero(self.view.radiantHardLane)
                        break
                    elif key == keys.SPAWN_HERO_IN_MID_LANE:
                        h.spawnHero(self.view.radiantMidLane)
                        break
                    elif key == keys.SPAWN_HERO_IN_BOT_LANE:
                        h.spawnHero(self.view.radiantEasyLane)
                        break
        if player_code == self.dire_player_code:
            for h in self.view.direHeroes:
                if h.status == states.QUEUING:
                    if key == keys.SPAWN_HERO_IN_TOP_LANE:
                        h.spawnHero(self.view.direEasyLane)
                        break
                    elif key == keys.SPAWN_HERO_IN_MID_LANE:
                        h.spawnHero(self.view.direMidLane)
                        break
                    elif key == keys.SPAWN_HERO_IN_BOT_LANE:
                        h.spawnHero(self.view.direHardLane)
                        break

    def tick(self):
        if self.radiant_callback != None:
            self.radiant_callback()

        if self.dire_callback != None:
            self.dire_callback()

class InvalidPlayerCodeError(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

class FactionTakenError(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

class Colours:
    global red, green, blue, darkBlue, white, black, pink, mygreen, radiant_1, radiant_2, radiant_3

    # some colours might be useful
    orange = (255,153,0)
    red = (255,0,0)
    green = (0,255,0)
    blue = (0,0,255)
    darkBlue = (0,0,128)
    white = (255,255,255)
    black = (0,0,0)
    pink = (155,100,100)
    mygreen = (0, 135, 0)

    radiant_1 = (46, 106, 230)
    radiant_2 = (93, 230, 173)
    radiant_3 = (173, 0, 173)
    radiant_4 = (220, 217, 10)
    radiant_5 = (220, 98, 0)

    dire_1 = (230, 122, 176)
    dire_2 = (146, 164, 64)
    dire_3 = (92, 197, 224)
    dire_4 = (0, 119, 31)
    dire_5 = (149, 96, 0)



class View:

    def __init__(self):
        global font, rand, creepNo, states, factions, colours
        states = enum(QUEUING=1, ALIVE=2, DEAD=3)
        factions = enum(RADIANT=1, DIRE=2)
        colours = {}
        colours[factions.RADIANT] = {}
        colours[factions.RADIANT][0] = (46, 106, 230)
        colours[factions.RADIANT][1] = (93, 230, 173)
        colours[factions.RADIANT][2] = (173, 0, 173)
        colours[factions.RADIANT][3] = (220, 217, 10)
        colours[factions.RADIANT][4] = (220, 98, 0)
        colours[factions.DIRE] = {}
        colours[factions.DIRE][0] = (230, 122, 176)
        colours[factions.DIRE][1] = (146, 164, 64)
        colours[factions.DIRE][2] = (92, 197, 224)
        colours[factions.DIRE][3] = (0, 119, 31)
        colours[factions.DIRE][4] = (149, 96, 0)
        colours[factions.RADIANT]["faction"] = (0, 255, 0)
        colours[factions.DIRE]["faction"] = (255, 0, 0)

        pygame.init()
        font = pygame.font.SysFont('Arial', 16)
        rand = random.Random()
        rand.seed(2)
        creepNo = 1
        self.cgi = CGI(self)

    def addHumanPlayer(self, faction):
        try:
            self.player1_code = self.cgi.register(faction, "Player 1")
        except FactionTakenError as e:
            print(str(e))

    def addAI(self, faction, ai):
        try:
            ai.player_code = self.cgi.register(faction, "Player 2", ai.tick)
        except FactionTakenError as e:
            print(str(e))


    def addRect(self, scr, col, pos, size):
        pygame.draw.rect(scr, col, (pos[0], pos[1], size[0], size[1]), 1)

    def addText(self, scr, col, pos, text):
        global font
        scr.blit(font.render(str(text), True, col), pos)

    def drawLane(self, scr, lane, towers):
        global red, darkBlue, font
        n = 1
        for i in lane:
            if n in towers:
                #print("Tower at " + str(i[0]) + "," + str(i[1]))
                self.addRect(scr, darkBlue, i, (20, 20))
                self.addText(scr, darkBlue, i, n)
            else:
                self.addRect(scr, red, i, (20, 20))
                self.addText(scr, red, i, n)
            n += 1

    def drawHpBar(self, scr, c, col):
        #global green, black
        pygame.draw.rect(scr, black, (c.offsetPos[0] - 1 - c.hpmax/40, c.offsetPos[1] - c.radius + 1*c.viewModifier, c.hpmax/15 + 3, 8), 0)

        if c.hp > 0:
            pygame.draw.rect(scr, col, (c.offsetPos[0] + 1 - c.hpmax/40, c.offsetPos[1] - c.radius + 1 + 1*c.viewModifier, c.hp/15, 6), 0)

    def generateRadiantBuildings(self):
        radiantAncientImage = pygame.image.load("ancient.png").convert()
        radiantTowerImage = pygame.image.load("redtower.png").convert()
        radiantTowerImage.set_colorkey((255,255,255))
        radiantTowerImageRect = radiantTowerImage.get_rect()
        radiantAncientImage.set_colorkey((255,255,255))
        radiantAncientImageRect = radiantAncientImage.get_rect()

        buildings = []
        buildings.append(Ancient((300, 660), radiantAncientImageRect, radiantAncientImage, 150, "Radiant Ancient"))
        #easy
        buildings.append(Lvl4Tower((320, 640), radiantTowerImageRect, radiantTowerImage)) #lvl4
        buildings.append(Lvl3Tower((320, 540), radiantTowerImageRect, radiantTowerImage))
        buildings.append(Lvl2Tower((320, 420), radiantTowerImageRect, radiantTowerImage))
        buildings.append(Lvl1Tower((320, 280), radiantTowerImageRect, radiantTowerImage))
        #mid:
        buildings.append(Lvl4Tower((340, 640), radiantTowerImageRect, radiantTowerImage, -10))
        buildings.append(Lvl3Tower((420, 560), radiantTowerImageRect, radiantTowerImage))
        buildings.append(Lvl2Tower((500, 480), radiantTowerImageRect, radiantTowerImage))
        buildings.append(Lvl1Tower((580, 400), radiantTowerImageRect, radiantTowerImage))
        #hard:
        buildings.append(Lvl4Tower((340, 660), radiantTowerImageRect, radiantTowerImage))
        buildings.append(Lvl3Tower((440, 660), radiantTowerImageRect, radiantTowerImage))
        buildings.append(Lvl2Tower((560, 660), radiantTowerImageRect, radiantTowerImage))
        buildings.append(Lvl1Tower((800, 660), radiantTowerImageRect, radiantTowerImage))
        return buildings

    def generateDireBuildings(self):
        direAncientImage = pygame.image.load("ancient.png").convert()
        direTowerImage = pygame.image.load("redtower.png").convert()
        direTowerImage.set_colorkey((255,255,255))
        direTowerImageRect = direTowerImage.get_rect()
        direAncientImage.set_colorkey((255,255,255))
        direAncientImageRect = direAncientImage.get_rect()

        buildings = []
        buildings.append(Ancient((940, 20), direAncientImageRect, direAncientImage, 80, "Dire Ancient"))
        #easy:
        buildings.append(Lvl4Tower((920, 40), direTowerImageRect, direTowerImage)) #lvl4
        buildings.append(Lvl3Tower((820, 40), direTowerImageRect, direTowerImage))
        buildings.append(Lvl2Tower((700, 40), direTowerImageRect, direTowerImage))
        buildings.append(Lvl1Tower((460, 40), direTowerImageRect, direTowerImage))
        #mid:
        buildings.append(Lvl4Tower((920, 60), direTowerImageRect, direTowerImage, -10))
        buildings.append(Lvl3Tower((840, 140), direTowerImageRect, direTowerImage))
        buildings.append(Lvl2Tower((760, 220), direTowerImageRect, direTowerImage))
        buildings.append(Lvl1Tower((680, 300), direTowerImageRect, direTowerImage))
        #hard:
        buildings.append(Lvl4Tower((940, 60), direTowerImageRect, direTowerImage))
        buildings.append(Lvl3Tower((940, 160), direTowerImageRect, direTowerImage))
        buildings.append(Lvl2Tower((940, 280), direTowerImageRect, direTowerImage))
        buildings.append(Lvl1Tower((940, 420), direTowerImageRect, direTowerImage))
        return buildings

    def generateHeroes(self, heroes):
        heroes.add(Ursa())
        heroes.add(Sven())
        heroes.add(Tidehunter())
        heroes.add(Sandking())
        heroes.add(Wraith_King())
        heroes.add(Furion())
        heroes.add(OgreMagi())
        heroes.add(Warlock())
        heroes.add(Zeus())
        heroes.add(WitchDoctor())

    def randomlyPickHeroes(self, available, heroes, faction):
        #raondom TODO heroes.append([available].remove(rand.randrange(0,len(available))))
        for i in range(0, 5):
            #randomHero = rand.randrange(1, len(available))
            hero = available.pop()
            hero.faction = faction
            heroes.append(hero)
            print(hero.name + " " + str(hero.faction))


    def dist(self, p, q):
        #print(p)
        #print(q)
        return math.sqrt((p[0] - q[0]) ** 2+(p[1] - q[1]) ** 2)

    def inRange(self, creep, targets):
        for t in targets:
            if t.status == states.ALIVE:
                #print(str(t.status))
                if self.dist(creep.pos, t.pos) <= creep.attackRange:
                    if self.attack(creep, t):
                        creep.xp += t.xp_bounty

                    if t.status == states.DEAD and not issubclass(t.__class__, Hero): ## YURGH
                        targets.remove(t)
                    return True
        return False

    def buildingsInRange(self, creep, buildings):
        for b in buildings:
            if b.status == states.ALIVE:
               if self.dist(creep.pos, b.pos) <= creep.attackRange:
                    if self.attack(creep, b):
                        creep.xp += b.xp_bounty
                    return True
        return False

    def attack(self, source, dest):
        # TODO: armor etc
        #armor: dmd reduction = ((0.06*armor) - (1 + 0.06 * armor))
        dmgReduction = ((0.06 * dest.armor) / (1 + 0.06 * dest.armor))


        if source.readyToAttack:
            source.resetAttackCooldown()
            #print(str(source) + " " + str(source.currentAttackCooldown))
            atk = source.attack()
            dmg = atk * (1-dmgReduction)
#            return dest.damage(dmg)

            print(str(pygame.time.get_ticks() / 1000) + ": " + str(source.name) +
            " hitting " + str(atk) + " on " + str(dest.name) + "(with armor " +
            str(dest.armor) + ") means dmg reduction of " + str(dmgReduction) +
            " == damage dealt: " + str(dmg) + " health remaining before dmg: " + str(dest.hp))

            return dest.damage(dmg)
        return False

    def collision(self, creep, pos, direCreeps, radiantCreeps):
        return False

        # NO COLLISION DETECTION IN USE, BECAUSE, WHY NOT?
        for c in direCreeps:
            if id(c) != id(creep):
                if self.dist(pos, c.pos) <= c.radius:
                    #print("pos: " + str(pos) + " is " + str(self.dist(pos, c.pos)) + " from " + str(c.pos))
                    return True
        for c in radiantCreeps:
            if id(c) != id(creep):
                if self.dist(pos, c.pos) <= c.radius:
                    #print("pos: " + str(pos) + " is " + str(self.dist(pos, c.pos)) + " from " + str(c.pos))
                    return True
        return False

    def standOrRand(self, c, pos):
        global rand
        foo = rand.randrange(10)
        if foo == 0:
            return (pos[0] + c.randomDirection, pos[1])
        elif foo == 1:
            return (pos[0], pos[1] + c.randomDirection)
        elif foo == 2:
            return (pos[0] + c.randomDirection, pos[1] + c.randomDirection)
        #elif foo == 2:
        #    return (pos[0] + rand.sample([-1,1],1)[0], pos[1] + rand.sample([-1,0,1],1)[0])
        #elif foo == 3:
        #    return (pos[0] + rand.sample([-1,0,1],1)[0], pos[1] + rand.sample([-1,1],1)[0])
        else:
            return pos

    def spawnCreep(self, group, lane, spawningNo):
        global creepNo
        creep = None
        if spawningNo == 1:
            creep = RangedCreep(lane)
            creep.name = "RangedCreep no " + str(creepNo)
        else:
            creep = MeleeCreep(lane)
            creep.name = "MeleeCreep no " + str(creepNo)
        creep.offset = 2 * spawningNo * creep.randomDirection
        if spawningNo == 5:
            creep.offset = 0
        group.append(creep)
        creepNo += 1

        #                        radiantCreeps.append(RangedCreep(radiantHardLane, rangedimagerect, rangedimage))

    def start(self):
        global red, green, blue, darkBlue, white, black, pink, mygreen, font, rand

        # some colours might be useful
        orange = (255,153,0)
        red = (255,0,0)
        green = (0,255,0)
        blue = (0,0,255)
        darkBlue = (0,0,128)
        white = (255,255,255)
        black = (0,0,0)
        pink = (155,100,100)
        mygreen = (0, 135, 0)



        spawnInterval = 20.0

        basicAI = BasicAI(self.cgi)
        try:
            self.addHumanPlayer(factions.RADIANT)
            self.addAI(factions.DIRE, basicAI)

        except FactionTakenError as e:
            print(str(e))

        w = 1280
        h = 720
        screen_size = (w, h)
        screen = pygame.display.set_mode(screen_size)  #, pygame.FULLSCREEN)

        background = pygame.Surface(screen.get_size())
        #background.fill(mygreen)
        # convert to make blitting faster
        background = background.convert()

        background_image = pygame.image.load("map.png").convert()

        #meleeimage = pygame.image.load("meleecreep.png").convert()
        #meleeimage.set_colorkey((255,255,255))
        #meleeimagerect = meleeimage.get_rect()
        #rangedimage = pygame.image.load("rangedcreep2.png").convert()
        #rangedimage.set_colorkey((255,255,255))
        #rangedimagerect = rangedimage.get_rect()

        clock = pygame.time.Clock()
        FPS = 10
        playtime = 0.0
        mainloop = True

        # 0 = all/both, 1 = radiant, 2  = dire,  3 = nothing
        view = 3

        self.direHardLane = []
        self.direMidLane = []
        self.direEasyLane = []

        self.radiantHardLane = []
        self.radiantEasyLane = []
        self.radiantMidLane = []

        for i in range(1,32):

            self.radiantMidLane.append((320 + i*20, 660 + i*-20))
            self.direMidLane.append((940 + i*-20, 40 + i*20))
            if i < 29:
                self.radiantHardLane.append((320, 660 + i*-20))
                self.radiantEasyLane.append((320 + i*20, 660))
                self.direHardLane.append((940,40 + i*20))
                self.direEasyLane.append((940 + i*-20,40))
            elif i == 29:
                self.radiantHardLane.append((320 + 20, 660 + i*-20))
                self.radiantEasyLane.append((320 + i*20, 640))
                self.direHardLane.append((940 - 20,40 + i*20))
                self.direEasyLane.append((940 + i*-20,60))
            elif i == 30:
                self.radiantHardLane.append((320 + 40, 660 + i*-20))
                self.radiantEasyLane.append((320 + i*20, 620))
                self.direHardLane.append((940 - 40,40 + i*20))
                self.direEasyLane.append((940 + i*-20,80))
        for i in range(29):
                self.radiantHardLane.append((320 + 60 + i*20, 40))
                self.radiantEasyLane.append((940, 600 + i*-20))
                self.direHardLane.append((940 - 60 - i*20,660))
                self.direEasyLane.append((320, 100 + i*20))

        radiantCreeps = []
        direCreeps = []

        availableHeroes = set()
        self.radiantHeroes = []
        self.direHeroes = []

        numberOfCreepsPerWave = 3

        n = 0
        FPS = 60

        direBuildings = self.generateDireBuildings()
        radiantBuildings = self.generateRadiantBuildings()

        previousSpawn = -10.0
        spawnInterval = 20.0

        spawning = 0
        spawningCooldown = 0

        self.generateHeroes(availableHeroes)
        self.randomlyPickHeroes(availableHeroes, self.radiantHeroes, factions.RADIANT)
        self.randomlyPickHeroes(availableHeroes, self.direHeroes, factions.DIRE)

        nextHero = 0
        inc = 0

        alphaMod = list(range(-44, 34, 2))
        #alphaMod.extend(list(range(25, -25, 2)))
        alphaMod.extend(list(reversed(range(-46, 35, 2))))
        print(str(alphaMod))

        slow_mo = False

        while mainloop:
            inc += 1

            # update offsets etc
            for c in radiantCreeps:
                c.newTurn()
            for c in direCreeps:
                c.newTurn()

            for h in self.radiantHeroes:
                h.newTurn()
            for h in self.direHeroes:
                h.newTurn()

            self.cgi.tick()

            milliseconds = clock.tick(FPS)
            playtime += milliseconds / 1000.0

            # SLOW
            if slow_mo:
                time.sleep(1)

            if spawning > 0:
                if spawningCooldown <= 0:
                    self.spawnCreep(radiantCreeps, self.radiantHardLane, spawning)
                    self.spawnCreep(radiantCreeps, self.radiantMidLane, spawning)
                    self.spawnCreep(radiantCreeps, self.radiantEasyLane, spawning)
                    #radiantCreeps.append(RangedCreep(radiantHardLane))

                    self.spawnCreep(direCreeps, self.direHardLane, spawning)
                    self.spawnCreep(direCreeps, self.direMidLane, spawning)
                    self.spawnCreep(direCreeps, self.direEasyLane, spawning)

                    spawning -= 1
                    spawningCooldown = 20
                else:
                    spawningCooldown -= 1

            if previousSpawn + spawnInterval < playtime:
                previousSpawn = playtime
                spawning = numberOfCreepsPerWave
                spawningCooldown = 20

            for event in pygame.event.get():
                # User presses QUIT-button.
                if event.type == pygame.QUIT:
                    mainloop = False
                elif event.type == pygame.KEYDOWN:
                    # User presses ESCAPE-Key
                    if event.key == pygame.K_ESCAPE:
                         mainloop = False
                    elif event.key == pygame.K_t:
                        # toggle view
                        view = (view + 1) % 4
                    elif event.key == pygame.K_s:
                        slow_mo = not slow_mo
                    elif event.key == pygame.K_q:
                        self.radiantHeroes[0].ultimate()
                    elif event.key == pygame.K_z:
                        for h in self.radiantHeroes:
                            if h.status == states.QUEUING:
                                #h.spawnHero(self.radiantHardLane)
                                self.cgi.press(self.player1_code, keys.SPAWN_HERO_IN_TOP_LANE)

                                break
                    elif event.key == pygame.K_x:
                        for h in self.radiantHeroes:
                            if h.status == states.QUEUING:
                                #h.spawnHero(self.radiantMidLane)
                                self.cgi.press(self.player1_code, keys.SPAWN_HERO_IN_MID_LANE)
                                break
                    elif event.key == pygame.K_c:
                        for h in self.radiantHeroes:
                            if h.status == states.QUEUING:
                                #h.spawnHero(self.radiantEasyLane)
                                self.cgi.press(self.player1_code, keys.SPAWN_HERO_IN_BOT_LANE)
                                break
                    elif event.key == pygame.K_5:
                        self.cgi.press(self.player2_code, keys.SPAWN_HERO_IN_TOP_LANE)
                    nextHero = nextHero + 1 % 5


            screen.fill(black)
            screen.blit(background_image, (235, -55))

            if view == 0 or view ==1:
                self.drawLane(screen, self.radiantHardLane, (1, 6, 12, 19))
                self.drawLane(screen, self.radiantMidLane, (1, 5, 9, 13))
                self.drawLane(screen, self.radiantEasyLane, (1, 6, 12, 24))
            if view == 0 or view == 2:
                self.drawLane(screen, self.direHardLane, (1, 6, 12, 19))
                self.drawLane(screen, self.direMidLane, (1, 5, 9, 13))
                self.drawLane(screen, self.direEasyLane, (1, 6, 12, 24))


            for b in radiantBuildings:
                if b.status == states.ALIVE:
                    if b.canAttack:
                        b.newTurn()
                        if self.inRange(b, self.direHeroes):
                            unused_variable = "attack enemies"
                        elif self.inRange(b, direCreeps):
                            unused_variable = "attack enemies"
                    screen.blit(b.image, b.pos)
                    b.draw(screen, colours[factions.RADIANT]["faction"])
                    self.drawHpBar(screen, b, green)


            for b in direBuildings:
                if b.status == states.ALIVE:
                    if b.canAttack:
                        b.newTurn()
                        if self.inRange(b, self.radiantHeroes):
                            unused_variable = "attack enemies"
                        elif self.inRange(b, radiantCreeps):
                            unused_variable = "attack enemies"
                    screen.blit(b.image, b.pos)
                    b.draw(screen, colours[factions.DIRE]["faction"])
                    self.drawHpBar(screen, b, red)
                #print(b.name + "(" + str(b.hp) + "): " + str(b.pos[0]) + "," + str(b.pos[1]))

            for c in radiantCreeps:
                if self.inRange(c, self.direHeroes): # this function records aggro
                    unused_variable = "attack enemies"
                elif self.inRange(c, direCreeps): # this function records aggro
                    unused_variable = "attack enemies"
                elif self.buildingsInRange(c, direBuildings):
                    unused_variable = "attack buildings"
                else:
                    # find out where the creep is heading
                    if len(c.path) > 0:
                        prevPathPos = c.path[c.pathPos-1]
                        if len(c.path) > c.pathPos:
                            targetPathPos = c.path[c.pathPos]
                    else:
                        prevPathPos = c.path[c.pathPos]
                        targetPathPos = c.path[c.pathPos+1]
                    targetx = targetPathPos[0] - prevPathPos[0]
                    targety = targetPathPos[1] - prevPathPos[1]
                    oldPos = c.pos
                    c.move()
                    # the move might be blocked! check if it's possible:'
                    if self.collision(c, c.pos, direCreeps, radiantCreeps):
                        #generate some random alternate moves:
                        #left/right if moving vertically - pick one and continue each turn
                        #up/down if moving vertically
                        # zero one if moving both - again remember. basically, more intelligent moves
                        # if that doesn't work try very random
                        # if not, stand still. update c.pos
                        movex = c.pos[0] - oldPos[0]
                        movey = c.pos[1] - oldPos[1]

                        # this bit is not working very well:


                        #print("Collision!: " + str(targetx) + "," + str(targety))
                        #c.pos = (oldPos[0] + rand.sample([-1,0,1], 1)[0], oldPos[1] + rand.sample([-1,0,1], 1)[0])
                        if targety < 0:
                            if not self.collision(c, (oldPos[0] + c.randomDirection, oldPos[1] - 1), direCreeps, radiantCreeps):
                                c.pos = (oldPos[0] + c.randomDirection, oldPos[1] - 1)
                            elif not self.collision(c, (oldPos[0] + c.randomDirection, oldPos[1]), direCreeps, radiantCreeps):
                                c.pos = (oldPos[0] + c.randomDirection, oldPos[1])
                            #elif not self.collision(c, (oldPos[0] + c.randomDirection, oldPos[1]), direCreeps, radiantCreeps):
                            #    c.pos = (oldPos[0] + c.randomDirection, oldPos[1] + 1)
                            else:
                                c.pos = self.standOrRand(c, oldPos)
                        if targety > 0:
                            if not self.collision(c, (oldPos[0] + c.randomDirection, oldPos[1] + 1), direCreeps, radiantCreeps):
                                c.pos = (oldPos[0] + c.randomDirection, oldPos[1] + 1)
                            elif not self.collision(c, (oldPos[0] + c.randomDirection, oldPos[1]), direCreeps, radiantCreeps):
                                c.pos = (oldPos[0] + c.randomDirection, oldPos[1])
                            #elif not self.collision(c, (oldPos[0] + c.randomDirection, oldPos[1]), direCreeps, radiantCreeps):
                            #    c.pos = (oldPos[0] + c.randomDirection, oldPos[1] - 1)
                            else:
                                c.pos = self.standOrRand(c, oldPos)
                        if targetx < 0:
                            if not self.collision(c, (oldPos[0] - 1, oldPos[1] + c.randomDirection), direCreeps, radiantCreeps):
                                c.pos = (oldPos[0] - 1, oldPos[1] + c.randomDirection)
                            elif not self.collision(c, (oldPos[0], oldPos[1] + c.randomDirection), direCreeps, radiantCreeps):
                                c.pos = (oldPos[0], oldPos[1] + c.randomDirection)
                            #elif not self.collision(c, (oldPos[0], oldPos[1] + c.randomDirection), direCreeps, radiantCreeps):
                            #    c.pos = (oldPos[0] + 1, oldPos[1] + c.randomDirection)
                            else:
                                c.pos = self.standOrRand(c, oldPos)
                        if targetx > 0:
                            if not self.collision(c, (oldPos[0] + 1, oldPos[1] + c.randomDirection), direCreeps, radiantCreeps):
                                c.pos = (oldPos[0] + 1, oldPos[1] + c.randomDirection)
                            elif not self.collision(c, (oldPos[0], oldPos[1] + c.randomDirection), direCreeps, radiantCreeps):
                                c.pos = (oldPos[0], oldPos[1] + c.randomDirection)
                            #elif not self.collision(c, (oldPos[0] - 1, oldPos[1] + c.randomDirection), direCreeps, radiantCreeps):
                            #    c.pos = (oldPos[0] - 1, oldPos[1] + c.randomDirection)
                            else:
                                c.pos = self.standOrRand(c, oldPos) #(oldPos[0], oldPos[1])

                        if c.paused:
                            c.standingStillCounter -= 1
                            if c.standingStillCounter == 0:
                                if rand.randrange(1) == 0:
                                    if len(c.path) > c.pathPos + 1:
                                        c.pathPos += 1
                                c.paused = False
                                #print("UNPAUSED") # never triggered...
                                quit()
                        else:
                            if self.dist(c.pos, c.prevPos) <= c.radius/2:
                                c.standingStillCounter += 1
                                #print("Standing still: " + str(c.standingStillCounter))
                                if rand.randrange(1) < c.standingStillCounter:
                                    c.paused = True
                                    #print("PAUSED")
                                    quit()
                            else:
                                c.standingStillCounter += 0
                                #c.paused = False

                screen.blit(c.image, c.offsetPos)

                c.draw(screen, colours[factions.RADIANT]["faction"])
                self.drawHpBar(screen, c, green)

            for c in direCreeps:
                if self.inRange(c, self.radiantHeroes): # this function records aggro
                    unused_variable = "attack enemy heroes"
                elif self.inRange(c, radiantCreeps): # this function records aggro
                    unused_variable = "attack enemy creeps"
                elif self.buildingsInRange(c, radiantBuildings):
                    unused_variable = "attack buildings"
                else:
                    # find out where the creep is heading
                    if len(c.path) > 0:
                        prevPathPos = c.path[c.pathPos-1]
                        if len(c.path) > c.pathPos:
                            targetPathPos = c.path[c.pathPos]
                    else:
                        prevPathPos = c.path[c.pathPos]
                        targetPathPos = c.path[c.pathPos+1]
                    targetx = targetPathPos[0] - prevPathPos[0]
                    targety = targetPathPos[1] - prevPathPos[1]
                    oldPos = c.pos
                    c.move()
                    # the move might be blocked! check if it's possible:'
                    if self.collision(c, c.pos, radiantCreeps, direCreeps):
                        c.pos = oldPos # just stand still

                # offset creep so they dont stand on top of each other

                screen.blit(c.image, c.offsetPos)
                #screen.update(c.image)
                c.draw(screen, colours[factions.DIRE]["faction"])

                self.drawHpBar(screen, c, red) # TODO: also offset hp bar...



 # TODO: this should all be h.update() followed by h.draw() - and h.update() can call view.attackDireCreeps() etc
            hero_number = 0
            for h in self.radiantHeroes:
                if h.status == states.ALIVE:
                    if self.inRange(h, self.direHeroes):
                        unused_variable = "attack enemy heroes"
                    elif self.inRange(h, direCreeps): # this function records aggro
                        unused_variable = "attack enemy creeps"
                    elif self.buildingsInRange(h, direBuildings):
                        unused_variable = "attack buildings"
                    else:
                        # find out where the creep is heading
                        if len(h.path) > 0:
                            prevPathPos = h.path[h.pathPos-1]
                            if len(h.path) > h.pathPos:
                                targetPathPos = h.path[h.pathPos]
                        else:
                            prevPathPos = h.path[h.pathPos]
                            targetPathPos = h.path[h.pathPos+1]
                        targetx = targetPathPos[0] - prevPathPos[0]
                        targety = targetPathPos[1] - prevPathPos[1]
                        oldPos = h.pos
                        h.move()
                        # the move might be blocked! check if it's possible:'
                        if self.collision(h, h.pos, radiantCreeps, direCreeps):
                            h.pos = oldPos # just stand still

                    # offset creep so they dont stand on top of each other

                    #screen.blit(h.image, h.offsetPos)
                h.draw(screen, orange, hero_number, factions.RADIANT, alphaMod[inc % len(alphaMod)])


                    #self.drawHpBar(screen, h, blue) # TODO: also offset hp bar...

                    #self.drawPortrait(screen, h, "radiant", hero_number)

                hero_number += 1

            hero_number = 0
            for h in self.direHeroes:
                if h.status == states.ALIVE:
                    if self.inRange(h, self.radiantHeroes):
                        unused_variable = "attack enemy heroes"
                    elif self.inRange(h, radiantCreeps): # this function records aggro
                        unused_variable = "attack enemy creeps"
                    elif self.buildingsInRange(h, radiantBuildings):
                        unused_variable = "attack buildings"
                    else:
                        # find out where the creep is heading
                        if len(h.path) > 0:
                            prevPathPos = h.path[h.pathPos-1]
                            if len(h.path) > h.pathPos:
                                targetPathPos = h.path[h.pathPos]
                        else:
                            prevPathPos = h.path[h.pathPos]
                            targetPathPos = h.path[h.pathPos+1]
                        targetx = targetPathPos[0] - prevPathPos[0]
                        targety = targetPathPos[1] - prevPathPos[1]
                        oldPos = h.pos
                        h.move()
                        # the move might be blocked! check if it's possible:'
                        if self.collision(h, h.pos, direCreeps, radiantCreeps):
                            h.pos = oldPos # just stand still

                    # offset creep so they dont stand on top of each other

                    #screen.blit(h.image, h.offsetPos)
                h.draw(screen, orange, hero_number, factions.DIRE, alphaMod[inc % len(alphaMod)])
                    #self.drawHpBar(screen, h, orange) # TODO: also offset hp bar...

                    #self.drawPortrait(screen, h, "dire", hero_number)

                hero_number += 1

            n += 1

            text = "FPS: {0:.2f}   Playtime: {1:.2f}".format(clock.get_fps(), playtime)
            pygame.display.set_caption(text)
            pygame.display.flip()
            if direBuildings[0].hp <= 0:
                print("The Dire ancient has been destroyed!")
                mainloop = False
            if radiantBuildings[0].hp <= 0:
                print("The Radiant ancient has been destroyed!")
                mainloop = False


if __name__ == "__main__":
    view = View()
    view.start()

