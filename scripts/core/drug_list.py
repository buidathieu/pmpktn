from initialize import *

import wx
import logging


class DrugList(wx.ListCtrl):

    def __init__(self, parent):
        super().__init__(parent, style=wx.LC_REPORT | wx.LC_SINGLE_SEL)
        self.dwh_list = []
        self.AppendColumn('STT', width=d_stt_w)
        self.AppendColumn('Thuốc', width=d_name_w)
        self.AppendColumn('Số cữ', width=d_socu_w)
        self.AppendColumn('Liều 1 cữ', width=d_l1cu_w)
        self.AppendColumn('Tổng cộng', width=d_tc_w)
        self.AppendColumn('Cách dùng', width=d_tc_w * 4)
        self.Bind(wx.EVT_LIST_ITEM_SELECTED, self.onDrugSelect)
        self.Bind(wx.EVT_LIST_ITEM_DESELECTED, self.onDrugDeselect)

    def Populate(self, linedrugs=None):
        self.dwh_list = [i.drug for i in linedrugs]
        self.DeleteAllItems()
        for i, ld in enumerate(linedrugs, start=1):
            self.Append(
                [i,
                 ld.drug.name,
                 f"{ld.times}",
                 f"{ld.dosage_per} {ld.drug.usage_unit}",
                 f"{ld.quantity} {ld.drug.sale_unit}",
                 ld.usage])

    def Clear(self):
        self.DeleteAllItems()
        self.dwh_list = []

    def onDrugSelect(self, e):
        i = e.Index
        pg = self.Parent
        pg.drug_picker.drugWH = self.dwh_list[i]
        pg.drug_picker.ChangeValue(self.dwh_list[i].name)
        pg.times.ChangeValue(self.GetItemText(i, 2))
        pg.dosage_per.ChangeValue(self.GetItemText(i, 3).partition(' ')[0])
        pg.quantity.ChangeValue(self.GetItemText(i, 4).partition(' ')[0])
        pg.usage.ChangeValue(self.GetItemText(i, 5))

    def onDrugDeselect(self, e):
        self.Parent.drug_picker.Clear()

    def add_or_update(self, d, times, dosage_per, quantity, usage):
        assert self.ItemCount == len(self.dwh_list)
        pg = self.Parent
        try:
            # find if already added drug
            row = [i.id for i in self.dwh_list].index(d.id)
            loggin.debug('drug found -> UPDATE ')
            self.SetItem(row, 2, times)
            self.SetItem(row, 3, f"{dosage_per} {d.usage_unit}")
            self.SetItem(row, 4, f"{quantity} {d.sale_unit}")
            self.SetItem(row, 5, usage)
        except ValueError:
            logging.debug('drug not found -> ADD')
            self.Append([
                self.ItemCount + 1,
                d.name,
                times,
                f"{dosage_per} {d.usage_unit}",
                f"{quantity} {d.sale_unit}",
                usage
            ])
            self.dwh_list.append(d)
        pg.drug_picker.Clear()
        pg.drug_picker.SetFocus()

    def remove_selected(self):
        assert self.ItemCount == len(self.dwh_list)
        idx = self.GetFirstSelected()
        logging.debug(f"Delete drug {self.dwh_list[idx].name} ")
        if idx >= 0:
            self.dwh_list.pop(idx)
            self.DeleteItem(idx)
            for row in range(1, self.ItemCount + 1):
                self.SetItem(row - 1, 0, str(row))
        else:
            logging.debug('drug not found when delete')

    def get_total_price(self):
        assert self.ItemCount == len(self.dwh_list)
        total = 0
        if self.ItemCount > 0:
            for i in range(self.ItemCount):
                qty = int(self.GetItemText(i, 4).partition(' ')[0])
                p = self.dwh_list[i].sale_price
                total += (qty * p)
        return total

    def build_linedrugs(self):
        linedrugs = []
        for i in range(self.ItemCount):
            ld = {}
            ld['drug_id'] = self.dwh_list[i].id
            ld['dosage_per'] = self.GetItemText(i, 3).partition(' ')[0]
            ld['times'] = int(self.GetItemText(i, 2))
            ld['quantity'] = int(self.GetItemText(i, 4).partition(' ')[0])
            ld['usage'] = self.GetItemText(i, 5)
            linedrugs.append(ld)
        return linedrugs

    def build_linedrugs_for_pdf(self):
        linedrugs = []
        for i in range(self.ItemCount):
            ld = []
            ld.append(self.GetItemText(i, 1))
            ld.append(self.GetItemText(i, 5))
            ld.append(self.GetItemText(i, 4))
            linedrugs.append(ld)
        return linedrugs
