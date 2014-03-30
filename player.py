#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pygame import *
import pyganim
import os

MOVE_SPEED = 10
WIDTH = 32
HEIGHT = 32
COLOR =  "#888888"
ANIMATION_DELAY = 0.5 # скорость смены кадров
ICON_DIR = os.path.dirname(__file__) #  Полный путь к каталогу с файлами

ANIMATION_RIGHT = [('%s/images/hero_1.png' % ICON_DIR),
                   ('%s/images/hero_2.png' % ICON_DIR)]

class Player(sprite.Sprite):
    def __init__(self, x, y):
        sprite.Sprite.__init__(self)
        self.image = Surface((WIDTH,HEIGHT))
        self.rect = Rect(x, y, WIDTH, HEIGHT)
        self.image.set_colorkey(Color(COLOR))
        boltAnim = []
        for anim in ANIMATION_RIGHT:
            boltAnim.append((anim, ANIMATION_DELAY))
        self.boltAnimRight = pyganim.PygAnimation(boltAnim)
        self.boltAnimRight.play()
        self.winner = False
        

    def update(self, speed, finish):
        self.image.fill(Color(COLOR))
        self.boltAnimRight.blit(self.image, (0, 0))
        self.rect.x += speed
        if sprite.collide_rect(self, finish):
            self.winner = True


class LastPlayer(Player):
    def __init__(self,x,y):
        Player.__init__(self,x,y)

    def update(self, distance):
        self.image.fill(Color(COLOR))
        self.boltAnimRight.blit(self.image, (0, 0))
        self.rect.x = distance

