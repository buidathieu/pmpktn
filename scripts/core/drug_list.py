import wx
import logging

class DrugList(wx.ListCtrl):

    def __init__(self, parent):
        super().__init__(parent, style=wx.LC_REPORT | wx.LC_SINGLE_SEL)
        self.total_drug_price = 0
        self.dwh_list = []
        self.AppendColumn('STT', width=d_stt_w)
        self.AppendColumn('Thuốc', width=d_name_w)
        self.AppendColumn('Số cữ', width=d_socu_w)
        self.AppendColumn('Liều 1 cữ', width=d_l1cu_w)
        self.AppendColumn('Tổng cộng', width=d_tc_w)
        self.AppendColumn('Cách dùng', width=d_tc_w * 4)
        self.Bind(wx.EVT_LIST_ITEM_SELECTED, self.onDrugSelect)
        self.Bind(wx.EVT_LIST_ITEM_DESELECTED, self.onDrugDeselect)

    def Update(self, linedruglist=None):
        if not linedruglist:
            linedruglist = self.Parent.Parent.visit.linedrugs
        self.dwh_list = [i.drug for i in linedruglist]
        self.DeleteAllItems()
        for i, ld in enumerate(linedruglist, start=1):
            self.Append(
                [i,
                 ld.drug.name,
                 f"{ld.times}",
                 f"{ld.dosage_per} {ld.drug.usage_unit}",
                 f"{ld.quantity} {ld.drug.sale_unit}",
                 ld.usage])
        self.calc_total_drug_price()

    def Clear(self):
        self.DeleteAllItems()
        self.dwh_list = []
        self.total_drug_price = 0

    def onDrugSelect(self, e):
        i = e.Index
        inf = self.Parent
        inf.drugpicker.drugWH = self.dwh_list[i]
        inf.drugpicker.ChangeValue(self.dwh_list[i].name)
        inf.times.ChangeValue(self.GetItemText(i, 2))
        inf.dosage_per.ChangeValue(self.GetItemText(i, 3).partition(' ')[0])
        inf.quantity.ChangeValue(self.GetItemText(i, 4).partition(' ')[0])
        inf.usage.ChangeValue(self.GetItemText(i, 5))

    def onDrugDeselect(self, e):
        self.Parent.drugpicker.Clear()

    def Add_or_Update(self, d, times, dosage_per, quantity, usage):
        assert self.ItemCount == len(self.dwh_list)
        inf = self.Parent
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
        inf.drugpicker.Clear()
        inf.drugpicker.SetFocus()
        self.calc_total_drug_price()

    def Remove(self):
        assert self.ItemCount == len(self.dwh_list)
        idx = self.GetFirstSelected()
        logging.debug(f"Delete drug {self.dwh_list[idx].name} ")
        if idx >= 0:
            self.dwh_list.pop(idx)
            self.DeleteItem(idx)
            for row in range(1, self.ItemCount):
                self.SetItem(row - 1, 0, str(row))
        else:
            logging.debug('drug not selected when delete')
        self.calc_total_drug_price()

    def calc_total_drug_price(self):
        assert self.ItemCount == len(self.dwh_list)
        self.total_drug_price = 0
        if self.ItemCount > 0:
            for i in range(self.ItemCount):
                qty = int(self.GetItemText(i, 4).partition(' ')[0])
                p = self.dwh_list[i].sale_price
                self.total_drug_price += (qty * p)

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