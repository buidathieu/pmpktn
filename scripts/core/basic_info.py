from initialize import *
from .custom_ctrl import *
import other_func as otf
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
        self.address = self._createAddress()
        self.past_history = self._createPastHistory()

    def _createName(self):
        w = wx.TextCtrl(self, size=name_size, style=wx.TE_READONLY)
        return w

    def _createGender(self):
        w = wx.TextCtrl(self, size=gender_size, style=wx.TE_READONLY)
        return w

    def _createBirthdate(self):
        w = wx.TextCtrl(self, size=bd_size, style=wx.TE_READONLY)
        return w

    def _createAge(self):
        w = wx.TextCtrl(self, style=wx.TE_READONLY)
        return w
    
    def _createAddress(self):
        w = wx.TextCtrl(self, style=wx.TE_READONLY)
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
        logging.debug('patient basic info updated')
        p = self.Parent.patient
        self.group_label.Label = f'Thông tin bệnh nhân (Mã BN: {p.id})'
        self.name.ChangeValue(p.name)
        self.gender.ChangeValue(gender_dict[p.gender])
        self.birthdate.ChangeValue(p.birthdate.strftime("%d/%m/%Y"))
        self.age.ChangeValue(otf.bd_to_age(p.birthdate).ljust(16))
        self.address.ChangeValue(p.address)
        self.past_history.ChangeValue(p.past_history)

    def Clear(self):
        self.group_label.Label = 'Thông tin bệnh nhân'
        self.name.ChangeValue("")
        self.gender.ChangeValue("")
        self.birthdate.ChangeValue("")
        self.age.ChangeValue("")
        self.address.ChangeValue("")
        self.past_history.ChangeValue("")
