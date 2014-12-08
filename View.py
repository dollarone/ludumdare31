import math
import pygame
import random
from pygame.locals import *

class Building:

    def __init__(self, pos, hp=300):
        self.name = "Unnamed Building"
        self.totalHp = hp
        self.hp = self.totalHp
        self.alive = True
        self.regen = 1
        self.canAttack = False
        self.pos = pos

    def damage(self, dam):
        self.hp -= dam
        if self.hp <= 0:
            self.alive = False

class Lvl1Tower(Building):

    def __init__(self, pos):
        super(Lvl1Tower, self).__init__(pos)
        self.name = "Lvl 1 Tower"
        self.attack = 20
        self.canAttack = True
        self.attackRange = 40
        self.readyToAttack = True

    def resetAttackCooldown(self):
        readyToAttack = False

class Ancient(Building):

    def __init__(self, pos, name="Ancient"):
        hp = 1000
        super(Ancient, self).__init__(pos, hp)
        self.name = name

class Creep:

    def __init__(self, path=[], rect=None, creepType="Unknown"):
        global rand
        self.path = path
        self.rect = rect
        self.hp = 200
        self.attack = 10
        self.pathPos = 0
        self.pos = path[0]
        self.attackRange = 5
        self.readyToAttack = True
        self.attackCooldown = 10
        self.currentAttackCooldown = 0
        self.creepType = creepType
        self.radius = 10
        self.randomDirection = rand.sample([-1,1],1)[0]

    def resetAttackCooldown(self):
        self.readyToAttack = False
        self.currentAttackCooldown = self.attackCooldown

    def newTurn(self):
        if self.currentAttackCooldown > 0:
            self.currentAttackCooldown -= 1
        if self.currentAttackCooldown == 0:
            self.readyToAttack = True

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

class MeleeCreep(Creep):

    def __init__(self, path, rect):
        super(MeleeCreep, self).__init__(path, rect, "Melee Creep")

class RangedCreep(Creep):

    def __init__(self, path, rect):
        super(RangedCreep, self).__init__(path, rect, "Ranged Creep")
        self.attackRange = 20

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
        n = 0
        for i in lane:
            if n in towers:
                #print("Tower at " + str(i[0]) + "," + str(i[1]))
                self.addRect(scr, darkBlue, i, (20, 20))
                self.addText(scr, darkBlue, i, n)
            else:
                self.addRect(scr, red, i, (20, 20))
                self.addText(scr, red, i, n)
            n += 1

    def generateRadiantBuildings(self):
        buildings = []
        buildings.append(Ancient((320, 660), "Radiant Ancient"))
        return buildings

    def generateDireBuildings(self):
        buildings = []
        buildings.append(Ancient((940, 40), "Dire Ancient"))
        buildings.append(Lvl1Tower((320, 540)))
        return buildings
        #buildings.append(Tower((940, 40)))
#            radiantMidLane.append((320 + i*20, 660 + i*-20))
#            direMidLane.append((940 + i*-20, 40 + i*20))
#New turn
#Tower at 320,640
#Tower at 320,540
#Tower at 320,420
#Tower at 320,280
#Tower at 340,640
#Tower at 420,560
#Tower at 500,480
#Tower at 580,400
#Tower at 340,660
#Tower at 440,660
#Tower at 560,660
#Tower at 800,660
#Tower at 940,60
#Tower at 940,160
#Tower at 940,280
#Tower at 940,420
#Tower at 920,60
#Tower at 840,140
#Tower at 760,220
#Tower at 680,300
#Tower at 920,40
#Tower at 820,40
#Tower at 700,40
#Tower at 460,40

    def dist(self, p, q):
        return math.sqrt((p[0] - q[0]) ** 2+(p[1] - q[1]) ** 2)

    def enemiesInRange(self):
        return False

    def buildingsInRange(self, creep, buildings):
        for b in buildings:
            if b.alive:
               if self.dist(creep.pos, b.pos) <= creep.attackRange:
                    self.attack(creep, b)
                    return True

#            if b.canAttack():
 #               if self.dist(creep.pos, buildings.pos) <= b.attackRange:
  #                  attack(b.attack, creep)

        return False

    def attack(self, source, dest):
        # TODO: armor etc

        if source.readyToAttack:
            source.resetAttackCooldown()
            dest.damage(source.attack)

    def collision(self, creep, pos, direCreeps, radiantCreeps):
        for c in direCreeps:
            if id(c) != id(creep):
                if self.dist(pos, c.pos) <= c.radius:
                    print("pos: " + str(c.pos) + " is " + str(self.dist(pos, c.pos)) + " from " + str(c.pos))
                    #quit()
                    return True
        for c in radiantCreeps:
            if id(c) != id(creep):
                if self.dist(pos, c.pos) <= c.radius:
                    print("pos: " + str(c.pos) + " is " + str(self.dist(pos, c.pos)) + " from " + str(c.pos))
                    #quit()
                    return True
        return False

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

        w = 1280
        h = 720
        screen_size = (w, h)
        screen = pygame.display.set_mode(screen_size, pygame.FULLSCREEN)
        background = pygame.Surface(screen.get_size())
        background.fill(mygreen)
        # convert to make blitting faster
        background = background.convert()
        screen.blit(background, (0, 0))

        meleeimage = pygame.image.load("meleecreep.png").convert()
        rangedimage = pygame.image.load("rangedcreep2.png").convert()
        #myimage.set_colorkey(-1, RLEACCEL) # use upper-left pixel as transparent
        meleeimage.set_colorkey((255,255,255))
        meleeimagerect = meleeimage.get_rect()
        rangedimage.set_colorkey((255,255,255))
        rangedimagerect = rangedimage.get_rect()

        clock = pygame.time.Clock()
        FPS = 60
        playtime = 0.0
        mainloop = True

        # 0 = all/both, 1 = radiant, 2  = dire,  3 = nothing
        view = 1

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
        #creep = Creep(radiantHardLane, imagerect)
        radiantCreeps = []
        direCreeps = []

        n = 0
        FPS = 60

        direBuildings = self.generateDireBuildings()
        radiantBuildings = self.generateRadiantBuildings()

        previousSpawn = -8.0
        spawning = 0
        spawningCooldown = 0

        while mainloop:
            print("New turn")
            for b in direBuildings:
                #newTurn(b)
                print(b.name + "(" + str(b.hp) + "): " + str(b.pos[0]) + "," + str(b.pos[1]))
            for b in radiantBuildings:
                print(b.name + "(" + str(b.hp) + "): " + str(b.pos[0]) + "," + str(b.pos[1]))
            for c in radiantCreeps:
                c.newTurn()
            for c in direCreeps:
                c.newTurn()

            milliseconds = clock.tick(FPS)
            playtime += milliseconds / 1000.0

            if spawning > 0:
                if spawningCooldown <= 0:
                    if spawning == 1:
                        radiantCreeps.append(RangedCreep(radiantHardLane, rangedimagerect))
                        radiantCreeps.append(RangedCreep(radiantMidLane, rangedimagerect))
                        radiantCreeps.append(RangedCreep(radiantEasyLane, rangedimagerect))
                    else:
                        radiantCreeps.append(MeleeCreep(radiantHardLane, meleeimagerect))
                        radiantCreeps.append(MeleeCreep(radiantMidLane, meleeimagerect))
                        radiantCreeps.append(MeleeCreep(radiantEasyLane, meleeimagerect))

                    spawning -= 1
                    spawningCooldown = 20
                else:
                    spawningCooldown -= 1

            if previousSpawn + 10.0 < playtime:
                radiantCreeps.append(MeleeCreep(radiantHardLane, meleeimagerect))
                radiantCreeps.append(MeleeCreep(radiantMidLane, meleeimagerect))
                radiantCreeps.append(MeleeCreep(radiantEasyLane, meleeimagerect))
                previousSpawn = playtime
                spawning = 4
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

            #pygame.display.update()

            #imagerect.move_ip(1, 1)
            screen.fill(mygreen)
            #screen.blit(myimage, creep.pos)
            for c in radiantCreeps:
                if self.enemiesInRange(): # this function records aggro
                    print("attack")
                elif self.buildingsInRange(c, direBuildings):
                    print("attack buildings")
                else:
                    oldPos = c.pos
                    c.move()
                    # the move might be blocked!
                    if self.collision(c, c.pos, direCreeps, radiantCreeps):
                        #generate some random alternate moves:
                        #left/right if moving vertically - pick one and continue each turn
                        #up/down if moving vertically
                        # zero one if moving both - again remember. basically, more intelligent moves
                        # if that doesn't work try very random
                        # if not, stand still. update c.pos
                        movex = c.pos[0] - oldPos[0]
                        movey = c.pos[1] - oldPos[1]
                        print("Collision!: " + str(movex) + "," + str(movey))
                        #c.pos = (oldPos[0] + rand.sample([-1,0,1], 1)[0], oldPos[1] + rand.sample([-1,0,1], 1)[0])
                        if movey == -1:
                            if not self.collision(c, (oldPos[0] + c.randomDirection, oldPos[1] - 1), direCreeps, radiantCreeps):
                                c.pos = (oldPos[0] + c.randomDirection, oldPos[1] - 1)
                            elif not self.collision(c, (oldPos[0] + c.randomDirection, oldPos[1]), direCreeps, radiantCreeps):
                                c.pos = (oldPos[0] + c.randomDirection, oldPos[1])
                            else:
                                c.pos = (oldPos[0], oldPos[1])
                        if movey == 1:
                            if not self.collision(c, (oldPos[0] + c.randomDirection, oldPos[1] + 1), direCreeps, radiantCreeps):
                                c.pos = (oldPos[0] + c.randomDirection, oldPos[1] + 1)
                            elif not self.collision(c, (oldPos[0] + c.randomDirection, oldPos[1]), direCreeps, radiantCreeps):
                                c.pos = (oldPos[0] + c.randomDirection, oldPos[1])
                            else:
                                c.pos = (oldPos[0], oldPos[1])
                        if movex == -1:
                            if not self.collision(c, (oldPos[0] - 1, oldPos[1] + c.randomDirection), direCreeps, radiantCreeps):
                                c.pos = (oldPos[0] - 1, oldPos[1] + c.randomDirection)
                            elif not self.collision(c, (oldPos[0], oldPos[1] + c.randomDirection), direCreeps, radiantCreeps):
                                c.pos = (oldPos[0], oldPos[1] + c.randomDirection)
                            else:
                                c.pos = (oldPos[0], oldPos[1])
                        if movex == 1:
                            if not self.collision(c, (oldPos[0] + 1, oldPos[1] + c.randomDirection), direCreeps, radiantCreeps):
                                c.pos = (oldPos[0] + 1, oldPos[1] + c.randomDirection)
                            elif not self.collision(c, (oldPos[0], oldPos[1] + c.randomDirection), direCreeps, radiantCreeps):
                                c.pos = (oldPos[0], oldPos[1] + c.randomDirection)
                            else:
                                c.pos = (oldPos[0], oldPos[1])



                        if 1 == 0: #movex == 1 and movey == 0:
                            # TOO COMPLICATED'
                            tryMove = rand.sample(set([-1,1]), 1)
                            print("tryMove7: " + str(tryMove))
                            tryMove = tryMove[0]
                            if self.collision(c, (oldPos[0] + 1, oldPos[1] + tryMove), direCreeps, radiantCreeps):
                                if self.collision(c, (oldPos[0] + 1, oldPos[1] + tryMove*-1), direCreeps, radiantCreeps):
                                    if self.collision(c, (oldPos[0], oldPos[1] + tryMove), direCreeps, radiantCreeps):
                                        if self.collision(c, (oldPos[0], oldPos[1] + tryMove*-1), direCreeps, radiantCreeps):
                                            if self.collision(c, (oldPos[0] - 1, oldPos[1] + tryMove), direCreeps, radiantCreeps):
                                                if self.collision(c, (oldPos[0] - 1, oldPos[1] + tryMove *-1), direCreeps, radiantCreeps):
                                                    c.pos = (oldPos[0], oldPos[1])
                                                else:
                                                    c.pos = (oldPos[0] - 1, oldPos[1] + tryMove *-1)
                                            else:
                                                c.pos = (oldPos[0] - 1, oldPos[1] + tryMove)
                                        else:
                                            c.pos = (oldPos[0], oldPos[1] + tryMove *-1)
                                    else:
                                        c.pos = (oldPos[0], oldPos[1] + tryMove)
                                else:
                                    c.pos = (oldPos[0] + 1, oldPos[1] + tryMove *-1)
                            else:
                                c.pos = (oldPos[0] + 1, oldPos[1] + tryMove)
                        #else: #if 1 ==2: #if movex == 0 and movey == 1:
                            tryMove = c.randomDirection# rand.sample(set([-3,-2,-1,1,2,3]), 1)
                            print("tryMove: " + str(tryMove))
                            #tryMove = tryMove[0]
                            if self.collision(c, (oldPos[0] + tryMove, oldPos[1] + 1), direCreeps, radiantCreeps):
                                if self.collision(c, (oldPos[0] + tryMove *-1, oldPos[1] + 1), direCreeps, radiantCreeps):
                                    if self.collision(c, (oldPos[0] + tryMove, oldPos[1]), direCreeps, radiantCreeps):
                                        if self.collision(c, (oldPos[0] + tryMove *-1, oldPos[1]), direCreeps, radiantCreeps):
                                            if self.collision(c, (oldPos[0] + tryMove, oldPos[1] - 1), direCreeps, radiantCreeps):
                                                if self.collision(c, (oldPos[0] + tryMove *-1, oldPos[1] - 1), direCreeps, radiantCreeps):
                                                    c.pos = (oldPos[0], oldPos[1])
                                                else:
                                                    c.pos = (oldPos[0] + tryMove *-1, oldPos[1] - 1)
                                            else:
                                                c.pos = (oldPos[0] + tryMove, oldPos[1] - 1)
                                        else:
                                            c.pos = (oldPos[0] + tryMove *-1, oldPos[1])
                                    else:
                                        c.pos = (oldPos[0] + tryMove, oldPos[1])
                                else:
                                    c.pos = (oldPos[0] + tryMove *-1, oldPos[1] + 1)
                            else:
                                c.pos = (oldPos[0] + tryMove, oldPos[1] + 1)



                # we have 20 pixels to  move
                #if FPS % 20 == 0:
                #c.move()
                #    print("lol " + str(FPS % 20))
                if c.creepType == "Ranged Creep":
                    screen.blit(rangedimage, c.pos)
                else:
                    screen.blit(meleeimage, c.pos)
                #if len(c.path) > n:
                #    c.pathPos = n
            n += 1

            if view == 0 or view ==1:
                self.drawLane(screen, radiantHardLane, (1, 6, 12, 19))
                self.drawLane(screen, radiantMidLane, (1, 5, 9, 13))
                self.drawLane(screen, radiantEasyLane, (1, 6, 12, 24))
            if view == 0 or view == 2:
                self.drawLane(screen, direHardLane, (1, 6, 12, 19))
                self.drawLane(screen, direMidLane, (1, 5, 9, 13))
                self.drawLane(screen, direEasyLane, (1, 6, 12, 24))

        # top-left: 300, 80                 top-right: 1000, 80
        # mid-left:
        # bot-left: 300, 620                bot-right: 1000, 620

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

