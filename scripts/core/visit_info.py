from initialize import *
from core.custom_ctrl import *
from core.__init__ import *
import other_func.other_func as otf
import db_sql.db_func as dbf
from sample_prescription.sample_prescription import SamplePrescriptionDialog
from fractions import Fraction as fr
import math
import wx
import logging


class Visit_Info_Panel(wx.Panel):

    def __init__(self, parent):
        super().__init__(parent)
        self._createWidgets()
        self._setSizer()

    def _createWidgets(self):
        self.group_label = wx.StaticText(self, label='Thông tin lượt khám')
        self.dt_label = wx.StaticText(self)
        self.note = self._createNote()
        self.diag = wx.TextCtrl(self)
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
        self.total_cost = self._createTotalCost()
        self.d_list = DrugList(self)
        self.followup = self._createFollowup()
        self.save_drug_btn = self._createSaveDrugbtn()
        self.erase_drug_btn = self._createEraseDrugbtn()
        self.new_visit_btn = self._createNewVisitbtn()
        self.reuse_btn = self._createReusebtn()
        self.sample_prescription_btn = self._createSamplePrescriptionbtn()
        self.save_visit_btn = self._createSaveVisitbtn()

    def _createNote(self):

        def on_tab(e):
            if e.KeyCode == wx.WXK_TAB:
                self.diag.SetFocus()
            else:
                e.Skip()

        w = wx.TextCtrl(self, size=note_size,
                        style=wx.TE_MULTILINE)
        w.Bind(wx.EVT_KEY_DOWN, on_tab)
        return w

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

    def _createTotalCost(self):

        def on_bill(e):
            val = int("".join(w.Value.split(".")))
            w.ChangeValue(otf.bill_int_to_str(val))
            w.SetInsertionPointEnd()

        def _kill_focus(e):
            if w.Value == '':
                w.ChangeValue('0')

        w = wx.TextCtrl(self,
                        value=otf.bill_int_to_str(setting['cong_kham_benh']))
        w.Bind(wx.EVT_CHAR, otf.only_nums)
        w.Bind(wx.EVT_TEXT, on_bill)
        w.Bind(wx.EVT_KILL_FOCUS, _kill_focus)
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
        btn.Bind(wx.EVT_BUTTON, self.onReuse)
        return btn

    def _createSamplePrescriptionbtn(self):
        btn = wx.Button(self, label="Toa mẫu")
        btn.Bind(wx.EVT_BUTTON, self.onSamplePrescriptionbtn)
        return btn

    def _createNewVisitbtn(self):
        btn = wx.Button(self, label='Lượt khám mới (F2)')
        btn.SetBitmap(wx.Bitmap(new_visit_bm))
        btn.Bind(wx.EVT_BUTTON, self.onNewVisit)
        return btn

    def _createSaveVisitbtn(self):
        btn = wx.Button(self, label='Lưu lượt khám (F3)')
        btn.SetBitmap(wx.Bitmap(save_visit_bm))
        btn.Bind(wx.EVT_BUTTON, self.onSaveVisit)
        return btn

    def _setSizer(self):
        label_1_row = wx.BoxSizer(wx.HORIZONTAL)
        datetime_row = wx.BoxSizer(wx.HORIZONTAL)
        diag_row = wx.BoxSizer(wx.HORIZONTAL)
        label_2_row = wx.BoxSizer(wx.HORIZONTAL)
        weight_days_row = wx.BoxSizer(wx.HORIZONTAL)
        drug_input_row = wx.BoxSizer(wx.HORIZONTAL)
        usage_row = wx.BoxSizer(wx.HORIZONTAL)
        followup_row = wx.BoxSizer(wx.HORIZONTAL)
        price_row = wx.BoxSizer(wx.HORIZONTAL)
        btn_row = wx.BoxSizer(wx.HORIZONTAL)
        sizer = wx.BoxSizer(wx.VERTICAL)

        label_1_row.Add(self.group_label)
        label_1_row.Add(wx.StaticLine(self), 1, wx.ALIGN_CENTER)
        datetime_row.Add(wx.StaticText(
            self,
            label='Bệnh sử, triệu chứng, ghi chú,... (theo từng lượt khám):'))
        datetime_row.Add(self.dt_label, 1, wx.RIGHT, 10)
        diag_row.Add(wx.StaticText(self, label='Chẩn đoán:'),
                     0, wx.ALIGN_CENTER | wx.TOP, 3)
        diag_row.Add(self.diag, 1)
        label_2_row.Add(wx.StaticText(self, label='Toa thuốc'), 0)
        label_2_row.Add(wx.StaticLine(self), 1, wx.ALIGN_CENTER)
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
        price_row.Add(self.reuse_btn, 0, wx.RIGHT, 5)
        price_row.Add(self.sample_prescription_btn, 0)
        price_row.AddStretchSpacer()
        price_row.Add(wx.StaticText(self, label='Tổng tiền:'), 0, wx.CENTRE)
        price_row.Add(self.total_cost, 0, wx.CENTRE)

        btn_row.Add(self.new_visit_btn)
        btn_row.Add(self.save_visit_btn)

        sizer.Add(label_1_row, 0, wx.EXPAND)
        sizer.Add(datetime_row, 0, wx.EXPAND)
        sizer.Add(self.note, 0, wx.EXPAND)
        sizer.Add(diag_row, 0, wx.EXPAND | wx.TOP, 3)
        sizer.Add(label_2_row, 0, wx.EXPAND)
        sizer.Add(weight_days_row, 0, wx.EXPAND)
        sizer.Add(drug_input_row, 0, wx.EXPAND)
        sizer.Add(usage_row, 0, wx.EXPAND)
        sizer.Add(self.d_list, 1, wx.EXPAND | wx.TOP, 3)
        sizer.Add(followup_row, 0, wx.EXPAND | wx.TOP, 3)
        sizer.Add(price_row, 0, wx.EXPAND | wx.TOP, 3)
        sizer.AddSpacer(20)
        sizer.Add(btn_row, 0, wx.EXPAND | wx.BOTTOM, 10)
        self.SetSizer(sizer)

    # functions
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

        v = self.Parent.visit
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

    def Clear(self):
        self.group_label.Label = 'Thông tin lượt khám'
        self.dt_label.Label = ""
        self.note.ChangeValue("")
        self.diag.ChangeValue("")
        self.weight.ChangeValue('0')
        self.days.ChangeValue('2')
        self.total_cost.ChangeValue("0")
        self.followup.Selection = 0
        self.d_list.Clear()
        self.drugpicker.Clear()

    def onNewVisit(self, e):
        self.NewVisit()

    def onSaveVisit(self, e):
        self.SaveVisit()

    def NewVisit(self):
        self.Parent.visit = None

    def SaveVisit(self):
        mv = self.Parent
        bs_inf = mv.basic_info
        v_inf = mv.visit_info
        v_list = mv.visit_list
        p = mv.patient
        v = mv.visit

        assert mv.patient is not None
        assert bs_inf.name.Value != ""
        assert self.diag.Value != ""

        kwargs = {
            'pid': p.id,
            'name': bs_inf.name.Value,
            'birthdate': otf.wxdate2pydate(
                bs_inf.birthdate.Value),
            'address': bs_inf.address.Value,
            'past_history': bs_inf.past_history.Value,
            'note': v_inf.note.Value,
            'diag': v_inf.diag.Value,
            'weight': float(v_inf.weight.Value),
            'days': int(v_inf.days.Value),
            'followup': v_inf.followup.Value,
            'bill': otf.bill_str_to_int(
                v_inf.total_cost.Value),
            'linedrugs': v_inf.d_list.build_linedrugs()
        }
        if v:
            ans = wx.MessageBox("Cập nhật lượt khám?", "Lưu", style=wx.YES_NO)
            if ans == wx.YES:
                logging.debug(f"update selected visit: {v.exam_date}")
                dbf.save_old_visit(**kwargs, vid=v.id, sess=self.Parent.sess)
                wx.MessageBox("Đã cập nhật")
        else:
            ans = wx.MessageBox("Lưu lượt khám mới?", "Lưu", style=wx.YES_NO)
            if ans == wx.YES:
                logging.debug("save new visit")
                dbf.save_new_visit(**kwargs, sess=self.Parent.sess)
                wx.MessageBox("Đã lưu")
        mv.Refresh()

    def onSamplePrescriptionbtn(self, e):
        with SamplePrescriptionDialog(self) as dlg:
            if dlg.ShowModal() == wx.ID_APPLY:
                ps, _ = dlg.get_selected_sample_prescription()
                self.d_list.Clear()
                for i in ps.samplelinedrugs:
                    self.drugpicker.drugWH = i.drug
                    self.times.ChangeValue(str(i.times))
                    self.dosage_per.ChangeValue(i.dosage_per)
                    self.usage_unit.Label = i.drug.usage_unit
                    self.sale_unit.Label = i.drug.sale_unit
                    self._calc_quantity(None)
                    kwargs = {
                        "d": self.drugpicker.drugWH,
                        "times": self.times.Value,
                        "dosage_per": self.dosage_per.Value,
                        "quantity": self.quantity.Value,
                        "usage": self.usage.Value
                    }
                    self.d_list.Add_or_Update(**kwargs)
                self.total_cost.ChangeValue(otf.bill_int_to_str(
                    setting['cong_kham_benh'] + self.d_list.total_drug_price))
