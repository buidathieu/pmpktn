from initialize import *
import core.db.db_func as dbf
import other_func as otf
import wx
import wx.adv


class BasePatientDialog(wx.Dialog):
    def __init__(self, parent, title):
        super().__init__(parent, title=title)
        self.mv = parent
        self.name = wx.TextCtrl(self, size=name_size)
        self.gender = self._createGender()
        self.birthdate = self._createBirthdate()
        self.age = self._createAge()
        self.address = wx.TextCtrl(self)

        self.Bind(wx.EVT_KEY_DOWN, self.onESC)
        self._setSizer()

    def _createGender(self):
        w = wx.Choice(self, choices=['nam', 'nữ'])
        w.Selection = 0
        return w

    def _createBirthdate(self):

        def onBirthdateChange(e):
            self.age.ChangeValue(otf.bd_to_age(w.Value).ljust(16))
            e.Skip()

        w = wx.adv.DatePickerCtrl(self, style=wx.adv.DP_DROPDOWN)
        w.Bind(wx.adv.EVT_DATE_CHANGED, onBirthdateChange)
        return w

    def _createAge(self):

        def onAgeChange(e):
            self.birthdate.SetValue(otf.age_to_bd(w.Value))
            e.Skip()

        w = wx.TextCtrl(self)
        w.Bind(wx.EVT_TEXT, onAgeChange)
        return w

    def _setSizer(self):
        entry_sizer = wx.FlexGridSizer(rows=6, cols=2, vgap=5, hgap=2)
        entry_sizer.AddMany([(wx.StaticText(self, label="Tên bệnh nhân: "),),
                             (self.name, 0, wx.EXPAND),
                             (wx.StaticText(self, label="Giới: "),),
                             (self.gender),
                             (wx.StaticText(self, label="Ngày sinh: "),),
                             (self.birthdate),
                             (wx.StaticText(self, label="Tuổi: "),),
                             (self.age),
                             (wx.StaticText(self, label="Địa chỉ: "),),
                             (self.address, 0, wx.EXPAND),
                             ])
        btn_sizer = wx.BoxSizer(wx.HORIZONTAL)
        btn_sizer.AddStretchSpacer()
        btn_sizer.Add(self.CreateButtonSizer(wx.OK | wx.CANCEL), 1)
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(entry_sizer, 0, wx.ALL ^ wx.RIGHT, 10)
        sizer.Add(btn_sizer, 0, wx.ALL ^ wx.RIGHT, 10)
        self.SetSizerAndFit(sizer)

    def onESC(self, e):
        if e.GetKeyCode() == wx.WXK_ESCAPE:
            self.EndModal(wx.ID_CANCEL)
        else:
            e.Skip()


class AddPatientDialog(BasePatientDialog):

    def __init__(self, parent):
        super().__init__(parent, title="Thêm bệnh nhân mới")

    def add_patient(self):
        kwargs = {'name': self.name.Value.upper(),
                  'gender': ['nam', 'nữ'][self.gender.Selection],
                  'birthdate': otf.wxdate2pydate(self.birthdate.Value),
                  'address': self.address.Value
                  }
        new_patient = dbf.add_patient(**kwargs, sess=self.mv.sess)
        return new_patient


class EditPatientDialog(BasePatientDialog):

    def __init__(self, parent, patient):
        super().__init__(parent, title="Chỉnh sửa thông tin bệnh nhân")
        self.patient = patient
        self.Populate()

    def Populate(self):
        self.name.ChangeValue(self.patient.name)
        self.gender.Selection = ['nam', 'nữ'].index(self.patient.gender)
        self.birthdate.SetValue(otf.pydate2wxdate(self.patient.birthdate))
        self.age.ChangeValue(otf.bd_to_age(self.birthdate.Value).ljust(16))
        self.address.ChangeValue(self.patient.address)

    def edit_patient(self):
        kwargs = {
            'patient': self.patient,
            'name': self.name.Value.upper(),
            'gender': ['nam', 'nữ'][self.gender.Selection],
            'birthdate': otf.wxdate2pydate(self.birthdate.Value),
            'address': self.address.Value}
        edited_patient = dbf.edit_patient(
            **kwargs, sess=self.mv.sess)
        return edited_patient
