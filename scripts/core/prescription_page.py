from initialize import *
from .custom_popup import DrugPicker
from .drug_list import DrugList
import other_func as otf
from .core_func import getWeight, calc_quantity,\
    onSaveDrug, onEraseDrug, onReuse, onSamplePrescriptionbtn

import logging

import wx


class PrescriptionPage(wx.Panel):

    def __init__(self, parent):
        super().__init__(parent)
        self._createWidgets()
        self._setSizer()
        
    def _createWidgets(self):
        self.weight = self._createWeight()
        self.getweightbtn = self._createGetWeightBtn()
        self.days = self._createDays()
        self.drugpicker = DrugPicker(self)
        self.times = self._createTimes()
        self.dosage_per = self._createDosagePer()
        self.quantity = self._createQuantity()
        self.usage_unit = wx.StaticText(self, label='{Đơn vị}')
        self.sale_unit = wx.StaticText(self, label='{Đơn vị}')
        self.usage = wx.TextCtrl(self)
        self.d_list = DrugList(self)
        self.followup = self._createFollowup()
        self.save_drug_btn = self._createSaveDrugbtn()
        self.erase_drug_btn = self._createEraseDrugbtn()
        self.reuse_btn = self._createReusebtn()
        self.sample_prescription_btn = self._createSamplePrescriptionbtn()
        
    def _createWeight(self):
        w = wx.TextCtrl(self, size=dose_size, value='0')
        w.Bind(wx.EVT_CHAR,
               lambda e: otf.only_nums(e, decimal=True))
        w.SetHint('Kg')
        return w

    def _createGetWeightBtn(self):
        w = wx.BitmapButton(self, bitmap=wx.Bitmap(weight_bm))
        w.Bind(wx.EVT_BUTTON, self._getWeight)
        return w

    def _createDays(self):
        w = wx.TextCtrl(self, size=days_size, value='2')
        w.Bind(wx.EVT_CHAR, otf.only_nums)
        w.Bind(wx.EVT_TEXT, self._calc_quantity)
        return w

    def _createTimes(self):
        w = wx.TextCtrl(self, size=dose_size)
        w.SetHint('lần')
        w.Bind(wx.EVT_CHAR, otf.only_nums)
        w.Bind(wx.EVT_TEXT, self._calc_quantity)
        return w

    def _createDosagePer(self):
        w = wx.TextCtrl(self, size=dose_size)
        w.SetHint('liều')
        w.Bind(wx.EVT_CHAR,
               lambda e: otf.only_nums(e, decimal=True, slash=True))
        w.Bind(wx.EVT_TEXT, self._calc_quantity)
        return w

    def _createQuantity(self):

        def on_txt_qty(e):
            x = e.KeyCode
            if x in (wx.WXK_RETURN, wx.WXK_NUMPAD_ENTER):
                self.onSaveDrug(None)
            elif x == wx.WXK_TAB:
                return
            else:
                otf.only_nums(e)

        w = wx.TextCtrl(self, size=dose_size, style=wx.TE_PROCESS_ENTER)
        w.SetHint('Enter')
        w.Bind(wx.EVT_CHAR, on_txt_qty)
        return w

    def _createFollowup(self):
        choices = setting["followup_list"]
        choices.extend(list(setting["followup_dict"]))
        w = wx.ComboBox(self, style=wx.CB_DROPDOWN, choices=choices)
        return w
        
    def _createSaveDrugbtn(self):
        btn = wx.BitmapButton(self, bitmap=wx.Bitmap(plus_bm))
        btn.Bind(wx.EVT_BUTTON, self._onSaveDrug)
        return btn

    def _createEraseDrugbtn(self):
        btn = wx.BitmapButton(self, bitmap=wx.Bitmap(minus_bm))
        btn.Bind(wx.EVT_BUTTON, self._onEraseDrug)
        return btn

    def _createReusebtn(self):
        btn = wx.Button(self, label='Lượt khám mới với toa cũ')
        btn.Bind(wx.EVT_BUTTON, self._onReuse)
        return btn

    def _createSamplePrescriptionbtn(self):
        btn = wx.Button(self, label="Toa mẫu")
        btn.Bind(wx.EVT_BUTTON, self._onSamplePrescriptionbtn)
        return btn
        
    def _setSizer(self):       
        weight_days_row = wx.BoxSizer(wx.HORIZONTAL)
        drug_input_row = wx.BoxSizer(wx.HORIZONTAL)
        usage_row = wx.BoxSizer(wx.HORIZONTAL)
        followup_row = wx.BoxSizer(wx.HORIZONTAL)
        btn_row = wx.BoxSizer(wx.HORIZONTAL)
        sizer = wx.BoxSizer(wx.VERTICAL)

        weight_days_row.Add(wx.StaticText(self, label='Cân nặng:'),
                            0, wx.ALIGN_CENTER)
        weight_days_row.Add(self.weight, 0, wx.ALIGN_CENTER | wx.RIGHT, 5)
        weight_days_row.Add(self.getweightbtn, 0, wx.RIGHT, 5)
        weight_days_row.Add(wx.StaticText(self, label='Số ngày:'),
                            0, wx.ALIGN_CENTER)
        weight_days_row.Add(self.days, 0, wx.ALIGN_CENTER)
        drug_input_row.Add(wx.StaticText(self, label='Thuốc:'),
                           0, wx.ALIGN_CENTER | wx.RIGHT, 5)
        drug_input_row.Add(self.drugpicker, 1, wx.ALIGN_CENTER | wx.RIGHT, 5)
        drug_input_row.Add(self.times, 0, wx.ALIGN_CENTER | wx.RIGHT, 5)
        drug_input_row.Add(wx.StaticText(self, label='lần, lần'),
                           0, wx.ALIGN_CENTER | wx.RIGHT, 5)
        drug_input_row.Add(
            self.dosage_per, 0, wx.ALIGN_CENTER | wx.RIGHT, 5)
        drug_input_row.Add(self.usage_unit, 0, wx.ALIGN_CENTER | wx.RIGHT, 5)
        drug_input_row.Add(wx.StaticText(
            self, label=u"\u21D2   Tổng cộng:"), 0, wx.ALIGN_CENTER)
        drug_input_row.Add(
            self.quantity, 0, wx.ALIGN_CENTER | wx.RIGHT, 5)
        drug_input_row.Add(self.sale_unit, 0, wx.ALIGN_CENTER | wx.RIGHT, 5)
        drug_input_row.Add(self.save_drug_btn, 0,
                           wx.ALIGN_CENTER | wx.RIGHT, 5)
        drug_input_row.Add(self.erase_drug_btn, 0,
                           wx.ALIGN_CENTER | wx.RIGHT, 5)

        usage_row.Add(wx.StaticText(
            self, label='Cách dùng:'), 0, wx.CENTRE | wx.RIGHT, 5)
        usage_row.Add(self.usage, 1)
        followup_row.Add(wx.StaticText(self, label='Dặn dò:'),
                         0, wx.CENTRE | wx.RIGHT, 5)
        followup_row.Add(self.followup, 1)
        btn_row.Add(self.reuse_btn, 0, wx.RIGHT, 5)
        btn_row.Add(self.sample_prescription_btn, 0)

        sizer.Add(weight_days_row, 0, wx.EXPAND)
        sizer.Add(drug_input_row, 0, wx.EXPAND)
        sizer.Add(usage_row, 0, wx.EXPAND)
        sizer.Add(self.d_list, 1, wx.EXPAND | wx.TOP, 3)
        sizer.Add(followup_row, 0, wx.EXPAND | wx.TOP, 3)
        sizer.Add(btn_row, 0, wx.EXPAND | wx.TOP, 3)
        self.SetSizer(sizer)
        
    def _getWeight(self, e):
        self.weight.ChangeValue(getWeight(mv=self.Parent.Parent))

    def _calc_quantity(self, e):
        calc_quantity(self)
            
    def _onSaveDrug(self, e):
        onSaveDrug(self)

    def _onEraseDrug(self, e):
        onEraseDrug(self)
        
    def _onReuse(self, e):
        onReuse(self)
    
    def _onSamplePrescriptionbtn(self, e):
        onSamplePrescriptionbtn(self)
