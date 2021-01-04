import database.db_func as dbf
from initialize import *
import other_func as otf

import wx


class PatientBook(wx.Notebook):

    def __init__(self, parent):
        super().__init__(parent)
        self.mv = parent
        # self.AddPage(page=QueuingPatientList(self),
        #              text='Danh sách chờ khám', select=True)
        self.AddPage(page=AllPatientList(self),
                     text='Danh sách toàn bộ bệnh nhân', select=True)
        self.AddPage(page=TodayPatientList(self),
                     text='Danh sách đã khám hôm nay')
        self.Bind(wx.EVT_NOTEBOOK_PAGE_CHANGED, self.onChangePage)

    def refresh(self):
        self.ChangeSelection(0)
        self.GetPage(0).refresh()

    def onChangePage(self, e):
        self.mv.patient = None
        self.GetPage(e.GetSelection()).refresh()
        e.Skip()

    def start(self):
        self.GetPage(0).refresh()


class BasePatientList(wx.ListCtrl):

    def __init__(self, parent):
        super().__init__(parent, style=wx.LC_REPORT | wx.LC_SINGLE_SEL)
        self.mv = parent.mv
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
            self.Append([p.id,
                         p.name,
                         p.gender,
                         b])

    def onSelect(self, e):
        self.mv.patient = self.p_list[e.Index]

    def onDeselect(self, e):
        self.mv.patient = None

    def refresh(self):
        self._make_p_list()
        self._append()

    def append_new_patient(self, new_patient):
        b = otf.bd_to_age(new_patient.birthdate)
        self.Append([
            new_patient.id,
            new_patient.name,
            new_patient.gender,
            b])
        self.p_list.append(new_patient)

    def renew_patient_info(self, patient, idx):
        self.SetItem(idx, 0, str(patient.id))
        self.SetItem(idx, 1, patient.name)
        self.SetItem(idx, 2, patient.gender)
        self.SetItem(idx, 3, otf.bd_to_age(patient.birthdate))
        self.Select(idx, on=0)
        self.Select(idx)

class TodayPatientList(BasePatientList):

    def __init__(self, parent):
        super().__init__(parent)

    def _make_p_list(self):
        self.p_list = dbf.get_today_seen_patient_list(
            sess=self.mv.sess).all()


class AllPatientList(BasePatientList):

    def __init__(self, parent):
        super().__init__(parent)

    def _make_p_list(self):
        self.p_list = dbf.get_all_patient_list(
            sess=self.mv.sess).all()
