import pygame

def addRect(scr, col, pos, size):
    pygame.draw.rect(scr, col, (pos[0], pos[1], size[0], size[1]), 1)

def addText(scr, col, pos, text):
    global font
    scr.blit(font.render(str(text), True, col), pos)


def main():
    global font
    # some colours might be useful
    red = (255,0,0)
    green = (0,255,0)
    blue = (0,0,255)
    darkBlue = (0,0,128)
    white = (255,255,255)
    black = (0,0,0)
    pink = (155,100,100)
    mygreen = (0, 135, 0)

    pygame.init()
    font = pygame.font.SysFont('Arial', 16)

    w = 1280
    h = 720
    screen_size = (w, h)
    screen = pygame.display.set_mode(screen_size, pygame.FULLSCREEN)
    background = pygame.Surface(screen.get_size())
    background.fill(mygreen)
    # convert to make blitting faster
    background = background.convert()
    screen.blit(background, (0, 0))

    myimage = pygame.image.load("randome.png")
    imagerect = myimage.get_rect()

    clock = pygame.time.Clock()
    FPS = 60
    playtime = 0.0
    mainloop = True

    # 0 = all/both, 1 = radiant, 2  = dire
    view = 1

    while mainloop:
        milliseconds = clock.tick(FPS)
        playtime += milliseconds / 1000.0
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
                    view = (view + 1) % 3

        #pygame.display.update()

        imagerect.move_ip(1, 1)
        screen.fill(mygreen)
        screen.blit(myimage, imagerect)

        direHardLane = []
        direMidLane = []
        direEasyLane = []

        radiantHardLane = []
        radiantEasyLane = []
        radiantMidLane = []
        for i in range(32):
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

        n = 0
        if view == 0 or view ==1:
            for i in radiantHardLane:
                if n == 1 or n == 6 or n == 12 or n == 19:
                    addRect(screen, darkBlue, i, (20, 20))
                    addText(screen, darkBlue, i, n)
                else:
                    addRect(screen, red, i, (20, 20))
                    addText(screen, red, i, n)
                n += 1
            n = 0
            for i in radiantMidLane:
                if n == 1 or n == 5 or n == 9 or n == 13:
                    addRect(screen, darkBlue, i, (20, 20))
                    addText(screen, darkBlue, i, n)
                else:
                    addRect(screen, red, i, (20, 20))
                    addText(screen, red, i, n)
                n += 1
            n = 0
            for i in radiantEasyLane:
                #print(str(n) + " " + str(i))
                if n == 1 or n == 6 or n == 13 or n == 24:
                    addRect(screen, darkBlue, i, (20, 20))
                    addText(screen, darkBlue, i, n)
                else:
                    addRect(screen, red, i, (20, 20))
                    addText(screen, red, i, n)
                n += 1
        if view == 0 or view == 2:
            n = 0
            for i in direHardLane:
                if n == 1 or n == 6 or n == 12 or n == 19:
                    addRect(screen, darkBlue, i, (20, 20))
                    addText(screen, darkBlue, i, n)
                else:
                    addRect(screen, red, i, (20, 20))
                    addText(screen, red, i, n)
                n += 1
            n = 0
            for i in direMidLane:
                if n == 1 or n == 5 or n == 9 or n == 13:
                    addRect(screen, darkBlue, i, (20, 20))
                    addText(screen, darkBlue, i, n)
                else:
                    addRect(screen, red, i, (20, 20))
                    addText(screen, red, i, n)
                n += 1
            n = 0
            for i in direEasyLane:
                #print(str(n) + " " + str(i))
                if n == 1 or n == 6 or n == 13 or n == 24:
                    addRect(screen, darkBlue, i, (20, 20))
                    addText(screen, darkBlue, i, n)
                else:
                    addRect(screen, red, i, (20, 20))
                    addText(screen, red, i, n)
                n += 1

        # top-left: 300, 80                 top-right: 1000, 80
        # mid-left:
        # bot-left: 300, 620                bot-right: 1000, 620

        text = "FPS: {0:.2f}   Playtime: {1:.2f}".format(clock.get_fps(), playtime)
        pygame.display.set_caption(text)
        pygame.display.flip()

if __name__ == "__main__":
    main()

