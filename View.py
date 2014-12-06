import pygame

def main():
    pygame.init()
    w = 1280
    h = 720
    screen_size = (w, h)
    screen = pygame.display.set_mode(screen_size, pygame.FULLSCREEN)
    background = pygame.Surface(screen.get_size())
    background.fill((0, 155, 0))
    # convert to make blitting faster
    background = background.convert()
    screen.blit(background, (0, 0))

    # some colours might be useful
    red = (255,0,0)
    green = (0,255,0)
    blue = (0,0,255)
    darkBlue = (0,0,128)
    white = (255,255,255)
    black = (0,0,0)
    pink = (255,200,200)

    myimage = pygame.image.load("randome.png")
    imagerect = myimage.get_rect()

    clock = pygame.time.Clock()
    FPS = 60
    playtime = 0.0
    mainloop = True

    while mainloop:
        milliseconds = clock.tick(FPS)
        playtime += milliseconds / 1000.0

        imagerect.move_ip(1, 1)
        screen.fill(black)
        screen.blit(myimage, imagerect)

        text = "FPS: {0:.2f}   Playtime: {1:.2f}".format(clock.get_fps(), playtime)
        pygame.display.set_caption(text)
        pygame.display.flip()
        for event in pygame.event.get():
            # User presses QUIT-button.
            if event.type == pygame.QUIT:
                mainloop = False
            elif event.type == pygame.KEYDOWN:
                # User presses ESCAPE-Key
                if event.key == pygame.K_ESCAPE:
                     mainloop = False

if __name__ == "__main__":
    main()

