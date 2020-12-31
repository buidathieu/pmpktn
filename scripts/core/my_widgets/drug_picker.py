from initialize import *
from db_sql.db_func import query_linedrug_list
import os
import wx


class DrugPopup(wx.ComboPopup):

    def __init__(self, parent):
        super().__init__()
        self.lc = None
        mv = parent.Parent.Parent.Parent
        self.init_d_l = query_linedrug_list(mv.sess).all()
        self.d_l = []

    def Create(self, parent):
        self.lc = wx.ListCtrl(
            parent,
            style=wx.LC_REPORT | wx.LC_SINGLE_SEL | wx.SIMPLE_BORDER)
        self.lc.AppendColumn('Thuốc', width=200)
        self.lc.AppendColumn('Thành phần', width=150)
        self.lc.AppendColumn('Số lượng')
        self.lc.AppendColumn('Đơn giá')
        self.lc.AppendColumn('Cách dùng', width=100)
        self.lc.AppendColumn('Nhà SX', width=80)
        self.lc.Bind(wx.EVT_MOTION, self.OnMotion)
        self.lc.Bind(wx.EVT_LEFT_DOWN, self.OnLeftDown)
        self.lc.Bind(wx.EVT_KEY_DOWN, self.onKeyPress)
        self.Update()
        return True

    def Init(self):
        self.value = -1
        self.curitem = -1

    def GetControl(self):
        return self.lc

    def SetStringValue(self, val):
        idx = self.lc.FindItem(-1, val)
        if idx != wx.NOT_FOUND:
            self.lc.Select(idx)

    def GetStringValue(self):
        if self.value >= 0:
            return self.lc.GetItemText(self.value, col=0)
        return ""

    def GetAdjustedSize(self, minWidth, prefHeight, maxHeight):
        return super().GetAdjustedSize(*popup_size)

    def Update(self, s=''):
        self.lc.DeleteAllItems()
        self.d_l = list(filter(
            lambda x: s.casefold() in x.name.casefold() or s.casefold() in x.element.casefold(),
            self.init_d_l))
        for item in self.d_l:
            self.lc.Append(
                [item.name, item.element, item.quantity, item.sale_price, item.usage, item.manufacturer])
        for index, item in enumerate(self.d_l):
            if item.quantity <10:
                self.lc.SetItemTextColour(index, wx.Colour(252, 3, 57,255))
                

    def OnMotion(self, e):
        item, flags = self.lc.HitTest(e.GetPosition())
        if item >= 0:
            self.lc.Select(item)
            self.curitem = item

    def OnLeftDown(self, e):
        try:
            self.value = self.curitem
            self.ComboCtrl.drugWH = self.d_l[self.value]
            self.Dismiss()
            self.ComboCtrl.SelectAll()
            self.ComboCtrl.SetInsertionPointEnd()
        except IndexError:
            self.Dismiss()

    def OnPopup(self):
        self.Init()
        self.Update(self.ComboCtrl.Value)
        if self.lc.ItemCount > 0:
            if self.curitem < (self.lc.ItemCount - 1):
                self.curitem += 1
            self.lc.Select(self.curitem)
            self.lc.EnsureVisible(self.curitem)

    def KeyDown(self):
        if self.lc.ItemCount > 0:
            if self.curitem < (self.lc.ItemCount - 1):
                self.curitem += 1
            self.lc.Select(self.curitem)
            self.lc.EnsureVisible(self.curitem)

    def KeyUp(self):
        if self.lc.ItemCount > 0:
            if self.curitem > 0:
                self.curitem -= 1
            self.lc.Select(self.curitem)
            self.lc.EnsureVisible(self.curitem)
        else:
            self.KeyESC()

    def KeyESC(self):
        a = self.ComboCtrl.Value
        self.Dismiss()
        self.ComboCtrl.ChangeValue(a)
        self.ComboCtrl.SetInsertionPointEnd()

    def KeyReturn(self):
        self.OnLeftDown(None)

    def onKeyPress(self, e):
        c = e.GetKeyCode()
        if c == wx.WXK_DOWN:
            self.KeyDown()
        elif c == wx.WXK_UP:
            self.KeyUp()
        elif c == wx.WXK_ESCAPE:
            self.KeyESC()
        elif c == wx.WXK_RETURN:
            self.KeyReturn()


class drug_picker(wx.ComboCtrl):

    def __init__(self, parent):
        super().__init__(parent, size=drugctrl_size, style=wx.TE_PROCESS_ENTER)
        self.drug_popup = DrugPopup(self)
        self.SetPopupControl(self.drug_popup)
        self.Bind(wx.EVT_KEY_DOWN, self.onKeyPress)
        self.Bind(wx.EVT_TEXT, self.onTextChange)
        self.SetHint("Nhấn Enter để search thuốc")
        self._drugWH = None
        self.EnablePopupAnimation(enable=False)

    @property
    def drugWH(self):
        return self._drugWH

    @drugWH.setter
    def drugWH(self, dwh):
        self._drugWH = dwh
        pg = self.Parent
        if dwh:
            pg.usage_unit.Label = dwh.usage_unit
            pg.sale_unit.Label = dwh.sale_unit
        else:
            self.ChangeValue('')
            pg.dosage_per.ChangeValue('')
            pg.usage_unit.Label = '{Đơn vị}'
            pg.times.ChangeValue("")
            pg.quantity.ChangeValue("")
            pg.sale_unit.Label = '{Đơn vị}'
            pg.usage.ChangeValue("")

    def onKeyPress(self, e):
        if os.name == "posix":
            if e.GetKeyCode() in [wx.WXK_RETURN, wx.WXK_DOWN]:
                if not self.IsPopupShown():
                    self.Popup()
            else:
                e.Skip()
        else:
            if e.GetKeyCode() not in [wx.WXK_RETURN,
                                      wx.WXK_UP,
                                      wx.WXK_DOWN,
                                      wx.WXK_ESCAPE]:
                if self.IsPopupShown():
                    a = self.Value
                    self.Dismiss()
                    self.ChangeValue(a)
                    self.SetInsertionPointEnd()
            e.Skip()

    def onTextChange(self, e):
        if os.name == "nt":
            if e.String == "":
                self.Clear()
            elif len(e.String) >= 1:
                if not self.IsPopupShown():
                    self.Popup()
                self.SetInsertionPointEnd()
        if os.name == "posix":
            if e.String == "":
                self.Clear()

    def Clear(self):
        self.drugWH = None
