from initialize import *
from .core_func import onNewVisit
import other_func as otf

from sample_prescription import SamplePrescriptionDialog

import wx
import logging


def button_bindings(mv):
    mv.new_visit_btn.Bind(onNewVisit(mv))
    mv.save_visit_btn.Bind()