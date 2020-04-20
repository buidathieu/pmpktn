import db_sql.db_func as dbf

import wx


class CheckStaffDialog(wx.Dialog):

    def __init__(self, parent, sess):
        super().__init__(parent, title="Đăng nhập hôm nay")
        self.sess = sess
        self.staff_list = dbf.query_staff_list(self.sess).all()
        self.staff_ctrl = wx.Choice(
            self, choices=[i.name for i in self.staff_list])

        sizer = wx.BoxSizer(wx.VERTICAL)

        btns = self.CreateStdDialogButtonSizer(wx.OK | wx.CANCEL)

        sizer.Add(self.staff_ctrl, 0, wx.EXPAND | wx.ALL, 10)
        sizer.Add(btns, 0, wx.ALL ^ wx.TOP, 10)
        self.SetSizerAndFit(sizer)

    def save_staff_workday(self):
        idx = self.staff_ctrl.Selection
        staff = self.staff_list[idx]
        dbf.save_staff_workday(staff, sess=self.sess)
