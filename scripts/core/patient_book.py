import db_sql.db_func as dbf
from initialize import *
import other_func as otf

import wx
import logging


class PatientBook(wx.Notebook):

    def __init__(self, parent):
        super().__init__(parent)

        self.AddPage(page=QueuingPatientList(self),
                     text='Danh sách chờ khám', select=True)
        self.AddPage(page=TodayPatientList(self),
                     text='Danh sách đã khám hôm nay')
        self.Bind(wx.EVT_NOTEBOOK_PAGE_CHANGED, self.onChangePage)

    def Refresh(self):
        self.ChangeSelection(0)
        self.GetPage(0).Refresh()

    def onChangePage(self, e):
        self.Parent.patient = None
        self.GetPage(e.GetSelection()).Refresh()
        logging.debug(f"Change to page {e.GetSelection()}")
        e.Skip()


class BasePatientList(wx.ListCtrl):

    def __init__(self, parent):
        super().__init__(parent, style=wx.LC_REPORT | wx.LC_SINGLE_SEL)
        self.AppendColumn('Mã BN', width=ma_bn_width)
        self.AppendColumn('Bệnh nhân', width=bn_width)
        self.AppendColumn('Giới', width=gender_width)
        self.AppendColumn('Tuổi', width=ns_width)
        self.Bind(wx.EVT_LIST_ITEM_SELECTED, self.onSelect)
        self.Bind(wx.EVT_LIST_ITEM_DESELECTED, self.onDeselect)

    def _make_p_list(self):
        self.p_list = None

    def _append(self):
        self.DeleteAllItems()
        for p in self.p_list:
            b = otf.bd_to_age(p.birthdate)
            self.Append([p.id, p.name,
                         gender_dict[p.gender], b])

    def onSelect(self, e):
        mv = self.Parent.Parent
        mv.patient = self.p_list[e.Index]

    def onDeselect(self, e):
        mv = self.Parent.Parent
        mv.patient = None

    def Refresh(self):
        logging.debug(f'{self.__class__.__name__} make query and rebuilt')
        self._make_p_list()
        self._append()


class QueuingPatientList(BasePatientList):

    def __init__(self, parent):
        super().__init__(parent)
        self.vq = None
        self.timer = self.RefreshQueueTimer()

    def _make_p_list(self):
        self.vq_list = dbf.get_visitqueue(
            sess=self.Parent.Parent.sess).all()
        self.p_list = [vq.patient for vq in self.vq_list]

    def RefreshQueueTimer(self):
        self.Refresh()
        return wx.CallLater(
            setting["time_between_rebuild_visitqueue"],
            self.RefreshQueueTimer)

    def onSelect(self, e):
        self.vq = self.vq_list[e.Index]
        super().onSelect(e)

    def onDeselect(self, e):
        self.vq = None
        super().onDeselect(e)


class TodayPatientList(BasePatientList):

    def __init__(self, parent):
        super().__init__(parent)

    def _make_p_list(self):
        self.p_list = dbf.get_today_seen_patient_list(
            sess=self.Parent.Parent.sess).all()
