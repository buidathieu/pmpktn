from initialize import *

import wx


class TherapyList(wx.ListCtrl):

    def __init__(self, parent):
        super().__init__(
            parent,
            style=wx.LC_REPORT | wx.LC_SINGLE_SEL)
        self.therapy_list = []
        self.AppendColumn('STT', width=d_stt_w)
        self.AppendColumn('Thủ thuật', width=d_name_w * 2)

    def Populate(self, linetherapies=None):
        self.therapy_list = [i.therapy for i in linetherapies]
        self.DeleteAllItems()
        for i, lt in enumerate(linetherapies, start=1):
            self.Append([i, lt.therapy.name])

    def Clear(self):
        self.DeleteAllItems()
        self.therapy_list = []

    def add(self, therapy):
        self.Append([
            self.ItemCount + 1,
            therapy.name])
        self.therapy_list.append(therapy)

    def remove_selected(self):
        idx = self.GetFirstSelected()
        if idx >= 0:
            self.therapy_list.pop(idx)
            self.DeleteItem(idx)
            for row in range(1, self.ItemCount + 1):
                self.SetItem(row - 1, 0, str(row))

    def get_total_price(self):
        assert self.ItemCount == len(self.therapy_list)
        return sum([i.sale_price for i in self.therapy_list])

    def build_linetherapies(self):
        return [t.id for t in self.therapy_list]

    # def build_linedrugs_for_pdf(self):
    #     linedrugs = []
    #     for i in range(self.ItemCount):
    #         ld = []
    #         ld.append(self.GetItemText(i, 1))
    #         ld.append(self.GetItemText(i, 5))
    #         ld.append(self.GetItemText(i, 4))
    #         linedrugs.append(ld)
    #     return linedrugs
