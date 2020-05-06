# -*- coding: utf-8 -*-
from core.log_in_dialog import LogInDialog
from core.main_view import Mainview
from core.nurse_view import NurseView
import wx


def mainloop():
    app = wx.App()
    with LogInDialog(None) as dlg:
        if dlg.ShowModal() == wx.ID_OK:
            dlg.save_staff_workday()
            job = dlg.get_staff_job()
            dlg.sess.close()
        else:
            quit()
    if job == 'Doctor':
        Mainview(None).Show()
    elif job == 'Nurse':
        NurseView(None).Show()
    app.MainLoop()
