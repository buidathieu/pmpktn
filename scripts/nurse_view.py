from patient_dialog import AddPatientDialog, EditPatientDialog
import db_sql.db_func as dbf
import other_func as otf
from initialize import *
import wx
import logging


class NurseView(wx.Frame):

    def __init__(self, parent):
        super().__init__(parent, title='Nhận bệnh')
        self.sess = Session()
        logging.debug('NurseView initialized, session opened')

        self.SetBackgroundColour(wx.Colour(206, 219, 186))

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
        sizer.Add(
            wx.StaticText(
                self,
                label="Kết quả tìm kiếm:"),
            0,
            wx.LEFT,
            20)
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
        w = wx.Choice(self, choices=[gender_dict[0], gender_dict[1], ''])
        w.Selection = 2
        return w

    def _createSearchBirthyear(self):
        w = wx.TextCtrl(self)
        w.Hint = "Năm sinh"
        w.Bind(wx.EVT_CHAR, lambda e: otf.only_nums(e))
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

        homeMenu = wx.Menu()
        menuRefresh = homeMenu.Append(wx.ID_REFRESH, "Refresh\tF5")
        menuExit = homeMenu.Append(wx.ID_EXIT, "Exit\tALT+F4")

        patientMenu = wx.Menu()
        menuNewPatient = patientMenu.Append(
            wx.ID_NEW, "Thêm bệnh nhân mới\tF1")
        menuEditPatient = patientMenu.Append(
            wx.ID_EDIT, "Chỉnh sửa thông tin bệnh nhân\tF2")

        queueMenu = wx.Menu()
        menuAddQueue = queueMenu.Append(wx.ID_ADD, "Thêm vào DS chờ khám\tF3")
        menuRemoveQueue = queueMenu.Append(
            wx.ID_REMOVE, "Xoá khỏi DS chờ khám\tF4")

        w.Append(homeMenu, "Home")
        w.Append(patientMenu, 'Bệnh nhân')
        w.Append(queueMenu, "Chờ khám")

        w.Bind(wx.EVT_MENU, lambda e: self.Refresh(), menuRefresh)
        w.Bind(wx.EVT_MENU, self.onClose, menuExit)
        w.Bind(wx.EVT_MENU, lambda e: self.NewPatient(), menuNewPatient)
        w.Bind(wx.EVT_MENU, lambda e: self.EditPatient(), menuEditPatient)
        w.Bind(wx.EVT_MENU, lambda e: self.AddQueue(), menuAddQueue)
        w.Bind(wx.EVT_MENU, lambda e: self.RemoveQueue(), menuRemoveQueue)

        self.SetMenuBar(w)

    def _setAccelTable(self):
        accel = wx.AcceleratorTable(
            [wx.AcceleratorEntry(wx.ACCEL_NORMAL, wx.WXK_F1, wx.ID_NEW),
             wx.AcceleratorEntry(wx.ACCEL_NORMAL, wx.WXK_F2, wx.ID_EDIT),
             wx.AcceleratorEntry(wx.ACCEL_NORMAL, wx.WXK_F3, wx.ID_ADD),
             wx.AcceleratorEntry(wx.ACCEL_NORMAL, wx.WXK_F4, wx.ID_REMOVE),
             wx.AcceleratorEntry(wx.ACCEL_ALT, wx.WXK_F4, wx.ID_EXIT),
             wx.AcceleratorEntry(wx.ACCEL_NORMAL, wx.WXK_F5, wx.ID_REFRESH)])
        self.SetAcceleratorTable(accel)

    # Functions

    def NewPatient(self):
        with AddPatientDialog(self) as dlg:
            if dlg.ShowModal() == wx.ID_OK:
                new_patient = dlg.add_patient()
                with wx.MessageDialog(self,
                                      "Thêm vào danh sách chờ khám?",
                                      "Thêm vào danh sách chờ khám?",
                                      style=wx.OK | wx.CANCEL) as dlg:
                    if dlg.ShowModal() == wx.ID_OK:
                        self.AddQueue(new_patient)

    def EditPatient(self):
        idx = self.p_listctrl.GetFirstSelected()
        if idx >= 0:
            patient = self.p_list[idx]
            with EditPatientDialog(self, patient) as dlg:
                if dlg.ShowModal() == wx.ID_OK:
                    edited_patient = dlg.edit_patient()
                    self.p_listctrl.DeleteAllItems()
                    self.p_list = []
        else:
            wx.MessageBox("Chưa chọn bệnh nhân", "Lỗi", parent=self)

    def AddQueue(self, patient=None):
        if not patient:
            patient_idx = self.p_listctrl.GetFirstSelected()
            patient = self.p_list[patient_idx]
        logging.debug(f'Adding {patient.name} to waiting queue')
        if patient.id in [q.patient_id for q in self.queue_list]:
            logging.debug(f'Patient already in waiting queue. AddQueue failed')
            wx.MessageBox('Đã có trong danh sách chờ khám',
                          "Không thực hiện được")
        else:
            logging.debug(f'{patient.name} added to waiting queue')
            dbf.add_new_visitqueue(patient.id, sess=self.sess)
            self.RefreshQueue()

    def RemoveQueue(self):
        idx = self.queue_listctrl.GetFirstSelected()
        if idx >= 0:
            queue = self.queue_list[idx]
            with wx.MessageDialog(self,
                                  f"Xoá {queue.patient.name} ra khỏi danh sách chờ khám?",
                                  "Xoá khỏi DS chờ khám",
                                  style=wx.OK | wx.CANCEL) as dlg:
                if dlg.ShowModal() == wx.ID_OK:
                    logging.debug(
                        f"Deleted {queue.patient.name} from waiting queue")
                    dbf.remove_visitqueue(queue, sess=self.sess)
                    self.RefreshQueue()
        else:
            wx.MessageBox("Chưa chọn bệnh nhân", "Lỗi", parent=self)

    def RefreshQueue(self):
        logging.debug('NurseView waiting queue rebuilt')
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
        kwargs = {
            'name': self.search_name.Value.upper(),
            'gender': self.search_gender.Selection,
            'birthyear': self.search_birthyear.Value,
            'sess': self.sess
        }
        logging.debug(f'NurseView search {kwargs}')
        self.p_listctrl.DeleteAllItems()
        self.p_list = dbf.search_patient(**kwargs).all()
        for p in self.p_list:
            self.p_listctrl.Append(
                [p.id, p.name, gender_dict[int(p.gender)], p.birthdate])

    def onClose(self, e):
        with wx.MessageDialog(self, "Kết thúc", "Close app?", style=wx.OK | wx.CANCEL) as dlg:
            if dlg.ShowModal() == wx.ID_OK:
                self.Destroy()

    def Refresh(self):
        self.search_name.ChangeValue("")
        self.search_gender.Selection = 2
        self.search_birthyear.ChangeValue("")
        self.p_listctrl.DeleteAllItems()
        self.p_list = []
        self.RefreshQueue()

    def Destroy(self):
        self.sess.commit()
        self.sess.close()
        logging.debug('NurseView destroyed. session closed')
        super().Destroy()
