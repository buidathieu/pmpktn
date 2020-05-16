import db_sql.db_func as dbf
from db_sql.make_db import Visit
from initialize import *
import other_func as otf

import wx


class PatientBook(wx.Notebook):

    def __init__(self, parent):
        super().__init__(parent)

        self.AddPage(page=AllPatientList(self),
                     text='DS toàn bộ bệnh nhân', select=True)
        self.AddPage(page=TodayPatientList(self),
                     text='DS đã khám hôm nay')


class AllPatientList(wx.ListCtrl):

    def __init__(self, parent):
        super().__init__(parent, style=wx.LC_REPORT | wx.LC_SINGLE_SEL)
        self.AppendColumn('Mã BN', width=ma_bn_width)
        self.AppendColumn('Bệnh nhân', width=bn_width)
        self.AppendColumn('Giới', width=gioi_width)
        self.AppendColumn('Tuổi', width=ns_width)
        self._initialize_p_list()
        self._make_p_list()
        self._reappend_to_ctrl()

    def _initialize_p_list(self):
        mv = self.Parent.Parent.Parent
        self.init_p_list = dbf.query_all_patient(sess=mv.sess).all()

    def _make_p_list(self):
        self.p_list = self.init_p_list.copy()

    def _reappend_to_ctrl(self):
        self.DeleteAllItems()
        for p in self.p_list:
            b = otf.bd_to_age(otf.pydate2wxdate(p.birthdate))
            self.Append([p.id, p.name,
                         gender_dict[p.gender], b])

    def Update(self, s=''):
        self.p_list = list(
            filter(lambda x: s.upper() in x.name, self.init_p_list))
        self._reappend_to_ctrl()

    def addNewPatient(self, p):
        self.init_p_list.append(p)
        self._make_p_list()
        self._reappend_to_ctrl()
        idx = self.ItemCount - 1
        self.Select(idx)
        self.EnsureVisible(idx)

class TodayPatientList(wx.ListCtrl):

    def __init__(self, parent):
        super().__init__(parent, style=wx.LC_REPORT | wx.LC_SINGLE_SEL)
        self.AppendColumn("STT", width=ma_bn_width)
        self.AppendColumn('Mã BN', width=ma_bn_width)
        self.AppendColumn('Bệnh nhân', width=bn_width)
        self.Refresh()

    def Refresh(self):
        self.DeleteAllItems()
        mv = self.Parent.Parent.Parent
        self.p_list = dbf.query_today_patient(
            sess=mv.sess).all()
        for i, p in enumerate(self.p_list):
            self.Append([i + 1, p.id, p.name])

    def addNewPatient(self, p):
        self.p_list.append(p)
        self.Append([self.ItemCount + 1, p.id, p.name])


class LeftPanel(wx.Panel):

    def __init__(self, parent):
        super().__init__(parent)
        self.book = PatientBook(self)
        self.search_entry = self._createSearchEntry()
        self.timer = self._createTimer()
        self.visit_listctrl = self._createVisitListCtrl()
        self.visit_list = []

        self._setBind()
        self._setSizer()

    def _setBind(self):
        for i in range(self.book.PageCount):
            self.Bind(wx.EVT_LIST_ITEM_SELECTED,
                      self.onPatientSelect, self.book.GetPage(i))
            self.Bind(wx.EVT_LIST_ITEM_DESELECTED,
                      self.onPatientDeselect, self.book.GetPage(i))
        self.Bind(wx.EVT_LIST_ITEM_SELECTED,
                  self.onVisitSelect, self.visit_listctrl)
        self.Bind(wx.EVT_LIST_ITEM_DESELECTED,
                  self.onVisitDeselect, self.visit_listctrl)

    def _setSizer(self):
        searchsizer = wx.BoxSizer(wx.HORIZONTAL)
        searchsizer.Add(wx.StaticText(
            self, label="Tìm kiếm: "), 0, wx.ALIGN_CENTER)
        searchsizer.Add(self.search_entry, 1)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.book, 10, wx.LEFT | wx.TOP, 10)
        sizer.Add(searchsizer, 0, wx.EXPAND | wx.LEFT | wx.BOTTOM, 15)
        sizer.Add(wx.StaticText(
            self, label='Lượt khám cũ:'), 0, wx.LEFT, 15)
        sizer.Add(self.visit_listctrl, 4, wx.EXPAND | wx.LEFT | wx.BOTTOM, 10)

        self.SetSizerAndFit(sizer)

    def _createSearchEntry(self):
        w = wx.TextCtrl(self)
        w.SetHint("Tên bệnh nhân")
        w.Bind(wx.EVT_TEXT, self.onText)
        return w

    def _createTimer(self):
        w = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.onSearch)
        return w

    def _createVisitListCtrl(self):
        w = wx.ListCtrl(self, style=wx.LC_REPORT | wx.LC_SINGLE_SEL)
        w.AppendColumn('Mã lượt khám', width=ma_lk_width)
        w.AppendColumn('Ngày giờ khám', width=date_width)
        w.AppendColumn('Chẩn đoán', width=date_width)

        return w

    def onText(self, e):
        self.timer.StartOnce(setting["time_between_search"])

    def onSearch(self, e):
        tab = self.book.GetPage(0)
        tab.Update(self.search_entry.Value)

    def onPatientSelect(self, e):
        self.Parent.patient = e.EventObject.p_list[e.Index]
        self.updateVisitList()
        self.Parent.right.updatePatientInfo()

    def onPatientDeselect(self, e):
        self.Parent.patient = None
        self.Parent.visit = None
        self.visit_listctrl.DeleteAllItems()
        self.visit_list = []
        self.Parent.right.clearPatientInfo()
        self.Parent.right.clearVisitInfo()

    def onVisitSelect(self, e):
        self.Parent.visit = self.visit_list[e.Index]
        self.Parent.right.updateVisitInfo()

    def onVisitDeselect(self, e):
        self.Parent.visit = None
        self.Parent.right.clearVisitInfo()

    def updateVisitList(self):
        self.visit_list = self.Parent.patient.visits.order_by(Visit.id.desc())
        self._reappend_visit_list()

    def _reappend_visit_list(self):
        self.visit_listctrl.DeleteAllItems()
        for v in self.visit_list:
            self.visit_listctrl.Append([
                v.id,
                v.exam_date.strftime('%d/%m/%Y %H:%M'),
                v.diag])

    def Refresh(self):
        self.book.ChangeSelection(0)
        tab = self.book.GetPage(0)
        tab._initialize_p_list()
        tab._make_p_list()
        tab._reappend_to_ctrl()
        self.book.GetPage(1).Refresh()
        self.search_entry.ChangeValue("")
        self.visit_listctrl.DeleteAllItems()
        self.visit_list = []
