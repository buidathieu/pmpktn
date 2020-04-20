# -*- coding: utf-8 -*-
from .make_db import *
from .__init__ import *
import datetime as dt
from random import randint, choices, uniform, sample
import math
from fractions import Fraction as fr


sample_drugs = [['AMOXICILLIN 500mg', 5000, 'gói', 'gói', 10000, 'uống', 5000],
                ['CEFUROXIM 250mg', 3000, 'gói', 'gói', 30000, 'uống', 25000],
                ['PARACETAMOL 80mg', 10000, 'gói', 'gói', 5000, 'uống', 3000],
                ['PARACETAMOL 150mg', 10000, 'gói', 'gói', 7000, 'uống', 4000],
                ['PARACETAMOL 250mg', 10000, 'gói', 'gói', 10000, 'uống', 5000],
                ['PARACETAMOL 500mg', 10000, 'viên', 'viên', 15000, 'uống', 10000],
                ['VITAMIN C 100mg', 10000, 'viên', 'viên', 2000, 'uống', 1000],
                ['SIMETHICON 15ml', 500, 'ml', 'chai', 30000, 'uống', 25000],
                ['DESLORATADINE', 5000, 'ml', 'chai', 40000, 'uống', 35000],
                ['BACIVIT H', 10000, 'gói', 'gói', 2000, 'uống', 1000],
                ['HOASTEX 90ml', 5000, 'ml', 'chai', 20000, 'uống', 15000],
                ['ACEMUC 200mg', 100, 'gói', 'gói', 5000, 'uống', 3000],
                ['ACEMUC 100mg', 100, 'gói', 'gói', 5000, 'uống', 3000],
                ['PASSEDYL E', 100, 'ml', 'chai', 5000, 'uống', 3000],
                ['PECTOL 90mg', 100, 'ml', 'chai', 5000, 'uống', 3000],
                ]


def rdate(exam=False):
    if exam:
        y = dt.datetime.now().year
        m = randint(dt.datetime.now().month - 3, dt.datetime.now().month)
        h = randint(18, 21)
        m2 = randint(0, 59)
        s = randint(0, 59)
    else:
        y = randint(1990, 2015)
        m = randint(1, 12)

    if m in [1, 3, 5, 7, 8, 10, 12]:
        d = randint(1, 31)
    elif m == 2:
        d = randint(1, 28)
    else:
        d = randint(1, 30)

    if exam:
        return dt.datetime(y, m, d, h, m2, s)
    else:
        return dt.date(y, m, d)


def rname():
    name_l = ['PHÙNG THÁI LONG', 'VĂN NGỌC HÂN', 'NGUYỄN HUỲNH BẢO NGỌC',
              'LÊ NGUYỄN KHÁNH LY', 'NGUYỄN THỊ PHƯƠNG TRINH',
              'NGUYỄN MẠNH THẮNG', 'NGUYỄN ĐỨC THỊNH', 'PHẠM ĐỨC TÍNH',
              'TRẦN NGUYỄN TRUNG HIẾU', 'NGUYỄN VĂN TÀI',
              'TRẦN PHẠM KHANG', 'LÊ PHƯỚC TOÀN', 'NGUYỄN THẾ LƯỢT',
              'PHẠM THỊ TRÀ MY', 'VÕ DƯƠNG TÚ QUỲNH', 'NGUYỄN THỊ CẨM GIANG',
              'MAI THỊ BÍCH TUYỀN', 'PHẠM HẠP TUỆ MẪN', 'ĐẶNG BẢO HÂN',
              'HOÀNG GIA HUY']
    for i in range(len(name_l)):
        yield(name_l[i])


def rtext():
    txt = choices('1234567890qwertyuiopasdfghjklzxcvbnm ', k=randint(20, 50))
    return ''.join(txt)


def random_patient_list(k=10):
    li = []
    for i, name in zip(range(k), rname()):
        li.append(Patient(name=name, gender=randint(0, 1),
                          birthdate=rdate(),
                          address=rtext(), past_history=rtext()))
    return li


def random_visit_list(k=10, w_note=False):
    li = []
    for i in range(k):
        li.append(Visit(exam_date=choices([rdate(exam=True),
                                           dt.datetime.now()])[0],
                        note=rtext(),
                        diag=rtext(),
                        weight=round(uniform(5, 20), 1),
                        days=randint(1, 5),
                        followup=rtext(),
                        bill=100000,
                        patient_id=(i + 1),
                        )
                  )
    return li


def sample_warehouse():
    li = []
    for i in sample_drugs:
        li.append(DrugWarehouse(
            name=i[0], quantity=i[1],
            usage_unit=i[2], sale_unit=i[3],
            sale_price=i[4], usage=i[5], purchase_price=i[6]))
    return li


def random_linedrug(k=10):
    li = []
    for i in range(k):
        for j in sample(list(range(15)), k=choices([1, 2, 3])[0]):
            a = choices(['1/3', '0.5', '2'])[0]
            b = choices([1, 2, 3])[0]
            try:
                quantity = float(a) * b
            except ValueError:
                quantity = fr(a) * b
            if sample_drugs[j][3] == "chai":
                quantity = 1
            li.append(LineDrug(drug_id=j + 1,
                               dosage_per=a,
                               times=b,
                               quantity=math.ceil(quantity),
                               usage=f"Ngày {sample_drugs[j][5]} {b} lần, lần {a} {sample_drugs[j][2]}",
                               visit_id=i + 1
                               )
                      )
    return li


def random_sample_prescription(k=10):
    li = []
    for i in range(k):
        li.append(SamplePrescription(name=rtext()))
    return li


def random_sample_linedrug(k=10):
    li = []
    for i in range(k):
        for j in sample(list(range(15)), k=choices([1, 2, 3])[0]):
            a = choices(['1/3', '0.5', '2'])[0]
            b = choices([1, 2, 3])[0]
            li.append(SampleLineDrug(drug_id=j + 1,
                                     sampleprescription_id=i + 1,
                                     dosage_per=a,
                                     times=b,
                                     ))
    return li


def make_staff():
    li = ["NGUYỄN DUY KHẢI", "VƯƠNG KIẾN THANH", "TRẦN VŨ",
          "HUỲNH HỮU DANH", "QUÁCH NGỌC VINH", "BÙI THỊ LỆ HUYỀN"]
    res = []
    for i in li:
        res.append(Staff(name=i))
    return res


def commit_population(k=10):
    li = [random_patient_list(k),
          random_visit_list(k),
          sample_warehouse(),
          random_linedrug(k),
          random_sample_prescription(),
          random_sample_linedrug(),
          make_staff()]
    flatten_li = [obj for sublist in li for obj in sublist]
    with session_scope() as sess:
        sess.add_all(flatten_li)


def commit_drugwarehouse():
    li = [sample_warehouse(),
          random_sample_prescription(),
          random_sample_linedrug()]
    flatten_li = [obj for sublist in li for obj in sublist]
    with session_scope() as sess:
        sess.add_all(flatten_li)
