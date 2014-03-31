#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pygame import *
import os

FINISHLINE_WIDTH = 64
FINISHLINE_HEIGHT = 640
FINISHLINE_COLOR = "#000000"

SNOWFLAKE_WIDTH = 32
SNOWFLAKE_HEIGHT = 32
SNOWFLAKE_COLOR = "#000000"

FLAG_WIDTH = 300
FLAG_HEIGHT = 16
FLAG_COLOR = "#000000"

ICON_DIR = os.path.dirname(__file__) #  Полный путь к каталогу с файлами

class FinishLine(sprite.Sprite):
    def __init__(self, x, y):
        sprite.Sprite.__init__(self)
        self.image = Surface((FINISHLINE_WIDTH, FINISHLINE_HEIGHT))
        self.image.fill(Color(FINISHLINE_COLOR))
        self.image = image.load("%s/images/finish.png" % ICON_DIR)
        self.image.set_colorkey(Color(FINISHLINE_COLOR))
        self.rect = Rect(x, y, FINISHLINE_WIDTH, FINISHLINE_HEIGHT)
        
class Snowflake(sprite.Sprite):
    def __init__(self, x, y):
        sprite.Sprite.__init__(self)
        self.image = Surface((SNOWFLAKE_WIDTH, SNOWFLAKE_HEIGHT))
        self.image.fill(Color(SNOWFLAKE_COLOR))
        self.image = image.load("%s/images/snowflake.png" % ICON_DIR)
        self.image.set_colorkey(Color(SNOWFLAKE_COLOR))
        self.rect = Rect(x, y, SNOWFLAKE_WIDTH, SNOWFLAKE_HEIGHT)

class FlagRed(sprite.Sprite):
    def __init__(self, x, y):
        sprite.Sprite.__init__(self)
        self.image = Surface((FLAG_WIDTH, FLAG_HEIGHT))
        self.image.fill(Color(FLAG_COLOR))
        self.image = image.load("%s/images/flagRed.png" % ICON_DIR)
        self.image.set_colorkey(Color(FLAG_COLOR))
        self.rect = Rect(x, y, SNOWFLAKE_WIDTH, SNOWFLAKE_HEIGHT)

class FlagBlue(sprite.Sprite):
    def __init__(self, x, y):
        sprite.Sprite.__init__(self)
        self.image = Surface((FLAG_WIDTH, FLAG_HEIGHT))
        self.image.fill(Color(FLAG_COLOR))
        self.image = image.load("%s/images/flagBlue.png" % ICON_DIR)
        self.image.set_colorkey(Color(FLAG_COLOR))
        self.rect = Rect(x, y, SNOWFLAKE_WIDTH, SNOWFLAKE_HEIGHT)