# -*- coding: utf-8 -*-

import sys
import os
from PyQt4.Qt import *
from PyQt4 import uic
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import timedelta
from dataManager import *
from matplotlib import rc
from mainForm import *



DIR = os.path.dirname(__file__)

DATEFORMAT = "%Y-%m-%d %H:%M:%S.%f"



class FormGraph(QMainWindow):
    def __init__(self,profileId):
        super(QMainWindow, self).__init__()
        uic.loadUi('%s/ui/frm_graph.ui' % DIR, self)
        self.profileId = profileId
        self.distanceId = -1
        self.cb_distance_load()
        self.move(QDesktopWidget().availableGeometry().center() - self.frameGeometry().center())


        self.connect(self.bt_averageSpeed, SIGNAL("clicked()"), self.bt_averageSpeed_clicked)
        self.connect(self.bt_averageTime, SIGNAL("clicked()"), self.bt_averageTime_clicked)
        self.connect(self.bt_distance, SIGNAL("clicked()"), self.bt_distance_clicked)
        self.connect(self.bt_back, SIGNAL("clicked()"), self.bt_back_clicked)

        #включаем кирилицу
        font = {'family': 'Droid Sans',
        'weight': 'normal',
        'size': 14}
        rc('font', **font)

    def cb_distance_load(self):
        self.cb_distance.clear()
        self.cb_distance.addItem(u"По всем дистанциям",-1)
        dm = DataManager()
        data = dm.getDistancesAndIds()
        for rec in data:
            id, dist = rec
            self.cb_distance.addItem(str(dist),id)



    def bt_distance_clicked(self):
        self.distanceId = int(self.cb_distance.itemData(self.cb_distance.currentIndex()).toString())
        dm = DataManager()
        minDate = datetime.today() - timedelta(days=30)
        dates = []
        distances = []
        for date in (minDate + timedelta(n) for n in range(33)):
            distance = 0
            data = dm.getRaceIdByDateAndProfileId(date,self.profileId)
            if data:
                print(data)
                for raceIds in data:
                    raceId = raceIds
                    distance += dm.getRaceDistance(raceId)
            distances.append(distance)
            dates.append(date)

        plt.plot_date(dates, distances,'b')
        plt.plot_date(dates, distances,'bo')
        distancesSum = sum(distances)
        plt.xlabel(u"Всего пройдено = %s м" % float(distancesSum))
        plt.ylabel(u"Пройдено в день (м)")
        plt.title(u"График пройденого расстояния профиля %s" % dm.getProfileNameById(self.profileId))
        plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%d/%m/%y'))
        plt.gcf().autofmt_xdate()
        plt.grid(True)
        plt.show()

    def bt_averageTime_clicked(self):
        self.distanceId = int(self.cb_distance.itemData(self.cb_distance.currentIndex()).toString())
        dm = DataManager()
        data = dm.getDatesAndRaceTimesAndRaceIdsByProfileId(self.profileId)
        dates = []
        times = []
        for rec in data:
           date, time, id = rec
           if date and time:
                if self.distanceId == -1:
                    dates.append(datetime.strptime(date,DATEFORMAT))
                    times.append(time)
                elif dm.getRaceDistance(id) == dm.getDistanceNameById(self.distanceId):
                        dates.append(datetime.strptime(date,DATEFORMAT))
                        times.append(time)

        plt.plot_date(dates, times,'b')
        plt.plot_date(dates, times,'bo')
        timesSum = sum(times)
        h = ((timesSum / 3600)) % 24
        m = (timesSum / 60) % 60
        s = timesSum % 60
        plt.xlabel(u"Всего времени = %s с или %d:%02d:%02d" % (timesSum,h,m,s))
        plt.ylabel(u"Время гонки (м/с)")
        plt.title(u"График времени гонки профиля %s" % dm.getProfileNameById(self.profileId))
        plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%d/%m/%y'))
        plt.gcf().autofmt_xdate()
        plt.grid(True)
        plt.show()

    def bt_averageSpeed_clicked(self):
        self.distanceId = int(self.cb_distance.itemData(self.cb_distance.currentIndex()).toString())
        dm = DataManager()
        data = dm.getDatesAndRaceTimesAndRaceIdsByProfileId(self.profileId)
        dates = []
        values = []
        for rec in data:
            date, time, id = rec
            if date and dm.getAverageSpeedByRace(id):
                if self.distanceId == -1:
                    dates.append(datetime.strptime(date,DATEFORMAT))
                    values.append(dm.getAverageSpeedByRace(id))
                elif dm.getRaceDistance(id) == dm.getDistanceNameById(self.distanceId):
                        dates.append(datetime.strptime(date,DATEFORMAT))
                        values.append(dm.getAverageSpeedByRace(id))

        plt.plot_date(dates, values,'b')
        plt.plot_date(dates, values,'bo')
        averageSpeed = len(values) > 0 and (lambda: sum(values) / len(values)) or (lambda: 0)
        plt.xlabel(u"Средняя-средняя скорость= %.2f м/с или %.2f км/ч" % (float(averageSpeed()),float(averageSpeed()) / 1000 * 3600))
        plt.ylabel(u"Средняя скорость (м/с)")
        plt.title(u"График скоростей профиля %s" % dm.getProfileNameById(self.profileId))
        plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%d/%m/%y'))
        plt.gcf().autofmt_xdate()
        plt.grid(True)
        plt.show()


    def bt_back_clicked(self):
        self.formProfile = FormProfile()
        self.formProfile.show()
        self.hide()

