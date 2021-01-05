from initialize import *
from database.make_db import make_db
from database.sampling import populate_db
import os
import webbrowser
import subprocess
import shutil
import datetime as dt
import wx


class MyMenuBar(wx.MenuBar):

    def __init__(self, mv):
        super().__init__()
        self.mv = mv
        self._createMenu()

    def _createMenu(self):
        homeMenu = wx.Menu()
        menuRefresh = homeMenu.Append(wx.ID_REFRESH, "Refresh\tF5")
        menuAbout = homeMenu.Append(wx.ID_ABOUT)
        menuExit = homeMenu.Append(wx.ID_EXIT, "Exit\tALT+F4")

        patientMenu = wx.Menu()
        menuNewPatient = patientMenu.Append(id_new_patient, "Bệnh nhân mới\tF1")
        menuEditPatient = patientMenu.Append(id_edit_patient, "Chỉnh sửa thông tin bệnh nhân\tF2")
        menuSaveVisit = patientMenu.Append(id_save_visit, "Lưu/Cập nhật lượt khám\tF3")

        settingMenu = wx.Menu()
        dbMenu = wx.Menu()
        menuSQLiteGUI = settingMenu.Append(wx.ID_ANY, "SQLiteGUI")
        opendbMenu = dbMenu.Append(wx.ID_ANY, "Mở folder database")
        createdbMenu = dbMenu.Append(wx.ID_ANY, "Tạo database")
        populatedbMenu = dbMenu.Append(wx.ID_ANY, "Thêm mẫu vào database")
        deletedbMenu = dbMenu.Append(wx.ID_ANY, "Xoá database (có backup)")
        settingMenu.Append(wx.ID_ANY, "Database...", dbMenu)
        menuUser_setting = settingMenu.Append(wx.ID_ANY, "user_setting")

        self.Append(homeMenu, "Home")
        self.Append(patientMenu, "Bệnh nhân")
        self.Append(settingMenu, "Cài đặt")

        self.Bind(wx.EVT_MENU, lambda e: self.mv.refresh(), menuRefresh)
        self.Bind(wx.EVT_MENU, lambda e: webbrowser.open(r"https://github.com/vuongkienthanh/pmpktn"), menuAbout)
        self.Bind(wx.EVT_MENU, lambda e: self.mv.Close(), menuExit)
        self.Bind(wx.EVT_MENU, lambda e: self.mv.onCreateNewPatient(), menuNewPatient)
        self.Bind(wx.EVT_MENU, lambda e: self.mv.onEditPatientInfo(), menuEditPatient)
        self.Bind(wx.EVT_MENU, lambda e: self.mv.onSaveVisit(), menuSaveVisit)
        self.Bind(wx.EVT_MENU, self.openSQLiteGUI, menuSQLiteGUI)
        self.Bind(wx.EVT_MENU, lambda e: subprocess.Popen(["open", os.path.join(os.path.dirname(SQLITE_PATH), "user_setting.json")]), menuUser_setting)
        self.Bind(wx.EVT_MENU, lambda e: subprocess.Popen(["open", os.path.dirname(SQLITE_PATH)]), opendbMenu)
        self.Bind(wx.EVT_MENU, lambda e: self.onCreateDB(), createdbMenu)
        self.Bind(wx.EVT_MENU, lambda e: self.onPopulateDB(), populatedbMenu)
        self.Bind(wx.EVT_MENU, lambda e: self.onDeleteDB(), deletedbMenu)

    def openSQLiteGUI(self, e):
        ans = wx.MessageBox(
            "Đây là đường dẫn đến file database sqlite của phần mềm.\n\n"
            + SQLITE_PATH + "\n\n"
            + "Bạn có thể dùng những phần mềm như SQLiteStudio để truy cập vào nó.\n\n"
            + "Nhấn OK để copy đường dẫn")
        if ans == wx.OK:
            txt = wx.TextDataObject(SQLITE_PATH)
            if wx.TheClipboard.Open():
                wx.TheClipboard.SetData(txt)
                wx.TheClipboard.Close()

    def onCreateDB(self):
        if os.path.exists(SQLITE_PATH):
            wx.MessageBox('Database existed, couldnt create a new one.')
        else:
            make_db()
            wx.MessageBox('New database created.')

    def onPopulateDB(self):
        if os.path.exists(SQLITE_PATH):
            populate_db()
            wx.MessageBox('Database populated.')
        else:
            wx.MessageBox("Couldnt find database.")

    def onDeleteDB(self):
        if os.path.exists(SQLITE_PATH):
            shutil.copy(SQLITE_PATH, SQLITE_PATH + dt.datetime.now().strftime("%Y%m%d_%H%M%S") + '.bak')
            self.mv.sess.close()
            os.remove(SQLITE_PATH)
            make_db()
            self.mv.sess = Session()
            wx.MessageBox('Database backed up, deleted and newly created.')
        else:
            wx.MessageBox("Couldnt find database.")
