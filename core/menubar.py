from initialize import *

import webbrowser
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

        patientmenu = wx.Menu()
        menuNewPatient = patientmenu.Append(id_new_patient, "Bệnh nhân mới\tF1")
        menuEditPatient = patientmenu.Append(id_edit_patient, "Chỉnh sửa thông tin bệnh nhân\tF2")
        menuSaveVisit = patientmenu.Append(id_save_visit, "Lưu/Cập nhật lượt khám\tF3")

        self.Append(homeMenu, "Home")
        self.Append(patientmenu, "Bệnh nhân")

        self.Bind(wx.EVT_MENU, lambda e: self.mv.refresh(), menuRefresh)
        self.Bind(wx.EVT_MENU, lambda e: webbrowser.open(r"https://github.com/vuongkienthanh/pmpktn"), menuAbout)
        self.Bind(wx.EVT_MENU, lambda e: self.mv.Close(), menuExit)
        self.Bind(wx.EVT_MENU, lambda e: self.mv.onCreateNewPatient(), menuNewPatient)
        self.Bind(wx.EVT_MENU, lambda e: self.mv.onEditPatientInfo(), menuEditPatient)
        self.Bind(wx.EVT_MENU, lambda e: self.mv.onSaveVisit(), menuSaveVisit)
