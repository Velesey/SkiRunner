# -*- coding: utf-8 -*-
from PyQt4.Qt import *
from PyQt4 import uic
import  os
import  sys
from dataManager import *

DIR = os.path.dirname(__file__) #  Полный путь к каталогу с файлами


class FormProfile(QMainWindow):

    def __init__(self):
        super(QMainWindow, self).__init__()
        uic.loadUi('%s/ui/frm_profile.ui' % DIR, self)
        self.cb_profile_load()
        self.te_newProfile.hide()
        self.bt_addProfile.hide()
        self.bt_cancel.hide()
        self.lb_add.hide()

        self.connect(self.bt_ok, SIGNAL("clicked()"), self.bt_ok_clicked)
        self.connect(self.bt_new, SIGNAL("clicked()"), self.bt_new_clicked)
        self.connect(self.bt_addProfile,SIGNAL("clicked()"), self.bt_addProfile_clicked)
        self.connect(self.bt_cancel, SIGNAL("clicked()"), self.bt_cancel_clicked)

        self.profileId = -1


    def bt_ok_clicked(self):
        self.profileId = self.cb_profile.itemData(self.cb_profile.currentIndex()).toString()
        self.formSpeed = FormDistance(self.profileId)
        self.formSpeed.show()

        self.hide()

    def bt_new_clicked(self):
        self.te_newProfile.show()
        self.bt_addProfile.show()
        self.lb_add.show()
        self.bt_cancel.show()
        self.lb_set.hide()
        self.cb_profile.hide()
        self.bt_ok.hide()
        self.bt_new.hide()

    def bt_addProfile_clicked(self):
        self.bt_cancel_clicked()

        name = u"%s" % self.te_newProfile.text()
        if name != "":
            dm = DataManager()
            dm.newProfile(name)

        self.cb_profile_load()

    def bt_cancel_clicked(self):
        self.te_newProfile.hide()
        self.bt_addProfile.hide()
        self.lb_add.hide()
        self.lb_set.show()
        self.cb_profile.show()
        self.bt_ok.show()
        self.bt_new.show()
        self.bt_cancel.hide()


    def cb_profile_load(self):
        self.cb_profile.clear()
        dm = DataManager()
        data = dm.getProfilesAndIds()
        for rec in data:
            id, name = rec
            self.cb_profile.addItem(name,id)


class FormDistance(QMainWindow):
    def __init__(self,profileId):
        super(QMainWindow, self).__init__()
        uic.loadUi('%s/ui/frm_distance.ui' % DIR, self)
        self.profileId = profileId
        self.distanceId = -1


        self.cb_distance_load()
        self.te_newDistance.hide()
        self.bt_addDistance.hide()
        self.bt_cancel.hide()
        self.lb_add.hide()

        self.connect(self.bt_new, SIGNAL("clicked()"), self.bt_new_clicked)
        self.connect(self.bt_cancel, SIGNAL("clicked()"), self.bt_cancel_clicked)
        self.connect(self.bt_addDistance,SIGNAL("clicked()"), self.bt_addDistance_clicked)
        self.connect(self.bt_ok, SIGNAL("clicked()"), self.bt_ok_clicked)



    def cb_distance_load(self):
        self.cb_distance.clear()
        dm = DataManager()
        data = dm.getDistancesAndIds()
        for rec in data:
            id, dist = rec
            self.cb_distance.addItem(str(dist),id)

    def bt_new_clicked(self):
        self.te_newDistance.show()
        self.bt_addDistance.show()
        self.lb_add.show()
        self.bt_cancel.show()
        self.lb_set.hide()
        self.cb_distance.hide()
        self.bt_ok.hide()
        self.bt_new.hide()

    def bt_cancel_clicked(self):
        self.te_newDistance.hide()
        self.bt_addDistance.hide()
        self.lb_add.hide()
        self.bt_cancel.hide()
        self.lb_set.show()
        self.cb_distance.show()
        self.bt_ok.show()
        self.bt_new.show()

    def bt_addDistance_clicked(self):
        self.bt_cancel_clicked()

        distance = u"%s" % self.te_newDistance.text()
        try:
            distance = int(distance)
            dm = DataManager()
            dm.newDistance(distance)
        except Exception as msg:
            print msg

        self.cb_distance_load()

    def bt_ok_clicked(self):
        self.distanceId = self.cb_distance.itemData(self.cb_distance.currentIndex()).toString()

        from SkiRun import *
        t1 = threading.Thread(target=main)
        t2 = threading.Thread(target=getDataFromSimulator)

        t2.start()
        t1.start()

        self.hide()



class App(QApplication):
    def __init__(self, *args):
        QApplication.__init__(self, *args)
        self.formProfile = FormProfile()
        self.formProfile.show()

def main(args):
    global app
    app = App(args)
    app.exec_()

if __name__ == "__main__":
    main(sys.argv)