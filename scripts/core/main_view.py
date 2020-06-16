from initialize import *
from .left_panel import *
from .right_panel import *

from .menubar import MyMenuBar
from .accel import my_accel
from .binding import button_bindings

from .core_func import onPatientSelect, onPatientDeselect, onVisitSelect, onVisitDeselect
import wx
import logging


class MainView(wx.Frame):

    def __init__(self, parent, staff_id, *args, **kw):

        self._patient = None
        self._visit = None
        self.staff_id = staff_id
        self.sess = Session()
        logging.debug("Mainview initialized, session opened")

        super().__init__(
            parent,
            title='APP PHÒNG MẠCH TƯ, created by thanhstardust@outlook.com',
            pos=(0, 20), size=window_size, *args, **kw)
        self.SetBackgroundColour(wx.Colour(206, 219, 186))

        self._createInterface()
        self._setMenuBar()
        self._setAccelTable()
        button_bindings(self)
        self.Bind(wx.EVT_CLOSE, self.onClose)

    def _createInterface(self):
        create_left_panel_widgets(self)
        create_right_panel_widgets(self)

        left_panel = create_left_panel_sizer(self)
        right_panel = create_right_panel_sizer(self)

        whole_panel = wx.BoxSizer(wx.HORIZONTAL)
        whole_panel.Add(left_panel, 0, wx.EXPAND)
        whole_panel.Add(right_panel, 0,
                        wx.EXPAND | wx.LEFT | wx.RIGHT | wx.BOTTOM, 10)
        self.SetSizer(whole_panel)

    def _setMenuBar(self):
        self.menubar = MyMenuBar(self)
        self.SetMenuBar(self.menubar)

    def _setAccelTable(self):
        self.SetAcceleratorTable(my_accel)

    @property
    def patient(self):
        return self._patient

    @patient.setter
    def patient(self, p):
        self._patient = p
        logging.debug(f'Set mainview patient = {p}')
        if p:
            onPatientSelect(self, p)
        else:
            self.visit = None
            onPatientDeselect(self)

    @property
    def visit(self):
        return self._visit

    @visit.setter
    def visit(self, v):
        self._visit = v
        logging.debug(f'Set mainview visit = {v}')
        if v:
            onVisitSelect(self, v)
        else:
            onVisitDeselect(self)

    def Refresh(self):
        self.book.Refresh()
        self.patient = None

    def onClose(self, e):
        dlg = wx.MessageDialog(
            self, "Kết thúc", "Close app?", style=wx.OK | wx.CANCEL)
        if dlg.ShowModal() == wx.ID_OK:
            self.Destroy()

    def Destroy(self):
        logging.debug('Mainview destroyed, session closed')
        self.sess.commit()
        self.sess.close()
        super().Destroy()
