from .patient_book import PatientBook
from .visit_list import VisitList
import wx


def create_left_panel_widgets(mv):
    mv.book = PatientBook(mv)
    mv.visit_list = VisitList(mv)


def create_left_panel_sizer(mv):
    sizer = wx.BoxSizer(wx.VERTICAL)
    sizer.Add(mv.book, 10, wx.LEFT | wx.TOP, 10)
    sizer.Add(wx.StaticText(mv, label='Lượt khám cũ:'), 0, wx.LEFT, 20)
    sizer.Add(mv.visit_list, 4, wx.EXPAND | wx.LEFT | wx.BOTTOM, 20)
    return sizer
