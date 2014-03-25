# -*- coding: utf-8 -*-
from PyQt4 import QtCore, QtGui, uic
import  os
import  sys
from dataManager import *

DIR = os.path.dirname(__file__) #  Полный путь к каталогу с файлами


class FormProfile(QtGui.QMainWindow):

    def __init__(self):
        super(QtGui.QMainWindow, self).__init__()
        uic.loadUi('%s/ui/frm_profile.ui' % DIR, self)
        self.cb_profile_load()
        self.te_newProfile.hide()
        self.bt_addProfile.hide()
        self.bt_cancel.hide()
        self.lb_add.hide()

        self.connect(self.bt_ok, QtCore.SIGNAL("clicked()"), self.bt_ok_clicked)
        self.connect(self.bt_new, QtCore.SIGNAL("clicked()"), self.bt_new_clicked)
        self.connect(self.bt_addProfile, QtCore.SIGNAL("clicked()"), self.bt_addProfile_clicked)
        self.connect(self.bt_cancel, QtCore.SIGNAL("clicked()"), self.bt_cancel_clicked)

        self.show()

    def bt_ok_clicked(self):
        print("clickef")

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
        self.te_newProfile.hide()
        self.bt_addProfile.hide()
        self.lb_add.hide()
        self.lb_set.show()
        self.cb_profile.show()
        self.bt_ok.show()
        self.bt_new.show()
        self.bt_cancel.hide()


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


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    window = FormProfile()
    sys.exit(app.exec_())