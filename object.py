#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pygame import *
import os

ICON_DIR = os.path.dirname(__file__) #  Полный путь к каталогу с файлами

class Object(sprite.Sprite):
    def __init__(self, x, y):
        sprite.Sprite.__init__(self)
        self.color = "#000000"
        self.image = Surface((self.widht, self.height))
        self.image.fill(Color(self.color))
        self.rect = Rect(x, y, self.widht, self.height)

class FinishLine(Object):
    def __init__(self, x, y):
        self.widht = 64
        self.height = 640
        Object.__init__(self,x,y)
        self.image = image.load("%s/images/finish.png" % ICON_DIR)

class Snowflake(Object):
    def __init__(self, x, y):
        self.widht = 32
        self.height = 32
        Object.__init__(self,x,y)
        self.image = image.load("%s/images/snowflake.png" % ICON_DIR)


class FlagRed(Object):
    def __init__(self, x, y):
        self.widht = 300
        self.height = 16
        Object.__init__(self,x,y)
        self.image = image.load("%s/images/flagRed.png" % ICON_DIR)

class FlagBlue(Object):
    def __init__(self, x, y):
        self.widht = 300
        self.height = 16
        Object.__init__(self,x,y)
        self.image = image.load("%s/images/flagBlue.png" % ICON_DIR)