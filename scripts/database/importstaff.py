from .make_db import Staff
from initialize import *

def import_staff():
    sess = Session()
    
    res = []
    doctor_li = ["NGUYỄN DUY KHẢI", "VƯƠNG KIẾN THANH", "TRẦN VŨ",
                 "HUỲNH HỮU DANH", "QUÁCH NGỌC VINH", "BÙI THỊ LỆ HUYỀN"]
    for i in doctor_li:
        res.append(Staff(name=i, password=1, job='Doctor'))
    nurse_li = []
    for i in nurse_li:
        res.append(Staff(name=i, password=1, job='Nurse'))
    sess.add_all(res)
    commit_(sess)
