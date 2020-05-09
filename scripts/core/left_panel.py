import db_sql.db_func as dbf
from db_sql.make_db import Visit
from initialize import *
from core.__init__ import *
import other_func.other_func as otf
import wx
import logging


class PatientBook(wx.Notebook):

    def __init__(self, parent):
        super().__init__(parent)

        self.AddPage(page=QueuingPatientList(self),
                     text='Danh sách chờ khám', select=True)
        self.AddPage(page=SeenPatientList(self),
                     text='Danh sách đã khám hôm nay')
        self.Bind(wx.EVT_NOTEBOOK_PAGE_CHANGED, self.onChangePage)

    def Refresh(self):
        self.ChangeSelection(0)
        self.GetPage(0).Refresh()

    def onChangePage(self, e):
        self.GetPage(e.GetSelection()).Refresh()
        self.Parent.patient = None
        self.Parent.visit = None
        self.Parent.visit_list.Clear()
        logging.debug(f"Change to page {e.GetSelection()}")
        e.Skip()


class QueuingPatientList(wx.ListCtrl):

    def __init__(self, parent):
        super().__init__(parent, style=wx.LC_REPORT | wx.LC_SINGLE_SEL)
        self.AppendColumn('Mã BN', width=ma_bn_width)
        self.AppendColumn('Bệnh nhân', width=bn_width)
        self.AppendColumn('Giới', width=gioi_width)
        self.AppendColumn('Tuổi', width=ns_width)

        self.timer = self.RefreshQueueTimer()

        self.Bind(wx.EVT_LIST_ITEM_SELECTED, self.onSelect)
        self.Bind(wx.EVT_LIST_ITEM_DESELECTED, self.onDeselect)

    def _make_p_list(self):
        self.p_list = dbf.get_queuing_patient_list(
            sess=self.Parent.Parent.sess).all()

    def _append(self):
        self.DeleteAllItems()
        for p in self.p_list:
            b = otf.bd_to_age(otf.pydate2wxdate(p.birthdate))
            self.Append([p.id, p.name,
                         gender_dict[p.gender], b])

    def onSelect(self, e):
        mv = self.Parent.Parent
        mv.patient = self.p_list[e.Index]

    def onDeselect(self, e):
        mv = self.Parent.Parent
        mv.patient = None
        mv.visit = None

    def Refresh(self):
        logging.debug('waiting queue rebuilt')
        self._make_p_list()
        self._append()

    def RefreshQueueTimer(self):
        self.Refresh()
        return wx.CallLater(1000 * 60 * 5, self.RefreshQueueTimer)


class SeenPatientList(wx.ListCtrl):

    def __init__(self, parent):
        super().__init__(parent, style=wx.LC_REPORT | wx.LC_SINGLE_SEL)
        self.AppendColumn('Mã BN', width=ma_bn_width)
        self.AppendColumn('Bệnh nhân', width=bn_width)
        self.AppendColumn('Giới', width=gioi_width)
        self.AppendColumn('Tuổi', width=ns_width)

        self.Bind(wx.EVT_LIST_ITEM_SELECTED, self.onSelect)
        self.Bind(wx.EVT_LIST_ITEM_DESELECTED, self.onDeselect)

    def _make_p_list(self):
        self.p_list = dbf.get_seen_patient_list(
            sess=self.Parent.Parent.sess).all()

    def _append(self):
        self.DeleteAllItems()
        for p in self.p_list:
            b = otf.bd_to_age(otf.pydate2wxdate(p.birthdate))
            self.Append([p.id, p.name,
                         gender_dict[p.gender], b])

    def onSelect(self, e):
        mv = self.Parent.Parent
        mv.patient = self.p_list[e.Index]

    def onDeselect(self, e):
        mv = self.Parent.Parent
        mv.patient = None
        mv.visit = None

    def Refresh(self):
        logging.debug('seen patient list rebuilt')
        self._make_p_list()
        self._append()


class VisitList(wx.ListCtrl):

    def __init__(self, parent):
        super().__init__(parent, style=wx.LC_REPORT | wx.LC_SINGLE_SEL)
        self.visit_list = []
        self.AppendColumn('Mã lượt khám', width=ma_lk_width)
        self.AppendColumn('Ngày giờ khám', width=date_width)
        self.AppendColumn('Chẩn đoán', width=date_width)
        self.Bind(wx.EVT_LIST_ITEM_SELECTED, self.onVisitSelect)
        self.Bind(wx.EVT_LIST_ITEM_DESELECTED, self.onVisitDeselect)

    def onVisitSelect(self, e):
        self.Parent.visit = self.visit_list[e.Index]

    def onVisitDeselect(self, e):
        self.Parent.visit = None

    def Update(self):
        self.visit_list = self.Parent.patient.visits.order_by(Visit.id.desc())
        self._append()

    def _append(self):
        logging.debug('visit list rebuilt')
        self.Clear()
        for v in self.visit_list:
            self.Append([v.id,
                         v.exam_date.strftime('%d/%m/%Y %H:%M'),
                         v.diag])

    def Clear(self):
        self.DeleteAllItems()
