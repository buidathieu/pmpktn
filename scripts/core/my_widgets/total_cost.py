from initialize import user_setting
import other_func as otf

import wx


class TotalCost(wx.TextCtrl):

    def __init__(self, parent):
        super().__init__(
            parent,
            value=otf.bill_int_to_str(user_setting['cong_kham_benh']))
        self.Bind(wx.EVT_CHAR, otf.only_nums)
        self.Bind(wx.EVT_TEXT, self._on_bill)
        self.Bind(wx.EVT_KILL_FOCUS, self._kill_focus)

    def _on_bill(self, e):
        val = int("".join(self.Value.split(".")))
        self.ChangeValue(otf.bill_int_to_str(val))
        self.SetInsertionPointEnd()

    def _kill_focus(self, e):
        if self.Value == '':
            self.ChangeValue('0')
