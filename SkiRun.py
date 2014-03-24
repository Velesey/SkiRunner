#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Импортируем библиотеку pygame
import pygame
from pygame import *
from player import *
from dataManager import *
from object import  *
import time
from random import randint
import threading
import serial




WIN_WIDTH = 800 #Ширина создаваемого окна
WIN_HEIGHT = 640 # Высота
DISPLAY = (WIN_WIDTH, WIN_HEIGHT) # Группируем ширину и высоту в одну переменную
BACKGROUND_COLOR = "#F9FFF8"
CENTER_OF_SCREEN = WIN_WIDTH / 2, WIN_HEIGHT / 2
total_level_width = 100 * 60 + 64
total_level_height = WIN_HEIGHT

FILE_DIR = os.path.dirname(__file__)

valueFromSimulator = 0
isRunnig = True

class Camera(object):
    def __init__(self, camera_func, width, height):
        self.camera_func = camera_func
        self.state = Rect(0, 0, width, height)

    def apply(self, target):
        return target.rect.move(self.state.topleft)

    def update(self, target):
        self.state = self.camera_func(self.state, target.rect)

    def reverse(self, pos):# получение внутренних координат из глобальных
        return pos[0] - self.state.left, pos[1] - self.state.top


def camera_configure(camera, target_rect):
    l, t, _, _ = target_rect
    _, _, w, h = camera
    l, t = -l+WIN_WIDTH / 2, -t+WIN_HEIGHT / 2

    l = min(0, l)                           # Не движемся дальше левой границы
    l = max(-(camera.width-WIN_WIDTH), l)   # Не движемся дальше правой границы
    t = max(-(camera.height-WIN_HEIGHT), t) # Не движемся дальше нижней границы
    t = min(0, t)                           # Не движемся дальше верхней границы

    return Rect(l, t, w, h)


def main():
    global valueFromSimulator, isRunnig
    lastValueFromSimulator = 0
    pygame.init() # Инициация PyGame, обязательная строчка
    screen = pygame.display.set_mode(DISPLAY) # Создаем окошко
    pygame.display.set_caption("SKiRun") # Пишем в шапку
    bg = Surface((WIN_WIDTH, WIN_HEIGHT)) # Создание видимой поверхности
    entities = pygame.sprite.Group() # Все объекты
    heroes = pygame.sprite.Group() # Все объекты

    dm = DataManager()
    raceId = dm.newRace(dm.getCurrentProfileId(),dm.getCurrentDistanceId())
    total_level_width =dm.getRaceDistance(raceId) * 10 + 64


    timer = pygame.time.Clock()

    bg.fill(Color(BACKGROUND_COLOR))     # Заливаем поверхность сплошным цветом

    for i in range(1,100):
        snowflake = Snowflake(randint(1,total_level_width),randint(1,total_level_height))
        entities.add(snowflake)

    speed = 0
    hero = Player(0, 300)
    heroes.add(hero)
    lastHero = LastPlayer(1, 350)
    heroes.add(lastHero)
    currentTime = time.time()



    timer = pygame.time.Clock()

    camera = Camera(camera_configure, total_level_width, total_level_height)

    finish = FinishLine(total_level_width-64,0)
    heroes.add(finish)



    isSetCurrentTime  = False
    while not hero.winner: # Основной цикл программы
        timer.tick_busy_loop(60)


        speed = dm.getImpulse(valueFromSimulator)
        if speed > 0:
            dm.logSpeed(hero.rect.x,dm.getCurrentRaceId())
        if not isSetCurrentTime and dm.isRaceStart:
            currentTime = time.time()
            isSetCurrentTime = True
        try:
            distanceLastRace = dm.getLastRaceDistanceAtCurrentTime(dm.getLastRaceId(),currentTime)
        except:
            distanceLastRace = 0
            print("dm.getLastRaceDistanceAtCurrentTime error")


        for e in pygame.event.get(): # Обрабатываем события
            if e.type == QUIT:
                dm.closeDB()
                isRunnig = False


                raise SystemExit, "QUIT"



        for e in entities:
            screen.blit(e.image, camera.apply(e))
            e.rect.y+=1
            if e.rect.y >= WIN_HEIGHT:
                e.rect.y = 0

        for e in heroes:
            screen.blit(e.image, camera.apply(e))

        #center_offset = camera.reverse(CENTER_OF_SCREEN) # получаем координаты внутри длинного уровня
        hero.update(speed, finish) # передвижение
        lastHero.update(distanceLastRace)

        camera.update(hero) # центризируем камеру относительно персонаж

        heroSpeed = dm.speed
        font=pygame.font.Font(None,70)
        textSpeed=font.render(("Speed : %.2f  km\h || %.2f m\s "  % ((heroSpeed * 1000 / 3600), heroSpeed)), 1,(0,0,0))
        textDistance=font.render(("Distance: %s  m" % (hero.rect.x / 10)), 1,(0,0,0))
        textTime=font.render(("Time: %.2f " % (time.time() - currentTime)), 1,(0,0,0))

        screen.blit(textSpeed, (10,10))
        screen.blit(textDistance, (10,50))
        screen.blit(textTime, (10,90))
        pygame.display.update()     # обновление и вывод всех изменений на экран
        screen.blit(bg, (0, 0))      # Каждую итерацию необходимо всё перерисовывать
    dm.closeDB()
    isRunnig = False


def getDataFromSimulator():
    global valueFromSimulator, isRunnig
    ser = serial.Serial('/dev/ttyACM0', 9600)
    while isRunnig:
       value =  ser.readline()
       try:
           valueFromSimulator = int(value)
       except:
           pass




        
#if __name__ == "__main__":
#    main()


t1 = threading.Thread(target=main)
t2 = threading.Thread(target=getDataFromSimulator)

# start threads
t2.start()
t1.start()




