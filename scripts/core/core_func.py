from initialize import *
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
    
    
def onVisitSelect(mv, visit):
    # mv.visit_info.Update()
    pass
    
def onVisitDeselect(mv, visit=None):
    # mv.visit_info.Clear()
    pass