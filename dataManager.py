#!/usr/bin/env python
# -*- coding: utf-8 -*-
from numpy.ma.core import _minimum_operation

import serial
import time
import MySQLdb
from datetime import datetime
from random import randint


STEP = 4.5 #метров
POWER_IMPULSE = 4
RESET_SPEED_TIME = 5

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
        self.currentRaceId = -1
        self.currentDistanceId = -1
        self.impulseMeter = 0

    def getImpulse(self, value):
        self.impulse = 0

        if self.time.time() - self.currentTime > RESET_SPEED_TIME:
            self.speed = 0
        self.value = value
        if self.value != self.lastValue:
            time = self.time.time() - self.currentTime
            self.impulse = POWER_IMPULSE
            self.isRaceStart = True

            self.speed = STEP / time # метры в секунду
            self.currentTime = self.time.time()
            self.lastValue = self.value
            self.impulseMeter+=1
            if self.impulseMeter >=2:
                self.impulse+=1# по аналогии високосного года
                self.impulseMeter = 0

        return  self.impulse * 10


    def getLastRaceDistanceAtCurrentTime(self, raceId,currentTime):
        lastRaceDistance = 0
        dateFormat = "%Y-%m-%d %H:%M:%S.%f"
        if  not self.isGetLastRaceSpeeds:

            sql = """SELECT min(date) FROM skirunner.runLog WHERE race_id = %s""" % raceId
            self.cursor.execute(sql)
            data = self.cursor.fetchall()
            for rec in data:
                self.lastRaceMinDate = datetime.strptime(rec[0],dateFormat)
            sql = """SELECT distance,date FROM skirunner.runLog WHERE race_id = %s ORDER BY date DESC""" % raceId
            self.cursor.execute(sql)
            self.dataLastRace = self.cursor.fetchall()
            self.isGetLastRaceSpeeds = True


        if self.isRaceStart:
            time = datetime.now() - datetime.fromtimestamp(currentTime)
            for rec in self.dataLastRace:
                distance, date = rec
                if time <= (datetime.strptime(date,dateFormat) - self.lastRaceMinDate):
                    lastRaceDistance = distance
        return  lastRaceDistance

    def getRaceDistance(self, raceId):
         sql = """SELECT distance FROM skirunner.distance  WHERE id =
                    (SELECT   id_distance FROM skirunner.race WHERE id = %s)""" % raceId
         self.cursor.execute(sql)
         result = self.cursor.fetchone()[0]
         return  result

    #TODO сделать выбор профиля
    def getCurrentProfileId(self):
        return 1

    #TODO сделать выбор дистанции забега
    def getCurrentDistanceId(self):
        if self.currentDistanceId != -1:
            return self.currentDistanceId
        return 2

    #TODO переделать. Если запускать разные профили, то ID меняется
    def getLastRaceId(self):
        if self.currentRaceId != -1:
            return  self.currentRaceId - 1
        sql = "SELECT max(id) FROM skirunner.race"
        self.currentRaceId = self.cursor.execute(sql)[0]
        return self.currentRaceId - 1

    def getCurrentRaceId(self):
        if self.currentRaceId != -1:
            return  self.currentRaceId
        sql = "SELECT max(id) FROM skirunner.race"
        self.currentRaceId = self.cursor.execute(sql)[0]
        return self.currentRaceId


    def newRace(self,profileId,distanceId):
        sql = """INSERT INTO race(id_user,id_distance)
        VALUES ('%s', '%s')
        """%(profileId,distanceId)
        self.cursor.execute(sql)
        self.db.commit()
        sql = "SELECT max(id) FROM skirunner.race"
        self.cursor.execute(sql)
        self.currentRaceId = self.cursor.fetchone()[0]
        return self.currentRaceId


    def closeDB(self):
        self.db.close()

    def commitDB(self):
        self.db.commit()

    def logSpeed(self,distance, raceId):
        sql = """INSERT INTO runLog(race_id,distance,date)
        VALUES ('%s', '%s', '%s')
        """%(raceId,distance,datetime.now())
        self.cursor.execute(sql)
        self.db.commit()




