import math
import pygame
import random
from pygame.locals import *

class Building:

    def __init__(self, pos, hp=300, rect=None, image=None, viewModifier=-20, name="Unnamed Building"):
        self.name = name
        self.hp = hp
        self.hpmax = self.hp
        self.alive = True
        self.regen = 1
        self.canAttack = False
        self.pos = pos
        self.offsetPos = pos
        self.radius = 10
        self.rect = rect
        self.image = image
        self.viewModifier = viewModifier
        self.armor = 15

    def damage(self, dam):
        self.hp -= dam
        if self.hp <= 0:
            self.alive = False

class Lvl1Tower(Building):

    def __init__(self, pos, rect, image, viewModifier=-20, name="Lvl 1 Tower"):
        hp = 1300
        super(Lvl1Tower, self).__init__(pos, hp, rect, image, viewModifier, name)
        self.canAttack = True
        self.attackRange = 40
        self.readyToAttack = True
        self.maxAttack = 120
        self.minAttack = 100
        self.attackCooldown = 50
        self.currentAttackCooldown = 0
        self.armor = 20

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

class Ancient(Building):

    def __init__(self, pos, rect, image, viewModifier=-20, name="Ancient"):
        hp = 4250
        super(Ancient, self).__init__(pos, hp, rect, image, viewModifier, name)
        self.radius = 100
        self.regen = 3

class Creep:

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
        self.pos = path[0]
        self.prevPos = self.pos #used for checking if the creep is stuck
        self.offsetPos = self.pos
        self.attackRange = 5
        self.readyToAttack = True
        self.attackCooldown = 30
        self.currentAttackCooldown = 0
        self.radius = 10
        self.randomDirection = rand.sample([-1,1],1)[0]
        self.paused = False
        self.standingStillCounter = 0
        self.image = image
        self.viewModifier = 0
        self.alive = True
        self.offset = 0
        self.armor = 2

    def resetAttackCooldown(self):
        self.readyToAttack = False
        self.currentAttackCooldown = self.attackCooldown

    def newTurn(self):
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
            self.alive = False

    def attack(self):
        global rand
        return rand.randrange(self.minAttack, self.maxAttack)


class MeleeCreep(Creep):

    meleeimage = pygame.image.load("meleecreep.png")    # didn't convert. is that bad?'
    meleeimage.set_colorkey(( 255, 255, 255))
    meleeimagerect = meleeimage.get_rect()

    def __init__(self, path, rect=None, image=None):
        super(MeleeCreep, self).__init__(path, rect, image, "Melee Creep")
        self.hp = 550
        self.hpmax = 550
        self.image = MeleeCreep.meleeimage.convert()
        self.rect = MeleeCreep.meleeimagerect

class RangedCreep(Creep):
    rangedimage = pygame.image.load("rangedcreep2.png")
    rangedimage.set_colorkey((255, 255, 255))
    rangedimagerect = rangedimage.get_rect()

    def __init__(self, path, rect=None, image=None):
        super(RangedCreep, self).__init__(path, rect, image, "Ranged Creep")
        self.attackRange = 20
        self.hp = 300
        self.image = RangedCreep.rangedimage.convert()
        self.rect = RangedCreep.rangedimagerect
        self.maxAttack = 26
        self.minAttack = 21
        self.armor = 0


class View:

    def __init__(self):
        global font, rand
        pygame.init()
        font = pygame.font.SysFont('Arial', 16)
        rand = random.Random()
        rand.seed(2)

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
        global green, black
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
        buildings.append(Lvl1Tower((320, 640), radiantTowerImageRect, radiantTowerImage)) #lvl4
        buildings.append(Lvl1Tower((320, 540), radiantTowerImageRect, radiantTowerImage))
        buildings.append(Lvl1Tower((320, 420), radiantTowerImageRect, radiantTowerImage))
        buildings.append(Lvl1Tower((320, 280), radiantTowerImageRect, radiantTowerImage))
        #mid:
        buildings.append(Lvl1Tower((340, 640), radiantTowerImageRect, radiantTowerImage, -10))
        buildings.append(Lvl1Tower((420, 560), radiantTowerImageRect, radiantTowerImage))
        buildings.append(Lvl1Tower((500, 480), radiantTowerImageRect, radiantTowerImage))
        buildings.append(Lvl1Tower((580, 400), radiantTowerImageRect, radiantTowerImage))
        #hard:
        buildings.append(Lvl1Tower((340, 660), radiantTowerImageRect, radiantTowerImage))
        buildings.append(Lvl1Tower((440, 660), radiantTowerImageRect, radiantTowerImage))
        buildings.append(Lvl1Tower((560, 660), radiantTowerImageRect, radiantTowerImage))
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
        buildings.append(Lvl1Tower((920, 40), direTowerImageRect, direTowerImage)) #lvl4
        buildings.append(Lvl1Tower((820, 40), direTowerImageRect, direTowerImage))
        buildings.append(Lvl1Tower((700, 40), direTowerImageRect, direTowerImage))
        buildings.append(Lvl1Tower((460, 40), direTowerImageRect, direTowerImage))
        #mid:
        buildings.append(Lvl1Tower((920, 60), direTowerImageRect, direTowerImage, -10))
        buildings.append(Lvl1Tower((840, 140), direTowerImageRect, direTowerImage))
        buildings.append(Lvl1Tower((760, 220), direTowerImageRect, direTowerImage))
        buildings.append(Lvl1Tower((680, 300), direTowerImageRect, direTowerImage))
        #hard:
        buildings.append(Lvl1Tower((940, 60), direTowerImageRect, direTowerImage))
        buildings.append(Lvl1Tower((940, 160), direTowerImageRect, direTowerImage))
        buildings.append(Lvl1Tower((940, 280), direTowerImageRect, direTowerImage))
        buildings.append(Lvl1Tower((940, 420), direTowerImageRect, direTowerImage))
        return buildings

    def dist(self, p, q):
        return math.sqrt((p[0] - q[0]) ** 2+(p[1] - q[1]) ** 2)

    def inRange(self, creep, targets):
        for t in targets:
            if t.alive:
               if self.dist(creep.pos, t.pos) <= creep.attackRange:
                    self.attack(creep, t)
                    if not t.alive:
                        targets.remove(t)
                    return True
        return False

    def buildingsInRange(self, creep, buildings):
        for b in buildings:
            if b.alive:
               if self.dist(creep.pos, b.pos) <= creep.attackRange:
                    self.attack(creep, b)
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
            print(str(source.name) + " hitting " + str(atk) + " on " + str(dest.name) + "(with armor " + str(dest.armor) + ") means dmg reduction of " + str(dmgReduction) + " == damage dealt: " + str(dmg))

            dest.damage(dmg)

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
        # spawnCreep(radiantCreeps,RangedCreep(radiantHardLane),spawning)
        creep = None
        if spawningNo == 1:
            creep = RangedCreep(lane)
        else:
            creep = MeleeCreep(lane)
        creep.offset = 2 * spawningNo * creep.randomDirection
        if spawningNo == 5:
            creep.offset = 0
        group.append(creep)

        #                        radiantCreeps.append(RangedCreep(radiantHardLane, rangedimagerect, rangedimage))

    def start(self):
        global red, green, blue, darkBlue, white, black, pink, mygreen, font, rand

        # some colours might be useful
        red = (255,0,0)
        green = (0,255,0)
        blue = (0,0,255)
        darkBlue = (0,0,128)
        white = (255,255,255)
        black = (0,0,0)
        pink = (155,100,100)
        mygreen = (0, 135, 0)

        spawnInterval = 20.0


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
        FPS = 60
        playtime = 0.0
        mainloop = True

        # 0 = all/both, 1 = radiant, 2  = dire,  3 = nothing
        view = 3

        direHardLane = []
        direMidLane = []
        direEasyLane = []

        radiantHardLane = []
        radiantEasyLane = []
        radiantMidLane = []

        for i in range(1,32):

            radiantMidLane.append((320 + i*20, 660 + i*-20))
            direMidLane.append((940 + i*-20, 40 + i*20))
            if i < 29:
                radiantHardLane.append((320, 660 + i*-20))
                radiantEasyLane.append((320 + i*20, 660))
                direHardLane.append((940,40 + i*20))
                direEasyLane.append((940 + i*-20,40))
            elif i == 29:
                radiantHardLane.append((320 + 20, 660 + i*-20))
                radiantEasyLane.append((320 + i*20, 640))
                direHardLane.append((940 - 20,40 + i*20))
                direEasyLane.append((940 + i*-20,60))
            elif i == 30:
                radiantHardLane.append((320 + 40, 660 + i*-20))
                radiantEasyLane.append((320 + i*20, 620))
                direHardLane.append((940 - 40,40 + i*20))
                direEasyLane.append((940 + i*-20,80))
        for i in range(29):
                radiantHardLane.append((320 + 60 + i*20, 40))
                radiantEasyLane.append((940, 600 + i*-20))
                direHardLane.append((940 - 60 - i*20,660))
                direEasyLane.append((320, 100 + i*20))

        radiantCreeps = []
        direCreeps = []

        n = 0
        FPS = 60

        direBuildings = self.generateDireBuildings()
        radiantBuildings = self.generateRadiantBuildings()

        previousSpawn = -10.0
        spawnInterval = 20.0

        spawning = 0
        spawningCooldown = 0

        while mainloop:

            # update offsets etc
            for c in radiantCreeps:
                c.newTurn()
            for c in direCreeps:
                c.newTurn()

            milliseconds = clock.tick(FPS)
            playtime += milliseconds / 1000.0

            if spawning > 0:
                if spawningCooldown <= 0:
                    self.spawnCreep(radiantCreeps, radiantHardLane, spawning)
                    self.spawnCreep(radiantCreeps, radiantMidLane, spawning)
                    self.spawnCreep(radiantCreeps, radiantEasyLane, spawning)
                    #radiantCreeps.append(RangedCreep(radiantHardLane))

                    self.spawnCreep(direCreeps, direHardLane, spawning)
                    self.spawnCreep(direCreeps, direMidLane, spawning)
                    self.spawnCreep(direCreeps, direEasyLane, spawning)

                    spawning -= 1
                    spawningCooldown = 20
                else:
                    spawningCooldown -= 1

            if previousSpawn + spawnInterval < playtime:
                previousSpawn = playtime
                spawning = 5
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

            screen.fill(black)
            screen.blit(background_image, (235, -55))

            if view == 0 or view ==1:
                self.drawLane(screen, radiantHardLane, (1, 6, 12, 19))
                self.drawLane(screen, radiantMidLane, (1, 5, 9, 13))
                self.drawLane(screen, radiantEasyLane, (1, 6, 12, 24))
            if view == 0 or view == 2:
                self.drawLane(screen, direHardLane, (1, 6, 12, 19))
                self.drawLane(screen, direMidLane, (1, 5, 9, 13))
                self.drawLane(screen, direEasyLane, (1, 6, 12, 24))

            for b in direBuildings:
                if b.alive:
                    if b.canAttack:
                        b.newTurn()
                        self.inRange(b, radiantCreeps)
                    screen.blit(b.image, b.pos)
                    self.drawHpBar(screen, b, red)
                #print(b.name + "(" + str(b.hp) + "): " + str(b.pos[0]) + "," + str(b.pos[1]))
            for b in radiantBuildings:
                if b.alive:
                    if b.canAttack:
                        b.newTurn()
                        self.inRange(b, direCreeps)
                    screen.blit(b.image, b.pos)
                    self.drawHpBar(screen, b, green)


            for c in radiantCreeps:
                if self.inRange(c, direCreeps): # this function records aggro
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

                self.drawHpBar(screen, c, green)

            for c in direCreeps:
                if self.inRange(c, radiantCreeps): # this function records aggro
                    unused_variable = "attack enemies"
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

                self.drawHpBar(screen, c, red) # TODO: also offset hp bar...

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

