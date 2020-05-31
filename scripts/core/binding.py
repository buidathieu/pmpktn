from .core_func import onSaveVisit

import wx


def button_bindings(mv):
    mv.save_visit_btn.Bind(wx.EVT_BUTTON, lambda e: onSaveVisit(mv))