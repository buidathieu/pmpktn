from initialize import *
from core.__init__ import *
from core.custom_ctrl import *
import other_func.other_func as otf
import wx
import wx.adv


class Basic_Info_Panel(wx.Panel):

    def __init__(self, parent):
        super().__init__(parent)
        self._createWidgets()
        self._setSizer()

    def _createWidgets(self):
        self.group_label = wx.StaticText(self, label='Thông tin bệnh nhân')
        self.name = self._createName()
        self.gender = self._createGender()
        self.birthdate = self._createBirthdate()
        self.age = self._createAge()
        self.address = wx.TextCtrl(self)
        self.past_history = self._createPastHistory()

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

    def _createPastHistory(self):

        def onTab(e):
            if e.KeyCode == wx.WXK_TAB:
                self.Parent.visit_info.note.SetFocus()
            else:
                e.Skip()

        w = wx.TextCtrl(self, style=wx.TE_MULTILINE, size=note_size)
        w.Bind(wx.EVT_CHAR, onTab)
        return w

    def _setSizer(self):
        group_row = wx.BoxSizer(wx.HORIZONTAL)
        name_row = wx.BoxSizer(wx.HORIZONTAL)
        addr_row = wx.BoxSizer(wx.HORIZONTAL)
        sizer = wx.BoxSizer(wx.VERTICAL)

        group_row.Add(self.group_label, 0)
        group_row.Add(wx.StaticLine(self), 1, wx.ALIGN_CENTER)
        name_row.Add(wx.StaticText(
            self, label='Họ tên:'), 0, wx.ALIGN_CENTER)
        name_row.Add(self.name, 0, wx.ALIGN_CENTER | wx.RIGHT, 5)
        name_row.Add(self.gender, 0, wx.ALIGN_CENTER | wx.RIGHT, 5)
        name_row.Add(wx.StaticText(
            self, label='Ngày sinh:'), 0, wx.ALIGN_CENTER)
        name_row.Add(self.birthdate, 0, wx.ALIGN_CENTER | wx.RIGHT, 5)
        name_row.Add(wx.StaticText(
            self, label='Tuổi:'), 0, wx.ALIGN_CENTER)
        name_row.Add(self.age, 1, wx.ALIGN_CENTER)
        addr_row.Add(wx.StaticText(
            self, label='Địa chỉ:'), 0, wx.ALIGN_CENTER)
        addr_row.Add(self.address, 1, wx.EXPAND)
        sizer.Add(group_row, 0, wx.EXPAND)
        sizer.Add(name_row, 0, wx.EXPAND)
        sizer.Add(addr_row, 0, wx.EXPAND | wx.TOP, 3)
        sizer.Add(wx.StaticText(
            self, label='Bệnh nền, dị ứng:'),
            0, wx.TOP, 3)
        sizer.Add(self.past_history, 0, wx.EXPAND)
        self.SetSizer(sizer)

    def Update(self):
        p = self.Parent.patient
        self.group_label.Label = f'Thông tin bệnh nhân (Mã BN: {p.id})'
        self.name.ChangeValue(p.name)
        self.gender.Selection = p.gender
        self.birthdate.SetValue(otf.pydate2wxdate(p.birthdate))
        self.age.ChangeValue(otf.bd_to_age(self.birthdate.Value).ljust(16))
        self.address.ChangeValue(p.address)
        self.past_history.ChangeValue(p.past_history)

    def Clear(self):
        self.group_label.Label = 'Thông tin bệnh nhân'
        self.name.ChangeValue('')
        self.gender.Selection = 0
        self.birthdate.SetValue(wx.DateTime(31, 11, 2010))
        self.age.ChangeValue("")
        self.address.ChangeValue('')
        self.past_history.ChangeValue('')
