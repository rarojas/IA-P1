#! usr/bin/env python

import pygame, sys, os
from pygame.locals import *
import time
pygame.mixer.init()
import os, pygame.mixer
pygame.font.init

class Game:
    def __init__(self):
        self.FRAME_RATE = 30

        self.x_offset = 0
        self.y_offset = 0

        #self.level = Level()
        #self.calcGridOffsets()

        self.current_level = 1
        self.lives = 5

        self.animation_offset_x = 0
        self.animation_offset_y = 0

        self.stop_moving = False
        self.restart = False
        self.floor_block = pygame.image.load(os.path.join("assets","Floor.gif"))

        pygame.init()
        self.screen = pygame.display.set_mode((640, 480))
        pygame.display.set_caption('Labryinth')
        pygame.mouse.set_visible(0)
        pygame.display.init()


    def drawLevel(self):
        self.screen.blit(self.floor_block, (32, 32))

    def update(self):
        self.drawLevel()

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            if (event.type == KEYDOWN):
                if (event.key == K_ESCAPE):
                    pygame.quit()
                    sys.exit()

    def main(self):
        while(True):
            test = Game()
            while True:
                test.update()
                time.sleep(1 / test.FRAME_RATE)

game = Game()
game.main()
