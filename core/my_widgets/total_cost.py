from initialize import user_setting
import other_func as otf

import wx


class TotalCost(wx.TextCtrl):

    def __init__(self, parent):
        super().__init__(
            parent,
            value=otf.bill_int_to_str(user_setting['cong_kham_benh']))
        self.Bind(wx.EVT_CHAR, otf.only_nums)
        self.Bind(wx.EVT_TEXT, self._on_text)
        self.Bind(wx.EVT_KILL_FOCUS, self._kill_focus)

    def _on_text(self, e):
        try:
            val = int("".join(self.Value.split(".")))
            self.ChangeValue(val)
            self.SetInsertionPointEnd()
        except ValueError:
            pass

    def _kill_focus(self, e):
        if self.Value == '':
            self.ChangeValue(0)

    def ChangeValue(self, val):
        val = otf.bill_int_to_str(val)
        super().ChangeValue(val)
