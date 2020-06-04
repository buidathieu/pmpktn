from db_sql.make_db import Visit
from initialize import *

import wx
import logging


class VisitList(wx.ListCtrl):

    def __init__(self, parent):
        super().__init__(parent, style=wx.LC_REPORT | wx.LC_SINGLE_SEL)
        self.visit_list = []
        self.AppendColumn('Mã lượt khám', width=ma_lk_width)
        self.AppendColumn('Ngày giờ khám', width=date_width)
        self.AppendColumn('Chẩn đoán', width=date_width)
        self.Bind(wx.EVT_LIST_ITEM_SELECTED, self.onSelect)
        self.Bind(wx.EVT_LIST_ITEM_DESELECTED, self.onDeselect)

    def onSelect(self, e):
        self.Parent.visit = self.visit_list[e.Index]

    def onDeselect(self, e):
        self.Parent.visit = None

    def buildVisitList(self, p):
        self.visit_list = p.visits.order_by(Visit.id.asc())
        logging.debug('visit list rebuilt')
        self.Clear()
        for v in self.visit_list:
            self.Append([v.id,
                         v.exam_date.strftime('%d/%m/%Y %H:%M'),
                         v.diag])

    def Clear(self):
        self.DeleteAllItems()
