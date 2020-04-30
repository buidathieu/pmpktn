
from initialize import *
from core.__init__ import *
from core.left_panel import *
from core.visit_info import Visit_Info_Panel
from core.basic_info import Basic_Info_Panel
from core.menubar import MyMenuBar
from db_sql.__init__ import Session
import db_sql.db_func as dbf
import wx


class Mainview(wx.Frame):

    def __init__(self, parent, *args, **kw):

        self._patient = None
        self._visit = None
        self.sess = Session()

        super().__init__(parent, title='APP PHÒNG MẠCH TƯ, created by thanhstardust@outlook.com', pos=(0, 20),
                         *args, **kw)
        self.SetBackgroundColour(wx.Colour(206, 219, 186))

        self._createInterface()
        self._setMenuBar()
        self._setAccelTable()
        self.Bind(wx.EVT_CLOSE, self.onClose)

    def _createInterface(self):
        self.book = PatientBook(self)
        self.searchctrl = SearchCtrl(self)
        self.visit_list = VisitList(self)
        self.basic_info = Basic_Info_Panel(self)
        self.visit_info = Visit_Info_Panel(self)

        leftpanel = wx.BoxSizer(wx.VERTICAL)
        leftpanel.Add(self.book, 10, wx.LEFT | wx.TOP, 10)
        leftpanel.Add(self.searchctrl, 0, wx.EXPAND | wx.LEFT | wx.BOTTOM, 15)
        leftpanel.Add(wx.StaticText(
            self, label='Lượt khám cũ:'), 0, wx.LEFT, 20)
        leftpanel.Add(self.visit_list, 4, wx.EXPAND | wx.LEFT | wx.BOTTOM, 10)

        rightpanel = wx.BoxSizer(wx.VERTICAL)
        rightpanel.Add(self.basic_info, 0, wx.EXPAND)
        rightpanel.Add(self.visit_info, 1, wx.EXPAND)

        wholepanel = wx.BoxSizer(wx.HORIZONTAL)
        wholepanel.Add(leftpanel, 0, wx.EXPAND)
        wholepanel.Add(rightpanel, 0, wx.EXPAND | wx.LEFT | wx.RIGHT, 10)
        self.SetSizerAndFit(wholepanel)

    def _setMenuBar(self):
        self.menubar = MyMenuBar(self)
        self.SetMenuBar(self.menubar)

    def _setAccelTable(self):
        accel = wx.AcceleratorTable(
            [wx.AcceleratorEntry(wx.ACCEL_NORMAL, wx.WXK_F1, id_new_patient),
             wx.AcceleratorEntry(wx.ACCEL_NORMAL, wx.WXK_F2, id_new_visit),
             wx.AcceleratorEntry(wx.ACCEL_NORMAL, wx.WXK_F3, id_save_visit),
             wx.AcceleratorEntry(wx.ACCEL_NORMAL, wx.WXK_F5, wx.ID_REFRESH),
             wx.AcceleratorEntry(wx.ACCEL_ALT, wx.WXK_F4, wx.ID_EXIT)])
        self.SetAcceleratorTable(accel)

    @property
    def patient(self):
        return self._patient

    @patient.setter
    def patient(self, p):
        self._patient = p
        if p:
            self.basic_info.Update()
            self.visit_list.Update()
            if p.visits.count() > 0:
                self.visit_list.Select(0)
        else:
            self.basic_info.Clear()
            self.visit_list.Clear()
            self.visit_info.Clear()

    @property
    def visit(self):
        return self._visit

    @visit.setter
    def visit(self, v):
        self._visit = v
        if v:
            self.visit_info.Update()
        else:
            self.visit_info.Clear()

    def Refresh(self):
        self.book.ChangeSelection(0)
        idx = self.book.GetPage(0).GetFirstSelected()
        self.book.GetPage(0).Select(idx, 0)
        self.searchctrl.Clear()

    def onClose(self, e):
        dlg = wx.MessageDialog(self, "", "Close app?", style=wx.OK | wx.CANCEL)
        if dlg.ShowModal() == wx.ID_OK:
            e.Skip()
            self.sess.close()
