import wx
from .prescription_page import PrescriptionPage
from .therapy_page import TherapyPage


class OrderBook(wx.Notebook):

    def __init__(self, parent):
        super().__init__(parent)
        self.AddPage(page=PrescriptionPage(self),
                     text='Toa thuốc', select=True)
        self.AddPage(page=TherapyPage(self),
                     text="Thủ thuật")
