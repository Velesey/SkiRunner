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
from matplotlib.dates import  drange


DIR = os.path.dirname(__file__)

DATEFORMAT = "%Y-%m-%d %H:%M:%S.%f"



class FormGraph(QMainWindow):
    def __init__(self,profileId,distanceId):
        super(QMainWindow, self).__init__()
        uic.loadUi('%s/ui/frm_graph.ui' % DIR, self)
        self.profileId = profileId
        self.distanceId = distanceId
        self.cb_distance_load()

        self.connect(self.bt_averageSpeed, SIGNAL("clicked()"), self.bt_averageSpeed_clicked)
        self.connect(self.bt_averageTime, SIGNAL("clicked()"), self.bt_averageTime_clicked)
        self.connect(self.bt_distance, SIGNAL("clicked()"), self.bt_distance_clicked)

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
            distance = dm.getRaceDistance(dm.getRaceIdByDateAndProfileId(date,self.profileId))
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
        plt.xlabel(u"Всего времени = %s с" % float(timesSum))
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
        plt.xlabel(u"Средняя-средняя скорость= %.2f м/с" % float(averageSpeed()))
        plt.ylabel(u"Средняя скорость (м/с)")
        plt.title(u"График скоростей профиля %s" % dm.getProfileNameById(self.profileId))
        plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%d/%m/%y'))
        plt.gcf().autofmt_xdate()
        plt.grid(True)
        plt.show()



class App(QApplication):
    def __init__(self, *args):
        QApplication.__init__(self, *args)
        self.formGraph = FormGraph(1,1)
        self.formGraph.show()

def main(args):
    global app
    app = App(args)
    app.exec_()

if __name__ == "__main__":
    main(sys.argv)