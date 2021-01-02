from initialize import *
import wx


my_accel = wx.AcceleratorTable(
    [wx.AcceleratorEntry(wx.ACCEL_NORMAL, wx.WXK_F1, id_new_patient),
     wx.AcceleratorEntry(wx.ACCEL_NORMAL, wx.WXK_F2, id_edit_patient),
     wx.AcceleratorEntry(wx.ACCEL_NORMAL, wx.WXK_F3, id_save_visit),
     wx.AcceleratorEntry(wx.ACCEL_NORMAL, wx.WXK_F5, wx.ID_REFRESH),
     wx.AcceleratorEntry(wx.ACCEL_ALT, wx.WXK_F4, wx.ID_EXIT)])
