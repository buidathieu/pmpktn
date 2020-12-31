from initialize import *
# import db_sql.db_func as dbf
# import other_func as otf
from .therapy_picker import TherapyPicker
from .therapy_list import TherapyList
from .core_func import onSaveTherapy, onEraseTherapy

import wx


class TherapyPage(wx.Panel):

    def __init__(self, parent):
        super().__init__(parent)
        self.therapy_picker = TherapyPicker(self)
        self.t_list = TherapyList(self)
        self.save_t_btn = self._createSaveTherapybtn()
        self.erase_t_btn = self._createEraseTherapybtn()
        self._setSizer()

    def _createSaveTherapybtn(self):
        btn = wx.BitmapButton(self, bitmap=wx.Bitmap(plus_bm))
        btn.Bind(wx.EVT_BUTTON, lambda e: onSaveTherapy(self))
        return btn

    def _createEraseTherapybtn(self):
        btn = wx.BitmapButton(self, bitmap=wx.Bitmap(minus_bm))
        btn.Bind(wx.EVT_BUTTON, lambda e: onEraseTherapy(self))
        return btn

    def _setSizer(self):
        row_1 = wx.BoxSizer(wx.HORIZONTAL)
        sizer = wx.BoxSizer(wx.VERTICAL)

        row_1.Add(self.therapy_picker, 1, wx.ALIGN_CENTER | wx.RIGHT, 5)
        row_1.Add(self.save_t_btn, 0, wx.ALIGN_CENTER | wx.RIGHT, 5)
        row_1.Add(self.erase_t_btn, 0, wx.ALIGN_CENTER | wx.RIGHT, 5)

        sizer.Add(row_1, 0, wx.EXPAND | wx.BOTTOM, 3)
        sizer.Add(self.t_list, 0, wx.EXPAND)
        self.SetSizer(sizer)
