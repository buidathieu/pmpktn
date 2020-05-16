# -*- coding: utf-8 -*-

from initialize import *
from .left_panel import LeftPanel
from .right_panel import RightPanel
from .menubar import MyMenuBar
import db_sql.db_func as dbf

import wx


class Mainview(wx.Frame):

    def __init__(self, parent, *args, **kw):

        self.patient = None
        self.visit = None
        self.sess = Session()

        super().__init__(parent, title='APP PHÒNG MẠCH TƯ, created by thanhstardust@outlook.com', pos=(0, 20),
                         *args, **kw)
        self.SetBackgroundColour(wx.Colour(206, 219, 186))

        self._createInterface()
        self._createMenuBar()
        self._createAccelTable()
        self.Bind(wx.EVT_CLOSE, self.onClose)
        self.Show()

    def _createInterface(self):
        self.left = LeftPanel(self)
        self.right = RightPanel(self)

        wholepanel = wx.BoxSizer(wx.HORIZONTAL)
        wholepanel.Add(self.left, 0, wx.EXPAND)
        wholepanel.Add(self.right, 0, wx.EXPAND | wx.LEFT | wx.RIGHT, 10)
        self.SetSizerAndFit(wholepanel)

    def _createMenuBar(self):
        self.menubar = MyMenuBar(self)
        self.SetMenuBar(self.menubar)

    def _createAccelTable(self):
        accel = wx.AcceleratorTable(
            [wx.AcceleratorEntry(wx.ACCEL_NORMAL, wx.WXK_F1, id_new_patient),
             wx.AcceleratorEntry(wx.ACCEL_NORMAL, wx.WXK_F2, id_new_visit),
             wx.AcceleratorEntry(wx.ACCEL_NORMAL, wx.WXK_F3, id_save_visit),
             wx.AcceleratorEntry(wx.ACCEL_NORMAL, wx.WXK_F5, wx.ID_REFRESH),
             wx.AcceleratorEntry(wx.ACCEL_ALT, wx.WXK_F4, wx.ID_EXIT)])
        self.SetAcceleratorTable(accel)

    def Refresh(self):
        self.left.Refresh()
        self.right.Refresh()
        self.patient = None
        self.visit = None

    def onClose(self, e):
        dlg = wx.MessageDialog(
            self, "Kết thúc", "Close app?", style=wx.OK | wx.CANCEL)
        if dlg.ShowModal() == wx.ID_OK:
            self.sess.close()
            e.Skip()


def mainloop():
    app = wx.App()
    Mainview(None)
    app.MainLoop()
