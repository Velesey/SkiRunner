#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import MySQLdb
from datetime import datetime

STEP = 4 #метров
POWER_IMPULSE = STEP
RESET_SPEED_TIME = 3

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
        self.currentProfileId = -1
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

        return  self.impulse

    def getLastRaceDistanceAtCurrentTime(self, raceId,currentTime):
        lastRaceDistance = 0
        dateFormat = "%Y-%m-%d %H:%M:%S.%f"
        if  not self.isGetLastRaceSpeeds:

            sql = """SELECT min(date) FROM runLog WHERE race_id = %s""" % raceId
            self.cursor.execute(sql)
            data = self.cursor.fetchall()
            for rec in data:
                self.lastRaceMinDate = datetime.strptime(rec[0],dateFormat)
            sql = """SELECT distance,date FROM runLog WHERE race_id = %s ORDER BY date DESC""" % raceId
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
         sql = """SELECT distance FROM distance  WHERE id =
                    (SELECT   id_distance FROM race WHERE id = %s)""" % raceId
         self.cursor.execute(sql)
         try:
            data = self.cursor.fetchone()[0]
         except:
            data = 0
         return data

    def getLastRaceId(self, profileId):
        sql = """SELECT max(id) FROM race
            WHERE id_user = %s
            AND id != (SELECT max(id) FROM race
            WHERE id_user = %s)""" % (profileId, profileId)
        self.cursor.execute(sql)
        data = self.cursor.fetchone()[0]
        return data

    def getCurrentRaceId(self):
        if self.currentRaceId != -1:
            return  self.currentRaceId
        sql = "SELECT max(id) FROM race"
        self.currentRaceId = self.cursor.execute(sql)[0]
        return self.currentRaceId

    def newRace(self,profileId,distanceId):
        sql = """INSERT INTO race(id_user,id_distance)
        VALUES ('%s', '%s')
        """%(profileId,distanceId)
        self.cursor.execute(sql)
        self.db.commit()
        sql = "SELECT max(id) FROM race"
        self.cursor.execute(sql)
        self.currentRaceId = self.cursor.fetchone()[0]
        return self.currentRaceId

    def getProfilesAndIds(self):
        sql = "SELECT * FROM user"
        self.cursor.execute(sql)
        data = self.cursor.fetchall()
        return data

    def getDistancesAndIds(self):
        sql = "SELECT * FROM distance"
        self.cursor.execute(sql)
        data = self.cursor.fetchall()
        return data

    def newProfile(self,name):
        sql = """INSERT INTO user(name)
        VALUES ('%s')
        """%(name)
        self.cursor.execute(sql)
        self.db.commit()

    def newDistance(self,distance):
        sql = """INSERT INTO distance(distance)
        VALUES ('%s')
        """%(distance)
        self.cursor.execute(sql)
        self.db.commit()

    def closeDB(self):
        self.db.close()

    def commitDB(self):
        self.db.commit()

    #TODO Если будет тормозить, комитить после окончания бега
    def logSpeed(self,distance, raceId):
        sql = """INSERT INTO runLog(race_id,distance,date)
        VALUES ('%s', '%s', '%s')
        """%(raceId,distance,datetime.now())
        self.cursor.execute(sql)
        self.db.commit()

    def getAverageSpeedByRace(self, raceId):
        sql = """SELECT (SELECT distance FROM distance
                WHERE id = (SELECT id_distance FROM race WHERE id = %s))
                 / TIME_TO_SEC(TIMEDIFF(max(date), min(date))) AS race_time FROM runLog
                where race_id = %s""" % (raceId,raceId)
        self.cursor.execute(sql)
        averageSpeedByRace = self.cursor.fetchone()[0]
        return averageSpeedByRace

    def getProfileNameById(self,profileId):
        sql = "SELECT name FROM user WHERE id=%s" % profileId
        self.cursor.execute(sql)
        data = self.cursor.fetchone()[0]
        return data

    def getDistanceNameById(self,distanceId):
        sql = "SELECT distance FROM distance WHERE id=%s" % distanceId
        self.cursor.execute(sql)
        data = self.cursor.fetchone()[0]
        return data

    def getDatesAndRaceTimesAndRaceIdsByProfileId(self,profileId):
        sql = """SELECT
            (SELECT max(date) FROM runLog WHERE race_id = race.id),
            (SELECT TIME_TO_SEC(TIMEDIFF(max(date), min(date))) AS race_time FROM runLog WHERE race_id = race.id),
             race.id
             FROM race
             WHERE race.id_user = %s""" % profileId
        self.cursor.execute(sql)
        data = self.cursor.fetchall()
        return data

    def getRaceIdByDateAndProfileId(self, date, profileId):
        dateformat = '%Y-%m-%d'
        sql = """SELECT id FROM race
            WHERE id_user = %s
            AND id IN (SELECT DISTINCT race_id FROM runLog
            WHERE DATE(date) = STR_TO_DATE('%s', '%s'))""" % (profileId,date,dateformat)
        self.cursor.execute(sql)
        data = self.cursor.fetchall()
        return data






