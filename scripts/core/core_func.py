from initialize import *
import db_sql.db_func as dbf
import other_func as otf
from sample_prescription import SamplePrescriptionDialog

from fractions import Fraction as fr
import math
import logging

import wx


def onPatientSelect(mv, p):
    mv.visit_list.buildVisitList(p)
    # info
    mv.label_1.Label = f'Thông tin bệnh nhân (Mã BN: {p.id})'
    mv.name.ChangeValue(p.name)
    mv.gender.ChangeValue(gender_dict[p.gender])
    mv.birthdate.ChangeValue(p.birthdate.strftime("%d/%m/%Y"))
    mv.age.ChangeValue(otf.bd_to_age(p.birthdate).ljust(16))
    mv.address.ChangeValue(p.address)
    mv.past_history.ChangeValue(p.past_history)
    
def onPatientDeselect(mv, p=None):
    mv.visit_list.Clear()
    # info
    mv.label_1.Label = 'Thông tin bệnh nhân'
    mv.name.ChangeValue("")
    mv.gender.ChangeValue("")
    mv.birthdate.ChangeValue("")
    mv.age.ChangeValue("")
    mv.address.ChangeValue("")
    mv.past_history.ChangeValue("")
    
    
def onVisitSelect(mv, v):

    def _dt_to_label(p_dt):
        return ' ' * 20 + 'Giờ khám: {}:{} ngày {} tháng {} năm {}'.\
            format(str(p_dt.hour).rjust(2, '0'),
                   str(p_dt.minute).rjust(2, '0'),
                   p_dt.day,
                   p_dt.month,
                   p_dt.year)

    mv.label_2.Label =f'Thông tin lượt khám (Mã lượt khám: {v.id})'
    mv.label_dt.Label = _dt_to_label(v.exam_date)
    mv.note.ChangeValue(v.note)
    mv.diag.ChangeValue(v.diag)
    pg = mv.order_book.GetPage(0)
    pg.weight.ChangeValue(str(v.weight))
    pg.days.ChangeValue(str(v.days))
    pg.drugpicker.Clear()
    pg.d_list.Populate(v.linedrugs)
    pg.followup.ChangeValue(v.followup)
    mv.total_cost.ChangeValue(otf.bill_int_to_str(v.bill))
    
    
def onVisitDeselect(mv, v=None):
    mv.label_2.Label = 'Thông tin lượt khám'
    mv.label_dt.Label = ""
    mv.note.ChangeValue("")
    mv.diag.ChangeValue("")
    pg = mv.order_book.GetPage(0)
    pg.weight.ChangeValue('0')
    pg.days.ChangeValue('2')
    pg.drugpicker.Clear()
    pg.d_list.Clear()
    pg.followup.Selection = 0
    mv.total_cost.ChangeValue(otf.bill_int_to_str(setting['cong_kham_benh']))


def onSaveVisit(mv):
    assert mv.patient is not None
    assert mv.name.Value != ""
    assert mv.diag.Value != ""
    
    pg = mv.order_book.GetPage(0)

    kwargs = {
        'p': mv.patient,
        'v': mv.visit,
        'vq': mv.book.GetPage(0).vq,
        'past_history': mv.past_history.Value,
        'note': mv.note.Value,
        'diag': mv.diag.Value,
        'weight': float(pg.weight.Value),
        'days': int(pg.days.Value),
        'followup': pg.followup.Value,
        'bill': otf.bill_str_to_int(
            mv.total_cost.Value),
        'linedrugs': pg.d_list.build_linedrugs()
    }
    if mv.visit:
        ans = wx.MessageBox("Cập nhật lượt khám?", "Lưu", style=wx.YES_NO)
        if ans == wx.YES:
            logging.debug(f"update selected visit: {kwargs}")
            dbf.save_old_visit(**kwargs, sess=mv.sess)
            wx.MessageBox("Đã cập nhật")
    else:
        ans = wx.MessageBox("Lưu lượt khám mới?", "Lưu", style=wx.YES_NO)
        if ans == wx.YES:
            logging.debug(f"save new visit: {kwargs}")
            dbf.save_new_visit(**kwargs, sess=mv.sess)
            wx.MessageBox("Đã lưu")
    mv.Refresh()
    
    
def getWeight(mv):
    logging.debug('get latest weight')
    return str(mv.patient.visits[-1].weight)
    

def calc_quantity(pg):
    logging.debug('recalculate quantity')
    day = pg.days.Value
    dosage = pg.dosage_per.Value
    time = pg.times.Value
    drug = pg.drugpicker.drugWH
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
        if drug.sale_unit == 'chai':
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
    except AssertionError:
        pass


def onSaveDrug(pg):
    kwargs = {
        "d": pg.drugpicker.drugWH,
        "times": pg.times.Value,
        "dosage_per": pg.dosage_per.Value,
        "quantity": pg.quantity.Value,
        "usage": pg.usage.Value
    }
    assert kwargs["d"] is not None
    assert int(kwargs["times"])
    assert kwargs['dosage_per'] != ""
    assert int(kwargs['quantity'])

    logging.debug(f"Add or update drug, recalc total_drug_price:\n\t\
                  {kwargs['d'].name}\n{kwargs}")
    pg.d_list.add_or_update(**kwargs)
    calc_price(pg.Parent.Parent)


def onEraseDrug(pg):
    logging.debug("Del drug, recalc total_drug_price")
    pg.d_list.remove_selected()
    pg.drugpicker.Clear()
    pg.drugpicker.SetFocus()
    calc_price(pg.Parent.Parent)
    
    
def calc_price(mv):
    price = setting["cong_kham_benh"]
    price += mv.order_book.GetPage(0).d_list.get_total_price()
    mv.total_cost.ChangeValue(otf.bill_int_to_str(price))


def onReuse(pg):
    mv = pg.Parent.Parent
    # keep old values
    logging.debug('on Reuse weight, days, linedruglist, total_cost')
    linedrugs = mv.visit.linedrugs.copy()
    w = pg.weight.Value
    d = pg.days.Value
    # unselect
    v_idx = mv.visit_list.GetFirstSelected()
    mv.visit_list.Select(v_idx, 0)
    # populate field with old values
    pg.d_list.Populate(linedrugs=linedrugs)
    pg.weight.ChangeValue(w)
    pg.days.ChangeValue(d)
    calc_price(mv)


def onSamplePrescriptionbtn(pg):
    mv = pg.Parent.Parent
    with SamplePrescriptionDialog(mv) as dlg:
        if dlg.ShowModal() == wx.ID_APPLY:
            ps, _ = dlg.get_selected_sample_prescription()
            pg.d_list.Clear()
            for i in ps.samplelinedrugs:
                pg.drugpicker.drugWH = i.drug
                pg.times.ChangeValue(str(i.times))
                pg.dosage_per.ChangeValue(i.dosage_per)
                calc_quantity(pg)
                kwargs = {
                    "d": i.drug,
                    "times": str(i.times),
                    "dosage_per": i.dosage_per,
                    "quantity": pg.quantity.Value,
                    "usage": pg.usage.Value
                }
                pg.d_list.add_or_update(**kwargs)
    calc_price(mv)
