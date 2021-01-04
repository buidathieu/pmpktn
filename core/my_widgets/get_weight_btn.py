from initialize import weight_bm

import wx


class GetWeightBtn(wx.BitmapButton):

    def __init__(self, parent):
        super().__init__(
            parent=parent,
            bitmap=wx.Bitmap(weight_bm)
        )
        self.mv = parent.Parent.Parent
        self.Bind(wx.EVT_BUTTON, self.getLatestWeight)

    def getLatestWeight(self, e):
        visits = self.mv.patient.visits.all()
        weight = self.mv.order_book.GetPage(0).weight
        if len(visits) > 0:
            weight.ChangeValue(str(visits[-1].weight))
