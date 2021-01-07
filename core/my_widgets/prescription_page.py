from initialize import *
from .drug_picker import DrugPicker
from .drug_list import DrugList
import other_func as otf
from .get_weight_btn import GetWeightBtn
from .calc_quantity_widgets import Days, Times, DosagePer, Quantity

import wx

class PrescriptionPage(wx.Panel):

    def __init__(self, parent):
        super().__init__(parent)
        self.mv = parent.mv
        self._createWidgets()
        self._setSizer()
        self._bind()

    def _createWidgets(self):
        self.weight = self._createWeight()
        self.getweightbtn = GetWeightBtn(self)
        self.days = Days(self)
        self.drug_picker = DrugPicker(self)
        self.times = Times(self)
        self.dosage_per = DosagePer(self)
        self.quantity = Quantity(self)
        self.usage_unit = wx.StaticText(
            self,
            label='{Đơn vị} ')
        self.sale_unit = wx.StaticText(
            self,
            label='{Đơn vị} ')
        self.usage = wx.TextCtrl(self)
        self.d_list = DrugList(self)
        self.save_drug_btn = wx.BitmapButton(
            self,
            bitmap=wx.Bitmap(plus_bm))
        self.del_drug_btn = wx.BitmapButton(
            self,
            bitmap=wx.Bitmap(minus_bm))
        self.reuse_btn = wx.Button(
            self,
            label='Lượt khám mới với toa cũ')

    def _createWeight(self):
        w = wx.TextCtrl(self, size=dose_size, value='0')
        w.Bind(wx.EVT_CHAR,
               lambda e: otf.only_nums(e, decimal=True))
        w.SetHint('Kg')
        return w

    def _setSizer(self):
        weight_days_row = wx.BoxSizer(wx.HORIZONTAL)
        drug_input_row = wx.BoxSizer(wx.HORIZONTAL)
        usage_row = wx.BoxSizer(wx.HORIZONTAL)
        btn_row = wx.BoxSizer(wx.HORIZONTAL)
        sizer = wx.BoxSizer(wx.VERTICAL)

        weight_days_row.Add(wx.StaticText(self, label='Cân nặng: '),
                            0, wx.ALIGN_CENTER)
        weight_days_row.Add(self.weight, 0, wx.ALIGN_CENTER | wx.RIGHT, 5)
        weight_days_row.Add(self.getweightbtn, 0, wx.RIGHT, 5)
        weight_days_row.Add(wx.StaticText(self, label='Số ngày: '),
                            0, wx.ALIGN_CENTER)
        weight_days_row.Add(self.days, 0, wx.ALIGN_CENTER)
        drug_input_row.Add(wx.StaticText(self, label='Thuốc: '),
                           0, wx.ALIGN_CENTER | wx.RIGHT, 5)
        drug_input_row.Add(self.drug_picker, 1, wx.ALIGN_CENTER | wx.RIGHT, 5)
        drug_input_row.Add(self.times, 0, wx.ALIGN_CENTER | wx.RIGHT, 5)
        drug_input_row.Add(wx.StaticText(self, label='lần, lần'),
                           0, wx.ALIGN_CENTER | wx.RIGHT, 5)
        drug_input_row.Add(
            self.dosage_per, 0, wx.ALIGN_CENTER | wx.RIGHT, 5)
        drug_input_row.Add(self.usage_unit, 0, wx.ALIGN_CENTER | wx.RIGHT, 5)
        drug_input_row.Add(wx.StaticText(
            self, label=u"\u21D2   Tổng cộng: "), 0, wx.ALIGN_CENTER)
        drug_input_row.Add(
            self.quantity, 0, wx.ALIGN_CENTER | wx.RIGHT, 5)
        drug_input_row.Add(self.sale_unit, 0, wx.ALIGN_CENTER | wx.RIGHT, 5)
        drug_input_row.Add(self.save_drug_btn, 0,
                           wx.ALIGN_CENTER | wx.RIGHT, 5)
        drug_input_row.Add(self.del_drug_btn, 0,
                           wx.ALIGN_CENTER | wx.RIGHT, 5)

        usage_row.Add(wx.StaticText(
            self, label='Cách dùng: '), 0, wx.CENTRE | wx.RIGHT, 5)
        usage_row.Add(self.usage, 1)
        btn_row.Add(self.reuse_btn, 0, wx.RIGHT, 5)

        sizer.Add(weight_days_row, 0, wx.EXPAND)
        sizer.Add(drug_input_row, 0, wx.EXPAND)
        sizer.Add(usage_row, 0, wx.EXPAND)
        sizer.Add(self.d_list, 1, wx.EXPAND | wx.TOP, 3)
        sizer.Add(btn_row, 0, wx.EXPAND | wx.TOP, 3)

        self.SetSizer(sizer)

    def _bind(self):
        self.save_drug_btn.Bind(wx.EVT_BUTTON, lambda e: self.onSaveDrug())
        self.del_drug_btn.Bind(wx.EVT_BUTTON, lambda e: self.onDelDrug())
        self.reuse_btn.Bind(wx.EVT_BUTTON, lambda e: self.onReuse())

    def refresh(self):
        self.drug_picker.Clear()
        self.drug_picker.refreshPopup()

    def onSaveDrug(self):
        kwargs = {
            "d": self.drug_picker.drugWH,
            "times": self.times.Value,
            "dosage_per": self.dosage_per.Value,
            "quantity": self.quantity.Value,
            "usage": self.usage.Value
        }
        assert kwargs["d"] is not None
        assert int(kwargs["times"])
        assert kwargs['dosage_per'] != ""
        assert int(kwargs['quantity'])
        self.d_list.add_or_update(**kwargs)
        self.mv.calc_price()

    def onDelDrug(self):
        selected_id = self.d_list.GetFirstSelected()
        self.d_list.remove(selected_id)
        self.mv.calc_price()
        self.drug_picker.Clear()

    def onReuse(self):
        v_idx = self.mv.visit_list.GetFirstSelected()
        if v_idx != -1:
            # keep old values
            linedrugs = self.mv.visit.linedrugs.copy()
            w = self.weight.Value
            d = self.days.Value
            # unselect
            self.mv.visit_list.Select(v_idx, 0)
            # populate field with old values
            self.d_list.Populate(linedrugs=linedrugs)
            self.weight.ChangeValue(w)
            self.days.ChangeValue(d)
            self.mv.calc_price()
