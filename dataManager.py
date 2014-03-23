#!/usr/bin/env python
# -*- coding: utf-8 -*-
from numpy.ma.core import _minimum_operation

import serial
import time
import MySQLdb
from datetime import datetime
from random import randint


STEP = 2.25 #метров


class DataManager:
    def __init__(self):
        self.time = time
        self.currentTimeForLastRace = datetime.now()
        self.currentTime = self.time.time()
        self.speed = 0
        self.db = MySQLdb.connect(host="localhost", user="root", passwd="root", db="skirunner", charset='utf8')
        self.cursor = self.db.cursor()
        self.isGetLastRaceSpeeds = False
        self.dataLastRace = []
        self.lastRaceMinDate = datetime.now()
        self.value = 0
        self.lastValue = 0
        self.impulse = 0
        self.isRaceStart = False

    def getImpulse(self, value):
        self.impulse = 0
        #if self.isFirstRound:
        #    self.value = value
        #    self.lastValue = self.value
        #    self.isFirstRound = False

        if self.time.time() - self.currentTime > 5:
            self.speed = 0
        self.value = value
        if self.value != self.lastValue:
            time = self.time.time() - self.currentTime
            self.impulse = 2
            self.isRaceStart = True

            self.speed = STEP / time # метры в секунду
            self.currentTime = self.time.time()
            self.lastValue = self.value
        #self.speed = speed / 1000 * 3600 #км в час
        #print ("m/s " + str(speed))
        #self.dm.logSpeed(self.speed)
        #print self.speed
        return  self.impulse * 10


    def getLastRaceSpeed(self, raceId):
        dateFormat = "%Y-%m-%d %H:%M:%S.%f"
        if  not self.isGetLastRaceSpeeds:
            self.isGetLastRaceSpeeds = True
            sql = """SELECT min(date) FROM skirunner.runLog WHERE race_id = %s""" % raceId
            self.cursor.execute(sql)
            data = self.cursor.fetchall()
            for rec in data:
                self.lastRaceMinDate = datetime.strptime(rec[0],dateFormat)
            sql = """SELECT speed,date FROM skirunner.runLog WHERE race_id = %s ORDER BY date DESC""" % raceId
            self.cursor.execute(sql)
            self.dataLastRace = self.cursor.fetchall()
            self.currentTimeForLastRace = datetime.now()

        if self.isRaceStart:
            time = datetime.now() - self.currentTimeForLastRace
            result = 0
            for rec in self.dataLastRace:
                speed, date = rec
                if time <= (datetime.strptime(date,dateFormat) - self.lastRaceMinDate):
                    result = speed
            return  result
        return 0


    def closeDB(self):
        self.db.close()

    def commitDB(self):
        self.db.commit()

    def logSpeed(self,speed):
        sql = """INSERT INTO runLog(race_id,speed,date)
        VALUES ('1', '%s', '%s')
        """%(speed,datetime.now())
        #print(sql)
        self.cursor.execute(sql)
        #self.db.commit()


# класс заглушка
class DummyDataManager:
    def __init__(self):
        self.time = time
        self.currentTime = self.time.time()
        self.speed = 0
        pass
        self.timeDummy = 0
        self.dm = DataManager()
        self.tt = 0

    def getSpeed(self):
        self.timeDummy+=1
        if self.tt == 0:  self.tt = randint(25,100)
        if self.timeDummy > self.tt:
            self.timeDummy = 0
            self.tt = 0
            time = self.time.time() - self.currentTime
            self.currentTime =  self.time.time()
            self.speed = STEP / time # метры в секунду
            #self.speed = speed / 1000 * 3600 #км в час
            #print ("m/s " + str(speed))
            #self.dm.logSpeed(self.speed)
        return  self.speed # скрость оставим такой, а расстояние надо умножать на 60

    def closeDB(self):
        self.dm.commitDB()
        self.dm.closeDB()

    def getLastRaceSpeed(self, raceId):
        return  self.dm.getLastRaceSpeed(raceId)



#dm = DataManager()
#dm.getLastRaceSpeed(1)cute(sql)
        #self.db.commit()


