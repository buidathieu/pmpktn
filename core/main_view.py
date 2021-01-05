from initialize import *
from .my_widgets.patient_book import PatientBook
from .my_widgets.visit_list import VisitList
from .my_widgets.my_button import MyButton
from .my_widgets.total_cost import TotalCost
from .my_widgets.order_book import OrderBook
from .my_widgets.search_bar import PatientSearchBar
import other_func as otf
import database.db_func as dbf
from .patient_dialog import AddPatientDialog, EditPatientDialog

from .menubar import MyMenuBar
from .accel import my_accel

import wx


class MainView(wx.Frame):

    def __init__(self, parent, *args, **kw):

        self._patient = None
        self._visit = None
        self.sess = make_session()

        super().__init__(
            parent,
            title='PHẦN MỀM PHÒNG MẠCH TƯ, created by thanhstardust@outlook.com',
            pos=(0, 20), size=window_size, *args, **kw)
        self.SetBackgroundColour(background_color)
        self._createInterface()
        self._setMenuBar()
        self._setAccelTable()
        self.patient_book.start()
        self._bind()

    def _createInterface(self):
        self._createWidgets()
        self._setSizer()

    def _createWidgets(self):
        self._create_left_widgets()
        self._create_right_widgets()

    def _setSizer(self):

        left_sizer = self._create_left_sizer()
        right_sizer = self._create_right_sizer()

        whole_sizer = wx.BoxSizer(wx.HORIZONTAL)
        whole_sizer.Add(left_sizer, 0, wx.EXPAND)
        whole_sizer.Add(right_sizer, 0,
                        wx.EXPAND | wx.LEFT | wx.RIGHT | wx.BOTTOM, 10)
        self.SetSizer(whole_sizer)

    def _create_left_widgets(self):
        self.patient_book = PatientBook(self)
        self.search_bar = PatientSearchBar(self)
        self.visit_list = VisitList(self)

    def _create_right_widgets(self):
        self.label_1 = wx.StaticText(self, label='Thông tin bệnh nhân')
        self.name = wx.TextCtrl(self, size=name_size, style=wx.TE_READONLY)
        self.gender = wx.TextCtrl(self, size=gender_size, style=wx.TE_READONLY)
        self.birthdate = wx.TextCtrl(self, size=bd_size, style=wx.TE_READONLY)
        self.age = wx.TextCtrl(self, style=wx.TE_READONLY)
        self.address = wx.TextCtrl(self, style=wx.TE_READONLY)
        self.past_history = wx.TextCtrl(self, style=wx.TE_MULTILINE, size=note_size)
        self.label_2 = wx.StaticText(self, label='Thông tin lượt khám')
        self.label_dt = wx.StaticText(self)
        self.note = wx.TextCtrl(self, size=note_size, style=wx.TE_MULTILINE)
        self.diagnosis = wx.TextCtrl(self)
        self.order_book = OrderBook(self)
        self.new_patient_btn = MyButton(
            self,
            label="Bệnh nhân mới",
            bitmap=new_p_bm)
        self.save_visit_btn = MyButton(
            self,
            label="Lưu lượt khám mới",
            bitmap=save_visit_bm)
        self.total_cost = TotalCost(self)
        self.past_history.Bind(wx.EVT_CHAR, lambda e: otf.onTab(e, self.note))
        self.note.Bind(wx.EVT_CHAR, lambda e: otf.onTab(e, self.diagnosis))

        self.name.Disable()
        self.gender.Disable()
        self.birthdate.Disable()
        self.age.Disable()
        self.address.Disable()

    def _create_left_sizer(self):
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.patient_book, 10, wx.LEFT | wx.TOP, 10)
        sizer.Add(self.search_bar, 0, wx.EXPAND | wx.LEFT | wx.TOP, 10)
        sizer.Add(wx.StaticText(self, label='Lượt khám cũ:'), 0, wx.LEFT, 20)
        sizer.Add(self.visit_list, 4, wx.EXPAND | wx.LEFT | wx.BOTTOM, 20)
        return sizer

    def _create_right_sizer(self):
        sizer = wx.BoxSizer(wx.VERTICAL)
        label_1_row = wx.BoxSizer(wx.HORIZONTAL)
        name_row = wx.BoxSizer(wx.HORIZONTAL)
        addr_row = wx.BoxSizer(wx.HORIZONTAL)
        label_2_row = wx.BoxSizer(wx.HORIZONTAL)
        datetime_row = wx.BoxSizer(wx.HORIZONTAL)
        diag_row = wx.BoxSizer(wx.HORIZONTAL)
        order_book_row = wx.BoxSizer(wx.HORIZONTAL)
        btn_row = wx.BoxSizer(wx.HORIZONTAL)

        label_1_row.Add(self.label_1, 0)
        label_1_row.Add(wx.StaticLine(self), 1, wx.ALIGN_CENTER)
        name_row.Add(wx.StaticText(self, label='Họ tên: '), 0, wx.ALIGN_CENTER)
        name_row.Add(self.name, 0, wx.ALIGN_CENTER | wx.RIGHT, 5)
        name_row.Add(self.gender, 0, wx.ALIGN_CENTER | wx.RIGHT, 5)
        name_row.Add(wx.StaticText(self, label='Ngày sinh: '), 0, wx.ALIGN_CENTER)
        name_row.Add(self.birthdate, 0, wx.ALIGN_CENTER | wx.RIGHT, 5)
        name_row.Add(wx.StaticText(self, label='Tuổi: '), 0, wx.ALIGN_CENTER)
        name_row.Add(self.age, 1, wx.ALIGN_CENTER)
        addr_row.Add(wx.StaticText(self, label='Địa chỉ: '), 0, wx.ALIGN_CENTER)
        addr_row.Add(self.address, 1, wx.EXPAND)
        label_2_row.Add(self.label_2)
        label_2_row.Add(wx.StaticLine(self), 1, wx.ALIGN_CENTER)
        datetime_row.Add(wx.StaticText(
            self,
            label='Bệnh sử, triệu chứng, ghi chú,... (theo từng lượt khám): '))
        datetime_row.Add(self.label_dt, 1, wx.RIGHT, 10)
        diag_row.Add(wx.StaticText(self, label='Chẩn đoán:'),
                     0, wx.ALIGN_CENTER | wx.TOP, 3)
        diag_row.Add(self.diagnosis, 1)
        order_book_row.Add(self.order_book)
        btn_row.Add(self.new_patient_btn, 0)
        btn_row.Add(self.save_visit_btn, 0)
        btn_row.AddStretchSpacer()
        btn_row.Add(wx.StaticText(self, label='Tổng tiền: '), 0, wx.CENTRE)
        btn_row.Add(self.total_cost, 0, wx.CENTRE)

        sizer.Add(label_1_row, 0, wx.EXPAND)
        sizer.Add(name_row, 0, wx.EXPAND)
        sizer.Add(addr_row, 0, wx.EXPAND | wx.TOP, 3)
        sizer.Add(wx.StaticText(self, label='Bệnh nền, dị ứng: '), 0, wx.TOP, 3)
        sizer.Add(self.past_history, 0, wx.EXPAND)
        sizer.Add(label_2_row, 0, wx.EXPAND)
        sizer.Add(datetime_row, 0, wx.EXPAND)
        sizer.Add(self.note, 0, wx.EXPAND)
        sizer.Add(diag_row, 0, wx.EXPAND | wx.TOP, 3)
        sizer.Add(order_book_row, 0, wx.EXPAND | wx.TOP, 3)
        sizer.Add(btn_row, 0, wx.EXPAND | wx.TOP, 3)
        return sizer

    def _setMenuBar(self):
        self.menubar = MyMenuBar(self)
        self.SetMenuBar(self.menubar)

    def _setAccelTable(self):
        self.SetAcceleratorTable(my_accel)

    @property
    def patient(self):
        return self._patient

    @patient.setter
    def patient(self, p):
        self._patient = p
        if p:
            self.onPatientSelect()
        else:
            self.onPatientDeselect()

    @property
    def visit(self):
        return self._visit

    @visit.setter
    def visit(self, v):
        self._visit = v
        if v:
            self.onVisitSelect()
        else:
            self.onVisitDeselect()

    def refresh(self):
        self.patient_book.refresh()
        self.patient = None
        self.order_book.refresh()

    def onClose(self, e):
        dlg = wx.MessageDialog(
            self, "Kết thúc", "Close app?", style=wx.OK | wx.CANCEL)
        if dlg.ShowModal() == wx.ID_OK:
            self.Destroy()

    def Destroy(self):
        self.sess.commit()
        self.sess.close()
        super().Destroy()

    def onPatientSelect(self):
        p = self.patient
        self.visit_list.buildVisitList()
        self.label_1.Label = f'Thông tin bệnh nhân (Mã BN: {p.id}) '
        self.name.ChangeValue(p.name)
        self.gender.ChangeValue(p.gender)
        self.birthdate.ChangeValue(p.birthdate.strftime("%d/%m/%Y"))
        self.age.ChangeValue(otf.bd_to_age(p.birthdate).ljust(16))
        self.address.ChangeValue(p.address)
        self.past_history.ChangeValue(p.past_history)

    def onPatientDeselect(self):
        self.visit = None
        self.visit_list.DeleteAllItems()
        self.label_1.Label = 'Thông tin bệnh nhân '
        self.name.ChangeValue("")
        self.gender.ChangeValue("")
        self.birthdate.ChangeValue("")
        self.age.ChangeValue("")
        self.address.ChangeValue("")
        self.past_history.ChangeValue("")

    def onVisitSelect(self):

        def _dt_to_label(p_dt):
            return ' ' * 20 + 'Giờ khám: {}:{} ngày {} tháng {} năm {} '.\
                format(str(p_dt.hour).rjust(2, '0'),
                       str(p_dt.minute).rjust(2, '0'),
                       p_dt.day,
                       p_dt.month,
                       p_dt.year)
        v = self.visit
        self.label_2.Label = f'Thông tin lượt khám (Mã lượt khám: {v.id}) '
        self.label_dt.Label = _dt_to_label(v.exam_date)
        self.note.ChangeValue(v.note)
        self.diagnosis.ChangeValue(v.diagnosis)
        pg = self.order_book.GetPage(0)
        pg.weight.ChangeValue(str(v.weight))
        pg.days.ChangeValue(str(v.days))
        pg.drug_picker.Clear()
        pg.d_list.Populate(v.linedrugs)
        self.total_cost.ChangeValue(v.bill)
        self.save_visit_btn.SetLabel("Cập nhật lượt khám cũ")
        self.Layout()

    def onVisitDeselect(self):
        self.label_2.Label = 'Thông tin lượt khám '
        self.label_dt.Label = ""
        self.note.ChangeValue("")
        self.diagnosis.ChangeValue("")
        pg = self.order_book.GetPage(0)
        pg.weight.ChangeValue('0')
        pg.days.ChangeValue(
            str(user_setting['so_ngay_toa_ve_mac_dinh']))
        pg.drug_picker.Clear()
        pg.d_list.Clear()
        self.total_cost.ChangeValue(user_setting['cong_kham_benh'])
        self.save_visit_btn.SetLabel("Lưu lượt khám mới")
        self.Layout()

    def calc_price(self):
        price = user_setting["cong_kham_benh"]
        price += self.order_book.GetPage(0).d_list.get_total_price()
        self.total_cost.ChangeValue(price)

    def _bind(self):
        self.Bind(wx.EVT_CLOSE, self.onClose)
        self.new_patient_btn.Bind(wx.EVT_BUTTON, lambda e: self.onCreateNewPatient())
        self.save_visit_btn.Bind(wx.EVT_BUTTON, lambda e: self.onSaveVisit())

    def onCreateNewPatient(self):
        dialog = AddPatientDialog(self)
        if dialog.ShowModal() == wx.ID_OK:
            new_patient = dialog.add_patient()
            self.patient_book.GetPage(0).append_new_patient(new_patient)

    def onEditPatientInfo(self):
        page = self.patient_book.GetSelection()
        page = self.patient_book.GetPage(page)
        idx = page.GetFirstSelected()
        if idx == -1:
            wx.MessageBox("Vui lòng chọn một bệnh nhân", "Chỉnh sửa thông tin bệnh nhân")
        else:
            patient = page.p_list[idx]
            dialog = EditPatientDialog(self, patient)
            if dialog.ShowModal() == wx.ID_OK:
                edited_patient = dialog.edit_patient()
                page.renew_patient_info(edited_patient, idx)
                wx.MessageBox("Đã cập nhật")

    def onSaveVisit(self):
        pg = self.order_book.GetPage(0)

        def check_kwargs():
            if self.patient is not None and \
                    self.diagnosis.Value != "" and \
                    float(pg.weight.Value) >= 0 and \
                    int(pg.days.Value) >= 0:
                return True

        if check_kwargs():
            if self.visit:
                self._save_old_visit()
            else:
                self._save_new_visit()
        else:
            wx.MessageBox("Bạn chưa chọn bệnh nhân hoặc chưa gõ chẩn đoán, cân nặng, số ngày cho toa", "Lỗi")

    def _save_old_visit(self):
        pg = self.order_book.GetPage(0)
        kwargs = {
            'p': self.patient,
            'v': self.visit,
            'past_history': self.past_history.Value,
            'note': self.note.Value,
            'diagnosis': self.diagnosis.Value,
            'weight': float(pg.weight.Value),
            'days': int(pg.days.Value),
            'bill': otf.bill_str_to_int(
                self.total_cost.Value),
            'linedrugs': pg.d_list.build_linedrugs(),
        }
        ans = wx.MessageBox(
            f"Cập nhật lượt khám cũ lúc {self.visit.exam_date.strftime('%d/%m/%Y %H:%M')}?",
            "Cập nhật",
            style=wx.YES_NO)
        if ans == wx.YES:
            succeed = dbf.save_old_visit(**kwargs, sess=self.sess)
            if succeed == -1:
                wx.MessageBox("Kho thuốc không đủ")
            else:
                wx.MessageBox("Đã cập nhật")
            self.visit_list.buildVisitList()

    def _save_new_visit(self):
        pg = self.order_book.GetPage(0)
        kwargs = {
            'p': self.patient,
            'past_history': self.past_history.Value,
            'note': self.note.Value,
            'diagnosis': self.diagnosis.Value,
            'weight': float(pg.weight.Value),
            'days': int(pg.days.Value),
            'bill': otf.bill_str_to_int(
                self.total_cost.Value),
            'linedrugs': pg.d_list.build_linedrugs(),
        }
        ans = wx.MessageBox(
            "Lưu lượt khám mới?", "Lưu",
            style=wx.YES_NO)
        if ans == wx.YES:
            succeed = dbf.save_new_visit(**kwargs, sess=self.sess)
            if succeed == -1:
                wx.MessageBox("Kho thuốc không đủ")
            else:
                wx.MessageBox("Đã lưu")
            self.visit_list.buildVisitList()
