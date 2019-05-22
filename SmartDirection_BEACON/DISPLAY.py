#!/usr/bin/env python
import pygame
import keyboard


class DisplayArrow:
    def __init__(self, arrow_display, wait, display_Ready_q):

        self.arrow_display=arrow_display
        self.wait=wait
        self.display_Ready_q=display_Ready_q

    def Go(self):
        ################# PYGAME SETTING #############
        #   pygame init
        pygame.init()
        #   display setting
        display_width = 1100
        display_height = 800
        #   rgb color
        black = (0, 0, 0)
        white=(1,1,1)
        # setting
        #gameDisplay=pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        gameDisplay = pygame.display.set_mode((display_width, display_height))
        gameDisplay.fill(white)
        pygame.display.set_caption('A  bit Racey')
        clock = pygame.time.Clock()

        print("DISPLAY READY\n")
        self.display_Ready_q.put("ready")
        gameDisplay.fill(black) 
        ############# INFINITE LOOP ##############
        while True:
            if keyboard.is_pressed('z'):
                pygame.quit()
            ### WAITING FOR DATA INFO ###
            if not self.arrow_display.empty():
                
                if keyboard.is_pressed('z'):
                    pygame.quit()

                arrow = self.arrow_display.get()
                # DIRECTION AND COLOR
                direction = arrow["direction"]
                color = arrow["color"]

                # DOWNLOADING ARROW IMAGINE
                directory = "arrow/Tot/"
                
                arrowImg = pygame.image.load(str(directory) + str(color) + "_" + str(direction) + ".png")  # loading of the image, that have to be in the same directory of the script, or we have to put the path

                # ARROW STARTING POINT
                if direction == "sx":
                    x = (700)
                    y = (100)
                elif direction == "dx":
                    x = (200)
                    y = (100)
                elif direction == "up":
                    x = (400)
                    y = (500)
                elif direction == "back":
                    x = (400)
                    y = (-200)


                # QUIT COMMAND
                crashed = False

                # MOVEMENT AND UPADATE ARROW'S LOOP
                while not crashed:
                    if keyboard.is_pressed('z'):
                        pygame.quit()

                    # QUIT event
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            crashed = True

                    # UPDATE ARROW
                    if direction == "sx":
                        x_change = -5
                        x += x_change

                    elif direction == "dx":
                        x_change = 5
                        x += x_change

                    elif direction == "up":
                        y_change = -5
                        y += y_change

                    elif direction == "back":
                        y_change = 5
                        y += y_change

                    gameDisplay.fill(black)
                    gameDisplay.blit(arrowImg, (x, y))

                    # QUIT definition
                    if x >= 600 and direction == "dx":
                        x = 200
                        crashed = True

                    elif x <= 200 and direction == "sx":
                        x = 700

                        crashed = True

                    elif y <= -0 and direction == "up":
                        y = 250

                        crashed = True

                    elif y >= 400 and direction == "back":
                        y = -200

                        crashed = True

                    pygame.display.update()

                    #  ARROW VELOCITY
                    clock.tick(200)

                # AREADY FOR THE NEXT ARROW
                self.wait.put("go")
                gameDisplay.fill(black)
                pygame.display.update()



