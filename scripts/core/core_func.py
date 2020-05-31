from initialize import *
import db_sql.db_func as dbf
import other_func as otf
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
    pg.d_list.Update(v.linedrugs)
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

    
def onNewVisit(mv):
    mv.visit = None


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