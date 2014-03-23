#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pygame import *
import pyganim
import os

MOVE_SPEED = 10
WIDTH = 22
HEIGHT = 32
COLOR =  "#888888"
ANIMATION_DELAY = 0.1 # скорость смены кадров
ICON_DIR = os.path.dirname(__file__) #  Полный путь к каталогу с файлами

ANIMATION_RIGHT = [('%s/mario/r1.png' % ICON_DIR),
            ('%s/mario/r2.png' % ICON_DIR),
            ('%s/mario/r3.png' % ICON_DIR),
            ('%s/mario/r4.png' % ICON_DIR),
            ('%s/mario/r5.png' % ICON_DIR)]

class Player(sprite.Sprite):
    def __init__(self, x, y):
        sprite.Sprite.__init__(self)
        self.xvel = 0   #скорость перемещения. 0 - стоять на месте
        self.startX = x # Начальная позиция Х, пригодится когда будем переигрывать уровень
        self.startY = y
        self.image = Surface((WIDTH,HEIGHT))
        self.image.fill(Color(COLOR))
        self.rect = Rect(x, y, WIDTH, HEIGHT) # прямоугольный объект
        self.image.set_colorkey(Color(COLOR)) # делаем фон прозрачным
#        Анимация движения вправо
        boltAnim = []
        for anim in ANIMATION_RIGHT:
            boltAnim.append((anim, ANIMATION_DELAY))
        self.boltAnimRight = pyganim.PygAnimation(boltAnim)
        self.boltAnimRight.play()

        self.winner = False
        

    def update(self, speed, finish):

        self.xvel = round(speed)

        self.image.fill(Color(COLOR))

        self.boltAnimRight.blit(self.image, (0, 0))
        #if speed == 0:
         #   self.boltAnimRight.pause()
        #else:
        self.boltAnimRight.play()

        self.rect.x += self.xvel # переносим свои положение на xvel
        if sprite.collide_rect(self, finish):
            self.winner = True



