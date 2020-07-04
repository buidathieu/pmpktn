from initialize import *
from db_sql.db_func import query_therapy_list
from .core_func import onSaveTherapy
import os
import wx


class TherapyPopup(wx.ComboPopup):

    def __init__(self, parent):
        super().__init__()
        self.lc = None
        mv = parent.Parent.Parent.Parent
        self.init_t_l = query_therapy_list(mv.sess).all()
        self.t_l = []

    def Create(self, parent):
        self.lc = wx.ListCtrl(
            parent,
            style=wx.LC_REPORT | wx.LC_SINGLE_SEL | wx.SIMPLE_BORDER)
        self.lc.AppendColumn('Thủ thuật', width=200)
        self.lc.AppendColumn('Đơn giá')
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
        self.t_l = list(filter(lambda x: s.casefold()
                               in x.name.casefold(), self.init_t_l))
        for item in self.t_l:
            self.lc.Append(
                [item.name, item.sale_price])

    def OnMotion(self, e):
        item, flags = self.lc.HitTest(e.GetPosition())
        if item >= 0:
            self.lc.Select(item)
            self.curitem = item

    def OnLeftDown(self, e):
        try:
            self.value = self.curitem
            self.ComboCtrl.therapy = self.t_l[self.value]
            self.Dismiss()
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
        self.Dismiss()

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


class TherapyPicker(wx.ComboCtrl):

    def __init__(self, parent):
        super().__init__(parent, style=wx.TE_PROCESS_ENTER)
        self.therapy_popup = TherapyPopup(self)
        self.SetPopupControl(self.therapy_popup)
        self.Bind(wx.EVT_KEY_DOWN, self.onKeyPress)
        self.Bind(wx.EVT_TEXT, self.onTextChange)
        self.SetHint("Nhấn Enter để search thủ thuật")
        self.therapy = None
        self.EnablePopupAnimation(enable=False)

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
            elif e.GetKeyCode()==wx.WXK_RETURN and not self.IsPopupShown():
                onSaveTherapy(self.Parent)
                self.Clear()
                self.ChangeValue("")
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
        self.therapy = None
