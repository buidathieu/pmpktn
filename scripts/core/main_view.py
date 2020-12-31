from initialize import *
from .my_widgets.patient_book import PatientBook
from .my_widgets.visit_list import VisitList
import other_func as otf
from .my_widgets.my_button import MyButton
from .my_widgets.total_cost import TotalCost

# from .menubar import MyMenuBar
# from .accel import my_accel
# from .binding import button_bindings

from .core_func import onPatientSelect, onPatientDeselect, onVisitSelect, onVisitDeselect
import wx
import logging


class MainView(wx.Frame):

    def __init__(self, parent, *args, **kw):

        self._patient = None
        self._visit = None
        self.sess = Session()
        logging.debug("Mainview initialized, session opened")

        super().__init__(
            parent,
            title='APP PHÒNG MẠCH TƯ, created by thanhstardust@outlook.com',
            pos=(0, 20), size=window_size, *args, **kw)
        self.SetBackgroundColour(wx.Colour(206, 219, 186))

        self._createInterface()
        # self._setMenuBar()
        # self._setAccelTable()
        # button_bindings(self)
        self.Bind(wx.EVT_CLOSE, self.onClose)

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
        self.book = PatientBook(self)
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
        self.save_visit_btn = MyButton(
            self,
            label="Lưu lượt khám (F3)",
            bitmap=save_visit_bm)
        self.total_cost = TotalCost(self)

        self.past_history.Bind(wx.EVT_CHAR, lambda e: otf.onTab(e, self.note))
        self.note.Bind(wx.EVT_CHAR, lambda e: otf.onTab(e, self.diagnosis))

    def _create_left_sizer(self):
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.book, 10, wx.LEFT | wx.TOP, 10)
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
        btn_row = wx.BoxSizer(wx.HORIZONTAL)

        label_1_row.Add(self.label_1, 0)
        label_1_row.Add(wx.StaticLine(self), 1, wx.ALIGN_CENTER)
        name_row.Add(wx.StaticText(self, label='Họ tên:'), 0, wx.ALIGN_CENTER)
        name_row.Add(self.name, 0, wx.ALIGN_CENTER | wx.RIGHT, 5)
        name_row.Add(self.gender, 0, wx.ALIGN_CENTER | wx.RIGHT, 5)
        name_row.Add(wx.StaticText(self, label='Ngày sinh:'), 0, wx.ALIGN_CENTER)
        name_row.Add(self.birthdate, 0, wx.ALIGN_CENTER | wx.RIGHT, 5)
        name_row.Add(wx.StaticText(self, label='Tuổi:'), 0, wx.ALIGN_CENTER)
        name_row.Add(self.age, 1, wx.ALIGN_CENTER)
        addr_row.Add(wx.StaticText(self, label='Địa chỉ:'), 0, wx.ALIGN_CENTER)
        addr_row.Add(self.address, 1, wx.EXPAND)
        label_2_row.Add(self.label_2)
        label_2_row.Add(wx.StaticLine(self), 1, wx.ALIGN_CENTER)
        datetime_row.Add(wx.StaticText(
            self,
            label='Bệnh sử, triệu chứng, ghi chú,... (theo từng lượt khám):'))
        datetime_row.Add(self.label_dt, 1, wx.RIGHT, 10)
        diag_row.Add(wx.StaticText(self, label='Chẩn đoán:'),
                     0, wx.ALIGN_CENTER | wx.TOP, 3)
        diag_row.Add(self.diagnosis, 1)
        btn_row.Add(self.save_visit_btn, 0, wx.CENTRE)
        btn_row.AddStretchSpacer()
        btn_row.Add(wx.StaticText(self, label='Tổng tiền:'), 0, wx.CENTRE)
        btn_row.Add(self.total_cost, 0, wx.CENTRE)

        sizer.Add(label_1_row, 0, wx.EXPAND)
        sizer.Add(name_row, 0, wx.EXPAND)
        sizer.Add(addr_row, 0, wx.EXPAND | wx.TOP, 3)
        sizer.Add(wx.StaticText(self, label='Bệnh nền, dị ứng:'), 0, wx.TOP, 3)
        sizer.Add(self.past_history, 0, wx.EXPAND)
        sizer.Add(label_2_row, 0, wx.EXPAND)
        sizer.Add(datetime_row, 0, wx.EXPAND)
        sizer.Add(self.note, 0, wx.EXPAND)
        sizer.Add(diag_row, 0, wx.EXPAND | wx.TOP, 3)
        sizer.Add(btn_row, 0, wx.EXPAND | wx.TOP, 3)
        return sizer

    # def _setMenuBar(self):
    #     self.menubar = MyMenuBar(self)
    #     self.SetMenuBar(self.menubar)

    # def _setAccelTable(self):
    #     self.SetAcceleratorTable(my_accel)

    @property
    def patient(self):
        return self._patient

    @patient.setter
    def patient(self, p):
        self._patient = p
        logging.debug('Set mainview patient = {}'.format(p))
        if p:
            onPatientSelect(self, p)
        else:
            self.visit = None
            onPatientDeselect(self)

    @property
    def visit(self):
        return self._visit

    @visit.setter
    def visit(self, v):
        self._visit = v
        logging.debug('Set mainview visit = {}'.format(v))
        if v:
            onVisitSelect(self, v)
        else:
            onVisitDeselect(self)

    def refresh(self):
        self.book.refresh()
        self.patient = None

    def onClose(self, e):
        dlg = wx.MessageDialog(
            self, "Kết thúc", "Close app?", style=wx.OK | wx.CANCEL)
        if dlg.ShowModal() == wx.ID_OK:
            self.Destroy()

    def Destroy(self):
        logging.debug('Mainview destroyed, session closed')
        self.sess.commit()
        self.sess.close()
        super().Destroy()
