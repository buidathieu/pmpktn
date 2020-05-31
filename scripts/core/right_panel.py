from initialize import *
import other_func as otf
from .order_book import OrderBook

import wx


def create_right_panel_widgets(mv):
    def _createNewVisitbtn(mv):
        btn = wx.Button(mv, label='Lượt khám mới (F2)')
        btn.SetBitmap(wx.Bitmap(new_visit_bm))
        return btn

    def _createSaveVisitbtn(mv):
        btn = wx.Button(mv, label='Lưu lượt khám (F3)')
        btn.SetBitmap(wx.Bitmap(save_visit_bm))
        return btn
    
    def _createTotalCost(mv):

        def on_bill(e):
            val = int("".join(w.Value.split(".")))
            w.ChangeValue(otf.bill_int_to_str(val))
            w.SetInsertionPointEnd()

        def _kill_focus(e):
            if w.Value == '':
                w.ChangeValue('0')

        w = wx.TextCtrl(mv,
                        value=otf.bill_int_to_str(setting['cong_kham_benh']))
        w.Bind(wx.EVT_CHAR, otf.only_nums)
        w.Bind(wx.EVT_TEXT, on_bill)
        w.Bind(wx.EVT_KILL_FOCUS, _kill_focus)
        return w
    mv.label_1 = wx.StaticText(mv, label='Thông tin bệnh nhân')
    mv.name = wx.TextCtrl(mv, size=name_size, style=wx.TE_READONLY)
    mv.gender = wx.TextCtrl(mv, size=gender_size, style=wx.TE_READONLY)
    mv.birthdate = wx.TextCtrl(mv, size=bd_size, style=wx.TE_READONLY)
    mv.age = wx.TextCtrl(mv, style=wx.TE_READONLY)
    mv.address = wx.TextCtrl(mv, style=wx.TE_READONLY)
    mv.past_history = wx.TextCtrl(mv, style=wx.TE_MULTILINE, size=note_size)
    mv.label_2 = wx.StaticText(mv, label='Thông tin lượt khám')
    mv.label_dt = wx.StaticText(mv)
    mv.note = wx.TextCtrl(mv, size=note_size, style=wx.TE_MULTILINE)
    mv.diag = wx.TextCtrl(mv)
    mv.order_book = OrderBook(mv)
    # mv.new_visit_btn = _createNewVisitbtn(mv)
    mv.save_visit_btn = _createSaveVisitbtn(mv)
    mv.total_cost = _createTotalCost(mv)
    
    
   
def create_right_panel_sizer(mv):    
    sizer = wx.BoxSizer(wx.VERTICAL)
    label_1_row = wx.BoxSizer(wx.HORIZONTAL)
    name_row = wx.BoxSizer(wx.HORIZONTAL)
    addr_row = wx.BoxSizer(wx.HORIZONTAL)
    label_2_row = wx.BoxSizer(wx.HORIZONTAL)
    datetime_row = wx.BoxSizer(wx.HORIZONTAL)
    diag_row = wx.BoxSizer(wx.HORIZONTAL)
    btn_row = wx.BoxSizer(wx.HORIZONTAL)

    label_1_row.Add(mv.label_1, 0)
    label_1_row.Add(wx.StaticLine(mv), 1, wx.ALIGN_CENTER)
    name_row.Add(wx.StaticText(mv, label='Họ tên:'), 0, wx.ALIGN_CENTER)
    name_row.Add(mv.name, 0, wx.ALIGN_CENTER | wx.RIGHT, 5)
    name_row.Add(mv.gender, 0, wx.ALIGN_CENTER | wx.RIGHT, 5)
    name_row.Add(wx.StaticText(mv, label='Ngày sinh:'), 0, wx.ALIGN_CENTER)
    name_row.Add(mv.birthdate, 0, wx.ALIGN_CENTER | wx.RIGHT, 5)
    name_row.Add(wx.StaticText(mv, label='Tuổi:'), 0, wx.ALIGN_CENTER)
    name_row.Add(mv.age, 1, wx.ALIGN_CENTER)
    addr_row.Add(wx.StaticText(mv, label='Địa chỉ:'), 0, wx.ALIGN_CENTER)
    addr_row.Add(mv.address, 1, wx.EXPAND)
    label_2_row.Add(mv.label_2)
    label_2_row.Add(wx.StaticLine(mv), 1, wx.ALIGN_CENTER)
    datetime_row.Add(wx.StaticText(
        mv,
        label='Bệnh sử, triệu chứng, ghi chú,... (theo từng lượt khám):'))
    datetime_row.Add(mv.label_dt, 1, wx.RIGHT, 10)
    diag_row.Add(wx.StaticText(mv, label='Chẩn đoán:'),
                 0, wx.ALIGN_CENTER | wx.TOP, 3)
    diag_row.Add(mv.diag, 1)
    # btn_row.Add(mv.new_visit_btn, 0, wx.CENTRE)
    btn_row.Add(mv.save_visit_btn, 0, wx.CENTRE)
    btn_row.AddStretchSpacer()
    btn_row.Add(wx.StaticText(mv, label='Tổng tiền:'), 0, wx.CENTRE)
    btn_row.Add(mv.total_cost, 0, wx.CENTRE)
    
    sizer.Add(label_1_row, 0, wx.EXPAND)
    sizer.Add(name_row, 0, wx.EXPAND)
    sizer.Add(addr_row, 0, wx.EXPAND | wx.TOP, 3)
    sizer.Add(wx.StaticText(mv, label='Bệnh nền, dị ứng:'), 0, wx.TOP, 3)
    sizer.Add(mv.past_history, 0, wx.EXPAND)
    sizer.Add(label_2_row, 0, wx.EXPAND)
    sizer.Add(datetime_row, 0, wx.EXPAND)
    sizer.Add(mv.note, 0, wx.EXPAND)
    sizer.Add(diag_row, 0, wx.EXPAND | wx.TOP, 3)
    sizer.Add(mv.order_book, 0, wx.EXPAND | wx.TOP, 3)
    sizer.Add(btn_row, 0, wx.EXPAND | wx.TOP, 3)
    
    return sizer