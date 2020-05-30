from initialize import *
from .custom_popup import DrugPicker
from .drug_list import DrugList
import other_func as otf
import db_sql.db_func as dbf
from sample_prescription import SamplePrescriptionDialog
from fractions import Fraction as fr
import math
import wx
import logging


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
        w.Bind(wx.EVT_SET_FOCUS, lambda e: w.SelectAll())
        w.Bind(wx.EVT_CHAR,
               lambda e: otf.only_nums(e, decimal=True))
        w.SetHint('Kg')
        return w

    def _createGetWeightBtn(self):
        w = wx.BitmapButton(self, bitmap=wx.Bitmap(weight_bm))
        w.Bind(wx.EVT_BUTTON, self.getWeight)
        return w

    def _createDays(self):
        w = wx.TextCtrl(self, size=days_size, value='2')
        w.Bind(wx.EVT_SET_FOCUS, lambda e: w.SelectAll())
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
        w = wx.TextCtrl(self)
        return w
        
    def _createSaveDrugbtn(self):
        btn = wx.BitmapButton(self, bitmap=wx.Bitmap(plus_bm))
        btn.Bind(wx.EVT_BUTTON, self.onSaveDrug)
        return btn

    def _createEraseDrugbtn(self):
        btn = wx.BitmapButton(self, bitmap=wx.Bitmap(minus_bm))
        btn.Bind(wx.EVT_BUTTON, self.onEraseDrug)
        return btn

    def _createReusebtn(self):
        btn = wx.Button(self, label='Lượt khám mới với toa cũ')
        # btn.Bind(wx.EVT_BUTTON, self.onReuse)
        return btn

    def _createSamplePrescriptionbtn(self):
        btn = wx.Button(self, label="Toa mẫu")
        # btn.Bind(wx.EVT_BUTTON, self.onSamplePrescriptionbtn)
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
        
    def getWeight(self, e):
        logging.debug('get latest weight')
        weight = self.Parent.patient.visits[-1].weight
        self.weight.Value = str(weight)
        
    def _calc_quantity(self, e):
        logging.debug('recalculate quantity')
        day = self.days.Value
        dosage = self.dosage_per.Value
        time = self.times.Value
        drug = self.drugpicker.drugWH
        try:
            assert day != 0
            assert dosage != ''
            assert time != ''
            assert drug is not None
            # numberize
            day = int(day)
            time = int(time)
            if "/" in dosage:
                dosage = fr(dosage)
            elif "." in dosage:
                dosage = float(dosage)
            else:
                dosage = int(dosage)
            # cal qty
            if drug.sale_unit == 'chai':
                qty = '1'
            else:
                qty = math.ceil(dosage * time * day)

            self.quantity.ChangeValue(str(qty))
            self.usage.ChangeValue(
                "Ngày {} {} lần, lần {} {}".format(
                    drug.usage,
                    time,
                    dosage,
                    drug.usage_unit))
        except AssertionError:
            pass
            
    def onSaveDrug(self, e):
        kwargs = {
            "d": self.drugpicker.drugWH,
            "times": self.times.Value,
            "dosage_per": self.dosage_per.Value,
            "quantity": self.quantity.Value,
            "usage": self.usage.Value
        }
        assert kwargs["d"] is not None
        assert int(kwargs["times"])
        assert kwargs['dosage_per'] != ""
        assert int(kwargs['quantity'])

        logging.debug(f"Add or update drug, recalc total_drug_price:\n\t\
                      {kwargs['d'].name}\n{kwargs}")
        self.d_list.Add_or_Update(**kwargs)
        self.total_cost.ChangeValue(otf.bill_int_to_str(
            setting['cong_kham_benh'] + self.d_list.total_drug_price))

    def onEraseDrug(self, e):
        logging.debug("Del drug, recalc total_drug_price")
        self.d_list.Remove()
        self.total_cost.ChangeValue(otf.bill_int_to_str(
            setting['cong_kham_benh'] + self.d_list.total_drug_price))
        self.drugpicker.Clear()
        self.drugpicker.SetFocus()
        
    def onReuse(self, e):
        # keep old values
        logging.debug('on Reuse weight, days, linedruglist, total_cost')
        linedruglist = self.Parent.visit.linedrugs.copy()
        w = self.weight.Value
        d = self.days.Value
        p = self.total_cost.Value
        # unselect
        self.Parent.visit = None
        # populate field with old values
        self.d_list.Update(linedruglist=linedruglist)
        self.weight.ChangeValue(w)
        self.days.ChangeValue(d)
        self.total_cost.ChangeValue(p)
        
    def Update(self):

        def _dt_to_label(p_dt):
            return ' ' * 20 + 'Giờ khám: {}:{} ngày {} tháng {} năm {}'.\
                format(str(p_dt.hour).rjust(2, '0'),
                       str(p_dt.minute).rjust(2, '0'),
                       p_dt.day,
                       p_dt.month,
                       p_dt.year)

        v = self.Parent.Parent.Parent.visit
        logging.debug(f"update visit_info with selected visit:\n\t\
                      {v.exam_date} {v.bill}")
        self.group_label.Label =\
            f'Thông tin lượt khám (Mã lượt khám: {v.id})'
        self.dt_label.Label = _dt_to_label(v.exam_date)
        self.note.ChangeValue(v.note)
        self.diag.ChangeValue(v.diag)
        self.weight.ChangeValue(str(v.weight))
        self.days.ChangeValue(str(v.days))
        self.drugpicker.Clear()
        self.d_list.Update()
        self.total_cost.ChangeValue(otf.bill_int_to_str(v.bill))
        self.followup.ChangeValue(v.followup)