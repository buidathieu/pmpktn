from initialize import *
import other_func as otf

import math
from fractions import Fraction as fr

import wx


class BaseCalcQuantityWidget(wx.TextCtrl):

    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.mv = parent.mv
        self.Bind(wx.EVT_TEXT, self.calc_quantity)

    def calc_quantity(self, e):
        pg = self.mv.order_book.GetPage(0)
        day = pg.days.Value
        dosage = pg.dosage_per.Value
        time = pg.times.Value
        drug = pg.drug_picker.drugWH
        try:
            assert day != 0
            assert dosage != ''
            assert time != ''
            assert drug is not None
            # numberize
            day = int(day)
            time = int(time)
            if "/" in dosage:
                dosage = fr(dosage)
            elif "." in dosage:
                dosage = float(dosage)
            else:
                dosage = int(dosage)
            # cal qty
            if drug.sale_unit in ['chai', 'lọ', 'týp']:
                qty = '1'
            else:
                qty = math.ceil(dosage * time * day)

            pg.quantity.ChangeValue(str(qty))
            pg.usage.ChangeValue(
                "Ngày {} {} lần, lần {} {}".format(
                    drug.usage,
                    time,
                    dosage,
                    drug.usage_unit))
            pg.quantity.SetInsertionPointEnd()
        except AssertionError:
            pass


class Days(BaseCalcQuantityWidget):

    def __init__(self, parent):
        default_days = str(user_setting['so_ngay_toa_ve_mac_dinh'])
        super().__init__(parent, size=days_size, value=default_days)
        self.Bind(wx.EVT_CHAR, otf.only_nums)


class Times(BaseCalcQuantityWidget):

    def __init__(self, parent):
        super().__init__(parent, size=dose_size)
        self.SetHint('lần')
        self.Bind(wx.EVT_CHAR, otf.only_nums)

class DosagePer(BaseCalcQuantityWidget):

    def __init__(self, parent):
        super().__init__(parent, size=dose_size)
        self.SetHint('liều')
        self.Bind(
            wx.EVT_CHAR,
            lambda e: otf.only_nums(e, decimal=True, slash=True))


class Quantity(wx.TextCtrl):

    def __init__(self, parent, size=dose_size, style=wx.TE_PROCESS_ENTER):
        super().__init__(parent)
        self.mv = parent.Parent.Parent
        self.SetHint('Enter')
        self.Bind(wx.EVT_CHAR, self.on_txt_qty)

    def on_txt_qty(self, e):
        x = e.KeyCode
        if x in (wx.WXK_RETURN, wx.WXK_NUMPAD_ENTER):
            self.mv.order_book.GetPage(0).onSaveDrug()
        else:
            otf.only_nums(e, tab=False)
