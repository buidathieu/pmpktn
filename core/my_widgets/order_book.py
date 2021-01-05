import wx
from .prescription_page import PrescriptionPage


class OrderBook(wx.Notebook):

    def __init__(self, parent):
        super().__init__(parent)
        self.mv = parent
        self.AddPage(page=PrescriptionPage(self),
                     text='Toa thuốc', select=True)

    def refresh(self):
        for i in range(self.PageCount):
            self.GetPage(i).refresh()
