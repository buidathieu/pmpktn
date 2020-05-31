from initialize import *
from .core_func import onNewVisit, onSaveVisit
import other_func as otf

from sample_prescription import SamplePrescriptionDialog

import wx


def button_bindings(mv):
    # mv.new_visit_btn.Bind(wx.EVT_BUTTON, lambda e: onNewVisit(mv))
    mv.save_visit_btn.Bind(wx.EVT_BUTTON, lambda e: onSaveVisit(mv))