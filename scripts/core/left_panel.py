import db_sql.db_func as dbf
from db_sql.make_db import Visit
from initialize import *
from core.__init__ import *
import other_func.other_func as otf
import wx


class PatientBook(wx.Notebook):

    def __init__(self, parent):
        super().__init__(parent)

        self.AddPage(page=PatientList(self),
                     text='Danh sách chờ khám', select=True)
        self.AddPage(page=PatientList(self, today=True),
                     text='Danh sách đã khám hôm nay')

    def Refresh(self):
        for t in [self.GetPage(0), self.GetPage(1)]:
            t.Refresh()
        self.ChangeSelection(0)


class PatientList(wx.ListCtrl):

    def __init__(self, parent, today=False):
        super().__init__(parent, style=wx.LC_REPORT | wx.LC_SINGLE_SEL)
        self.today = today
        if today:
            self.AppendColumn("STT", width=ma_bn_width)
        else:
            self.AppendColumn('Mã BN', width=ma_bn_width)
        self.AppendColumn('Bệnh nhân', width=bn_width)
        self.AppendColumn('Giới', width=gioi_width)
        self.AppendColumn('Tuổi', width=ns_width)

        self.Renew()

        self.Bind(wx.EVT_LIST_ITEM_SELECTED, self.onSelect)
        self.Bind(wx.EVT_LIST_ITEM_DESELECTED, self.onDeselect)

    def initialize_p_list(self):
        self.init_p_list = dbf.get_patient_list_by_name(
            s='',
            today=self.today,
            sess=self.Parent.Parent.sess).all()

    def _makePatientList(self):
        self.DeleteAllItems()
        if self.today:
            for i, p in enumerate(self.patient_list):
                b = otf.bd_to_age(otf.pydate2wxdate(p.birthdate))
                self.Append([i + 1, p.name,
                             gender_dict[p.gender], b])
        else:
            for p in self.patient_list:
                b = otf.bd_to_age(otf.pydate2wxdate(p.birthdate))
                self.Append([p.id, p.name,
                             gender_dict[p.gender], b])

    def onSelect(self, e):
        mv = self.Parent.Parent
        mv.patient = self.patient_list[e.Index]

    def onDeselect(self, e):
        mv = self.Parent.Parent
        mv.patient = None
        mv.visit = None

    def Update(self, s=''):
        self.patient_list = list(
            filter(lambda x: s.upper() in x.name, self.init_p_list))
        self._makePatientList()

    def Refresh(self):
        self.patient_list = self.init_p_list.copy()
        self._makePatientList()

    def Renew(self):
        self.initialize_p_list()
        self.Refresh()



class SearchCtrl(wx.Panel):

    def __init__(self, parent):
        super().__init__(parent=parent)
        self.search_entry = wx.TextCtrl(self)
        self.search_entry.SetHint("Tên bệnh nhân")
        self.search_entry.Bind(wx.EVT_TEXT, self.onText)
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer.Add(wx.StaticText(self, label="Tìm kiếm: "), 0, wx.ALIGN_CENTER)
        sizer.Add(self.search_entry, 1)
        self.SetSizerAndFit(sizer)
        self.timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.onSearch)

    def onText(self, e):
        self.timer.StartOnce(800)

    def onSearch(self, e):
        tab = self.Parent.book.GetPage(self.Parent.book.Selection)
        tab.Update(self.search_entry.Value)

    def Clear(self):
        self.search_entry.ChangeValue("")


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
        self._makeVisitList()

    def _makeVisitList(self):
        self.Clear()
        for v in self.visit_list:
            self.Append([v.id,
                         v.exam_date.strftime('%d/%m/%Y %H:%M'),
                         v.diag])

    def Clear(self):
        self.DeleteAllItems()
