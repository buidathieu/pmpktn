import db_sql.db_func as dbf
from db_sql.__init__ import Session
import wx
import logging


class LogInDialog(wx.Dialog):

    def __init__(self, parent):
        super().__init__(parent, title="Đăng nhập")
        self.sess = Session()
        self.Centre()
        self.staff_list = dbf.query_staff_list(self.sess).all()
        self.staff_ctrl = wx.Choice(
            self, choices=[i.name for i in self.staff_list])

        sizer = wx.BoxSizer(wx.VERTICAL)

        btns = self.CreateStdDialogButtonSizer(wx.OK)

        sizer.Add(self.staff_ctrl, 0, wx.EXPAND | wx.ALL, 10)
        sizer.Add(btns, 0, wx.ALL ^ wx.TOP, 10)
        self.SetSizerAndFit(sizer)

        self.Bind(wx.EVT_CLOSE, self.onClose)
        logging.debug('LoginDialog initialized, session opened')

    def save_staff_workday(self):
        idx = self.staff_ctrl.Selection
        if idx >= 0:
            staff = self.staff_list[idx]
            logging.debug(
                f'LoginDialog: save_staff_workday: selection={idx}, name={staff.name}, job={staff.job}')
            dbf.save_staff_workday(staff, sess=self.sess)

    def get_staff_job(self):
        idx = self.staff_ctrl.Selection
        if idx >= 0:
            return self.staff_list[idx].job

    def onClose(self, e):
        self.EndModal(wx.ID_CLOSE)

    def Destroy(self):
        logging.debug('LoginDialog destroyed, session closed')
        self.sess.commit()
        self.sess.close()
        super().Destroy()
