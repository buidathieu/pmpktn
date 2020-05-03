from core.add_a_new_patient_dialog import NewPatientDialog
from core.__init__ import *
import db_sql.db_func as dbf
from db_sql.__init__ import Session
import wx


class NurseView(wx.Frame):

    def __init__(self, parent):
        super().__init__(parent, title='Nhận bệnh')
        self.sess = Session()

        self.search_name = self._createSearchName()
        self.search_gender = self._createSearchGender()
        self.search_birthyear = self._createSearchBirthyear()

        self.search_button = self._createSearchButton()
        self.add_patient_button = self._createAddPatientButton()
        self.add_queue_button = self._createAddQueueButton()

        self.p_listctrl = self._createPatientListCtrl()
        self.p_list = []

        self.queue_listctrl = self._createQueueListCtrl()
        self.queue_list = []

        self.timer = self.RefreshQueueTimer()

        self._setsizer()
        self._setMenuBar()
        self._setAccelTable()

        self.Bind(wx.EVT_CLOSE, self.onClose)

    def _setsizer(self):

        search_row = wx.BoxSizer(wx.HORIZONTAL)
        search_row.AddMany([
            (self.search_name, 1, wx.ALL, 10),
            (self.search_gender, 0, wx.ALL ^ wx.LEFT, 10),
            (self.search_birthyear, 0, wx.ALL ^ wx.LEFT, 10)
        ])

        btn_row = wx.BoxSizer(wx.HORIZONTAL)
        btn_row.AddMany([
            (self.search_button, 0, wx.ALL, 10),
            (self.add_patient_button, 0, wx.ALL ^ wx.LEFT, 10),
            (self.add_queue_button, 0, wx.ALL ^ wx.LEFT, 10)
        ])

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(search_row, 0, wx.EXPAND)
        sizer.Add(btn_row)
        sizer.Add(wx.StaticText(self, label="Kết quả tìm kiếm:"), 0, wx.LEFT, 20)
        sizer.Add(self.p_listctrl, 0, wx.ALL, 10)
        sizer.Add(wx.StaticText(
            self, label="Danh sách chờ khám:"), 0, wx.LEFT, 20)
        sizer.Add(self.queue_listctrl, 1, wx.EXPAND | wx.ALL, 10)
        self.SetSizerAndFit(sizer)

    def _createSearchName(self):
        w = wx.TextCtrl(self)
        w.Hint = "Họ tên"
        return w

    def _createSearchGender(self):
        w = wx.Choice(self, choices=[gender_dict[0], gender_dict[1]])
        w.Selection = 0
        return w

    def _createSearchBirthyear(self):
        w = wx.TextCtrl(self)
        w.Hint = "Năm sinh"
        return w

    def _createSearchButton(self):
        w = wx.Button(self, label='Tìm kiếm')
        w.Bind(wx.EVT_BUTTON, lambda e: self.Search())
        return w

    def _createAddPatientButton(self):
        w = wx.Button(self, label='Thêm bệnh nhân mới')
        w.Bind(wx.EVT_BUTTON, lambda e: self.NewPatient())
        return w

    def _createAddQueueButton(self):
        w = wx.Button(self, label='Thêm vào DS chờ khám')
        w.Bind(wx.EVT_BUTTON, lambda e: self.AddQueue())
        w.Disable()
        return w

    def _createPatientListCtrl(self):
        w = wx.ListCtrl(self, style=wx.LC_REPORT)
        w.AppendColumn("Mã bn", width=ma_bn_width)
        w.AppendColumn("Tên bệnh nhân", width=bn_width)
        w.AppendColumn("Giới tính", width=gioi_width)
        w.AppendColumn("Ngày tháng năm sinh", width=date_width)
        w.Bind(wx.EVT_LIST_ITEM_SELECTED,
               lambda e: self.add_queue_button.Enable())
        w.Bind(wx.EVT_LIST_ITEM_DESELECTED,
               lambda e: self.add_queue_button.Disable())
        return w

    def _createQueueListCtrl(self):
        w = wx.ListCtrl(self, style=wx.LC_REPORT)
        w.AppendColumn("Mã bn", width=ma_bn_width)
        w.AppendColumn("Tên bệnh nhân", width=bn_width)
        w.AppendColumn("Giới tính", width=gioi_width)
        w.AppendColumn("Ngày tháng năm sinh", width=date_width)
        return w

    def _setMenuBar(self):
        w = wx.MenuBar()
        menu = wx.Menu()

        newPatientMenu = menu.Append(wx.ID_NEW, "Thêm bệnh nhân mới\tF1")
        addQueueMenu = menu.Append(wx.ID_ADD, "Thêm vào DS chờ khám\tF2")
        exitMenu = menu.Append(wx.ID_EXIT, "&Exit\tALT+F4")

        w.Append(menu, 'Nhận bệnh')

        w.Bind(wx.EVT_MENU, lambda e: self.NewPatient(), newPatientMenu)
        w.Bind(wx.EVT_MENU, lambda e: self.AddQueue(), addQueueMenu)
        w.Bind(wx.EVT_MENU, lambda e: self.Close(), exitMenu)
        self.SetMenuBar(w)

    def _setAccelTable(self):
        accel = wx.AcceleratorTable(
            [wx.AcceleratorEntry(wx.ACCEL_NORMAL, wx.WXK_F1, wx.ID_NEW),
             wx.AcceleratorEntry(wx.ACCEL_NORMAL, wx.WXK_F2, wx.ID_ADD),
             wx.AcceleratorEntry(wx.ACCEL_ALT, wx.WXK_F4, wx.ID_EXIT)])
        self.SetAcceleratorTable(accel)

    # Functions

    def NewPatient(self):
        with NewPatientDialog(self) as dlg:
            if dlg.ShowModal() == wx.ID_OK:
                new_patient = dlg.add_a_new_patient(sess=self.sess)
                with wx.MessageDialog(self,
                                      "Thêm vào danh sách chờ khám?",
                                      "Thêm vào danh sách chờ khám?",
                                      style=wx.OK | wx.CANCEL) as dlg:
                    if dlg.ShowModal() == wx.ID_OK:
                        self.AddQueue(new_patient)

    def AddQueue(self, patient=None):
        if not patient:
            patient_idx = self.p_listctrl.GetFirstSelected()
            patient = self.p_list[patient_idx]
        if patient.id in [vq.patient_id for vq in self.queue_list]:
            wx.MessageBox('Đã có trong danh sách chờ khám',
                          "Không thực hiện được")
        else:
            dbf.add_new_visitqueue(patient.id, sess=self.sess)
            self.RefreshQueue()

    def RefreshQueue(self):
        self.queue_listctrl.DeleteAllItems()
        self.queue_list = dbf.get_visitqueue(sess=self.sess).all()
        for vq in self.queue_list:
            p = vq.patient
            self.queue_listctrl.Append(
                [p.id, p.name, gender_dict[int(p.gender)], p.birthdate])

    def RefreshQueueTimer(self):
        self.RefreshQueue()
        return wx.CallLater(1000 * 60 * 5, self.RefreshQueueTimer)

    def Search(self):
        self.p_listctrl.DeleteAllItems()
        self.p_list = dbf.search_patient(
            name=self.search_name.Value.upper(),
            gender=bool(self.search_gender.Selection),
            birthyear=self.search_birthyear.Value,
            sess=self.sess).all()
        for p in self.p_list:
            self.p_listctrl.Append(
                [p.id, p.name, gender_dict[int(p.gender)], p.birthdate])

    def onClose(self, e):
        dlg = wx.MessageDialog(self, "", "Close app?", style=wx.OK | wx.CANCEL)
        if dlg.ShowModal() == wx.ID_OK:
            e.Skip()
            self.sess.commit()
            self.sess.close()
