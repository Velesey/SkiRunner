#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pygame import *
import os

WIDTH = 32
HEIGHT = 32
ICON_DIR = os.path.dirname(__file__)

ANIMATION = [('%s/images/hero_1.png' % ICON_DIR),
                   ('%s/images/hero_2.png' % ICON_DIR)]

class Player(sprite.Sprite):
    def __init__(self, x, y):
        sprite.Sprite.__init__(self)
        self.image = Surface((WIDTH,HEIGHT))
        self.rect = Rect(x, y, WIDTH, HEIGHT)
        self.winner = False
        self.animationState  = 0
        
    def update(self, speed, finish):
        if speed > 0:
            self.animationState+=1;
            if self.animationState == 2: self.animationState = 0
        self.image = image.load(ANIMATION[self.animationState])
        self.rect.x += speed
        if sprite.collide_rect(self, finish):
            self.winner = True

class LastPlayer(Player):
    def __init__(self,x,y):
        Player.__init__(self,x,y)
        self.lastDistance = 0

    def update(self, distance):
        if self.lastDistance != distance:
            self.animationState+=1;
            if self.animationState == 2: self.animationState = 0
        self.lastDistance = distance
        self.image = image.load(ANIMATION[self.animationState])
        self.rect.x = distance

