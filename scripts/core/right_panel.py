from initialize import *
from .custom_ctrl import *
import other_func as otf
import db_sql.db_func as dbf
from sample_prescription.sample_prescription import SamplePrescriptionDialog

import wx
import wx.adv

from fractions import Fraction as fr
import math
    

class RightPanel(wx.Panel):

    def __init__(self, parent):
        super().__init__(parent)
        self.group_label_1 = wx.StaticText(self, label='Thông tin bệnh nhân')
        self.name = self._createName()
        self.gender = self._createGender()
        self.birthdate = self._createBirthdate()
        self.age = self._createAge()
        self.address = wx.TextCtrl(self)
        self.past_history = self._createPastHistory()
        self.group_label_2 = wx.StaticText(self, label='Thông tin lượt khám')
        self.dt_label = wx.StaticText(self)
        self.note = self._createNote()
        self.diag = wx.TextCtrl(self)
        self.weight = self._createWeight()
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
        self.new_p_btn = self._createNewbtn()
        self.new_visit_btn = self._createNewVisitbtn()
        self.reuse_btn = self._createReusebtn()
        self.sample_prescription_btn = self._createSamplePrescriptionbtn()
        self.save_visit_btn = self._createSaveVisitbtn()
        
        self._setSizer()
           
    def _createName(self):
        w = wx.TextCtrl(self, size=name_size)
        return w

    def _createGender(self):
        w = wx.Choice(self, choices=[gender_dict[0], gender_dict[1]])
        w.Selection = 0
        return w

    def _createBirthdate(self):

        def onBirthdateChange(e):
            self.age.ChangeValue(otf.bd_to_age(w.Value).ljust(16))
            e.Skip()

        w = wx.adv.DatePickerCtrl(self, dt=wx.DateTime(31, 11, 2010))
        w.Bind(wx.adv.EVT_DATE_CHANGED, onBirthdateChange)
        return w

    def _createAge(self):

        def onAgeChange(e):
            self.birthdate.SetValue(otf.age_to_bd(w.Value))
            e.Skip()

        w = wx.TextCtrl(self)
        w.Bind(wx.EVT_TEXT, onAgeChange)
        return w

    def _createPastHistory(self):

        def onTab(e):
            if e.KeyCode == wx.WXK_TAB:
                self.Parent.visit_info.note.SetFocus()
            else:
                e.Skip()

        w = wx.TextCtrl(self, style=wx.TE_MULTILINE, size=note_size)
        w.Bind(wx.EVT_CHAR, onTab)
        return w
        
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
        btn = wx.BitmapButton(self, bitmap=wx.Bitmap(save_drug_bm))
        btn.Bind(wx.EVT_BUTTON, self.onSaveDrug)
        return btn

    def _createEraseDrugbtn(self):
        btn = wx.BitmapButton(self, bitmap=wx.Bitmap(name=erase_drug_bm))
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

    def _createNewbtn(self):
        btn = wx.Button(self, label='Bệnh nhân mới (F1)')
        btn.SetBitmap(wx.Bitmap(new_p_bm))
        btn.Bind(wx.EVT_BUTTON, self.onNewPatientbtn)
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
        sizer = wx.BoxSizer(wx.VERTICAL)
        row_1 = wx.BoxSizer(wx.HORIZONTAL)
        row_2 = wx.BoxSizer(wx.HORIZONTAL)
        row_3 = wx.BoxSizer(wx.HORIZONTAL)
        row_4 = wx.BoxSizer(wx.HORIZONTAL)
        row_5 = wx.BoxSizer(wx.HORIZONTAL)
        row_6 = wx.BoxSizer(wx.HORIZONTAL)
        row_7 = wx.BoxSizer(wx.HORIZONTAL)
        row_8 = wx.BoxSizer(wx.HORIZONTAL)
        row_9 = wx.BoxSizer(wx.HORIZONTAL)
        row_10 = wx.BoxSizer(wx.HORIZONTAL)
        row_11 = wx.BoxSizer(wx.HORIZONTAL)
        row_12 = wx.BoxSizer(wx.HORIZONTAL)
        row_13 = wx.BoxSizer(wx.HORIZONTAL)

        row_1.Add(self.group_label_1, 0)
        row_1.Add(wx.StaticLine(self), 1, wx.ALIGN_CENTER)
        
        row_2.Add(wx.StaticText(
            self, label='Họ tên:'), 0, wx.ALIGN_CENTER)
        row_2.Add(self.name, 0, wx.ALIGN_CENTER | wx.RIGHT, 5)
        row_2.Add(self.gender, 0, wx.ALIGN_CENTER | wx.RIGHT, 5)
        row_2.Add(wx.StaticText(
            self, label='Ngày sinh:'), 0, wx.ALIGN_CENTER)
        row_2.Add(self.birthdate, 0, wx.ALIGN_CENTER | wx.RIGHT, 5)
        row_2.Add(wx.StaticText(
            self, label='Tuổi:'), 0, wx.ALIGN_CENTER)
        row_2.Add(self.age, 1, wx.ALIGN_CENTER)
        
        row_3.Add(wx.StaticText(
            self, label='Địa chỉ:'), 0, wx.ALIGN_CENTER)
        row_3.Add(self.address, 1, wx.EXPAND)
        
        sizer.Add(row_1, 0, wx.EXPAND)
        sizer.Add(row_2, 0, wx.EXPAND)
        sizer.Add(row_3, 0, wx.EXPAND | wx.TOP, 3)
        sizer.Add(wx.StaticText(
            self, label='Bệnh nền, dị ứng:'),
            0, wx.TOP, 3)
        sizer.Add(self.past_history, 0, wx.EXPAND)

        row_4.Add(self.group_label_2)
        row_4.Add(wx.StaticLine(self), 1, wx.ALIGN_CENTER)
        
        row_5.Add(wx.StaticText(
            self, label='Bệnh sử, triệu chứng, ghi chú,... (theo từng lượt khám):'))
        row_5.Add(self.dt_label, 1, wx.RIGHT, 10)
        
        row_6.Add(wx.StaticText(self, label='Chẩn đoán:'),
                     0, wx.ALIGN_CENTER | wx.TOP, 3)
        row_6.Add(self.diag, 1)
        
        row_7.Add(wx.StaticText(self, label='Toa thuốc'), 0)
        row_7.Add(wx.StaticLine(self), 1, wx.ALIGN_CENTER)
        
        row_8.Add(wx.StaticText(self, label='Cân nặng:'),
                            0, wx.ALIGN_CENTER)
        row_8.Add(self.weight, 0, wx.ALIGN_CENTER | wx.RIGHT, 5)
        row_8.Add(wx.StaticText(self, label='Số ngày:'),
                            0, wx.ALIGN_CENTER)
        row_8.Add(self.days, 0, wx.ALIGN_CENTER)
        
        row_9.Add(wx.StaticText(self, label='Thuốc:'),
                           0, wx.ALIGN_CENTER | wx.RIGHT, 5)
        row_9.Add(self.drugpicker, 1, wx.ALIGN_CENTER | wx.RIGHT, 5)
        row_9.Add(self.times, 0, wx.ALIGN_CENTER | wx.RIGHT, 5)
        row_9.Add(wx.StaticText(self, label='lần, lần'),
                           0, wx.ALIGN_CENTER | wx.RIGHT, 5)
        row_9.Add(
            self.dosage_per, 0, wx.ALIGN_CENTER | wx.RIGHT, 5)
        row_9.Add(self.usage_unit, 0, wx.ALIGN_CENTER | wx.RIGHT, 5)
        row_9.Add(wx.StaticText(
            self, label=u"\u21D2   Tổng cộng:"), 0, wx.ALIGN_CENTER)
        row_9.Add(
            self.quantity, 0, wx.ALIGN_CENTER | wx.RIGHT, 5)
        row_9.Add(self.sale_unit, 0, wx.ALIGN_CENTER | wx.RIGHT, 5)
        row_9.Add(self.save_drug_btn, 0,
                           wx.ALIGN_CENTER | wx.RIGHT, 5)
        row_9.Add(self.erase_drug_btn, 0,
                           wx.ALIGN_CENTER | wx.RIGHT, 5)

        row_10.Add(wx.StaticText(
            self, label='Cách dùng:'), 0, wx.CENTRE | wx.RIGHT, 5)
        row_10.Add(self.usage, 1)
        
        row_11.Add(wx.StaticText(self, label='Dặn dò:'),
                         0, wx.CENTRE | wx.RIGHT, 5)
        row_11.Add(self.followup, 1)
        
        row_12.Add(self.reuse_btn, 0, wx.RIGHT, 5)
        row_12.Add(self.sample_prescription_btn, 0)
        row_12.AddStretchSpacer()
        row_12.Add(wx.StaticText(self, label='Tổng tiền:'), 0, wx.CENTRE)
        row_12.Add(self.total_cost, 0, wx.CENTRE)

        row_13.Add(self.new_p_btn)
        row_13.Add(self.new_visit_btn)
        row_13.Add(self.save_visit_btn)

        sizer.Add(row_4, 0, wx.EXPAND)
        sizer.Add(row_5, 0, wx.EXPAND)
        sizer.Add(self.note, 0, wx.EXPAND)
        sizer.Add(row_6, 0, wx.EXPAND | wx.TOP, 3)
        sizer.Add(row_7, 0, wx.EXPAND)
        sizer.Add(row_8, 0, wx.EXPAND)
        sizer.Add(row_9, 0, wx.EXPAND)
        sizer.Add(row_10, 0, wx.EXPAND)
        sizer.Add(self.d_list, 1, wx.EXPAND | wx.TOP, 3)
        sizer.Add(row_11, 0, wx.EXPAND | wx.TOP, 3)
        sizer.Add(row_12, 0, wx.EXPAND | wx.TOP, 3)
        sizer.AddSpacer(20)
        sizer.Add(row_13, 0, wx.EXPAND | wx.BOTTOM, 10)
        self.SetSizer(sizer)
        
    def _calc_quantity(self, e):
        day = self.days.Value
        dosage = self.dosage_per.Value
        time = self.times.Value
        drug = self.drugpicker.drugWH
        try:
            assert day != 0
            assert dosage != ''
            assert time != ''
            assert drug is not None
            day = int(day)
            time = int(time)
            if "/" in dosage:
                dosage = fr(dosage)
            elif "." in dosage:
                dosage = float(dosage)
            else:
                dosage = int(dosage)
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
        try:
            assert self.drugpicker.drugWH is not None
            assert self.dosage_per.Value != ''
            assert int(self.times.Value)
            assert int(self.quantity.Value)
            
            self.d_list.Add_or_Update(**kwargs)
        except AssertionError:
            pass
        finally:
            self.drugpicker.Clear()
            self.drugpicker.SetFocus()
            self.total_cost.ChangeValue(otf.bill_int_to_str(
                setting['cong_kham_benh'] + self.d_list.total_drug_price))

    def onEraseDrug(self, e):
        d = self.drugpicker.drugWH
        try:
            assert d is not None
            self.d_list.Remove(d)
        except AssertionError:
            pass
        finally:
            self.drugpicker.Clear()
            self.total_cost.ChangeValue(otf.bill_int_to_str(
                setting['cong_kham_benh'] + self.d_list.total_drug_price))

    def onReuse(self, e):
        linedrugs = self.Parent.visit.linedrugs.copy()
        w = self.weight.Value
        d = self.days.Value
        p = self.total_cost.Value
        self.Parent.visit = None
        self.clearVisitInfo()
        self.d_list.Update(linedrugs=linedrugs)
        self.weight.ChangeValue(w)
        self.days.ChangeValue(d)
        self.total_cost.ChangeValue(p)

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
                    self.d_list.Add_or_Update()
                    
    

    def onNewPatientbtn(self, e):
        self.NewPatient()

    def onNewVisit(self, e):
        self.NewVisit()

    def onSaveVisit(self, e):
        self.SaveVisit()

    def NewPatient(self):
        with NewPatientDialog(self) as dlg:
            if dlg.ShowModal() == wx.ID_OK:
                new_patient = dbf.create_new_patient(
                    name=dlg.name.Value.upper(),
                    gender=dlg.gender.Selection,
                    birthdate=otf.wxdate2pydate(
                        dlg.birthdate.Value),
                    address=dlg.address.Value,
                    past_history=dlg.past_history.Value,
                    sess=self.Parent.sess
                )
                tab0 = self.Parent.book.GetPage(0)
                tab0.Add_new_patient(new_patient)

    def NewVisit(self):
        self.Parent.visit = None

    def SaveVisit(self):
        mv = self.Parent

        assert mv.patient is not None
        assert self.diag.Value != ""

        kwargs = {
            'pid': mv.patient.id,
            'name': self.name.Value,
            'birthdate': otf.wxdate2pydate(
                self.birthdate.Value),
            'address': self.address.Value,
            'past_history': self.past_history.Value,
            'note': self.note.Value,
            'diag': self.diag.Value,
            'weight': float(self.weight.Value),
            'days': int(self.days.Value),
            'followup': self.followup.Value,
            'bill': otf.bill_str_to_int(
                self.total_cost.Value),
            'linedrugs': self.d_list.build_linedrugs()
        }
        if mv.visit:
            ans = wx.MessageBox("Cập nhật lượt khám?", "Lưu", style=wx.YES_NO)
            if ans == wx.YES:
                p, v = dbf.save_old_visit(**kwargs, vid=mv.visit.id, sess=self.Parent.sess)
                wx.MessageBox("Đã cập nhật")
                self.updateAfterSave()
                
        else:
            ans = wx.MessageBox("Lưu lượt khám mới?", "Lưu", style=wx.YES_NO)
            if ans == wx.YES:
                p, v = dbf.save_new_visit(**kwargs, sess=self.Parent.sess)
                wx.MessageBox("Đã lưu")
                self.updateAfterSave()
                
    def updateAfterSave(self):
        self.Parent.left.updateVisitList()
              
    def updatePatientInfo(self):
        p = self.Parent.patient
        self.group_label_1.Label = f'Thông tin bệnh nhân (Mã BN: {p.id})'
        self.name.ChangeValue(p.name)
        self.gender.Selection = p.gender
        self.birthdate.SetValue(otf.pydate2wxdate(p.birthdate))
        self.age.ChangeValue(otf.bd_to_age(self.birthdate.Value).ljust(16))
        self.address.ChangeValue(p.address)
        self.past_history.ChangeValue(p.past_history)          
     
    def clearPatientInfo(self):
        self.group_label_1.Label = 'Thông tin bệnh nhân'
        self.name.ChangeValue('')
        self.gender.Selection = 0
        self.birthdate.SetValue(wx.DateTime(31, 11, 2010))
        self.age.ChangeValue("")
        self.address.ChangeValue('')
        self.past_history.ChangeValue('') 
        
    def updateVisitInfo(self):

        def _dt_to_label(p_dt):
            return ' ' * 20 + 'Giờ khám: {}:{} ngày {} tháng {} năm {}'.\
                format(str(p_dt.hour).rjust(2, '0'),
                       str(p_dt.minute).rjust(2, '0'),
                       p_dt.day,
                       p_dt.month,
                       p_dt.year)

        v = self.Parent.visit
        self.group_label_2.Label =\
            f'Thông tin lượt khám (Mã lượt khám: {v.id})'
        self.dt_label.Label = _dt_to_label(v.exam_date)
        self.note.ChangeValue(v.note)
        self.diag.ChangeValue(v.diag)
        self.weight.ChangeValue(str(v.weight))
        self.days.ChangeValue(str(v.days))
        self.drugpicker.Clear()
        self.d_list.Update(v.linedrugs)
        self.followup.ChangeValue(v.followup)

    def clearVisitInfo(self):
        self.group_label_2.Label = 'Thông tin lượt khám'
        self.dt_label.Label = ""
        self.note.ChangeValue("")
        self.diag.ChangeValue("")
        self.weight.ChangeValue('0')
        self.days.ChangeValue('2')
        self.followup.Selection = 0
        self.d_list.Clear()
        self.drugpicker.Clear()
    
    def Refresh(self):
        self.clearPatientInfo()
        self.clearVisitInfo()