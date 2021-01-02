# -*- coding: utf-8 -*-
from .make_db import *
from initialize import *
import datetime as dt
from random import randint, choices, uniform, sample, random
import math
from fractions import Fraction as fr

# id
# name
# element
# quantity
# usage_unit
# sale_unit
# purchase_price
# sale_price
# usage


sample_drugs = [[1, 'AMOXICILLIN 500mg', 'amoxicillin', 1000, 'gói', 'gói', 5000, 10000, 'uống'],
                [2, 'CEFUROXIM 250mg', 'cefuroxim', 3000, 'gói', 'gói', 30000, 25000, 'uống'],
                [3, 'PARACETAMOL 80mg', 'paracetamol', 10000, 'gói', 'gói', 5000, 3000, 'uống'],
                [4, 'PARACETAMOL 500mg', 'para', 10000, 'viên', 'viên', 15000, 10000, 'uống'],
                [5, 'DESLORATADINE', 'desloratadin', 5000, 'ml', 'chai', 40000, 35000, 'uống'],
                [6, 'BACIVIT H', "men", 10000, 'gói', 'gói', 2000, 1000, 'uống'],
                [7, 'HOASTEX 90ml', "hoas", 5000, 'ml', 'chai', 20000, 15000, 'uống'],
                [8, 'ACEMUC 200mg', 'acemu', 100, 'gói', 'gói', 5000, 3000, 'uống'],
                [9, 'TOBREX', 'Tobramycin', 2, 'giọt', 'lọ', 1000, 2000, 'nhỏ mắt']
                ]


def rdate(exam=False):
    if exam:
        y = dt.datetime.now().year
        m = dt.datetime.now().month
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
        li.append(Patient(name=name, gender=choices(['nam', 'nữ'])[0],
                          birthdate=rdate(),
                          address=rtext(), past_history=rtext()))
    return li


def random_visit_list(k=10, w_note=False):
    li = []
    for i in range(k):
        li.append(Visit(exam_date=choices([rdate(exam=True),
                                           dt.datetime.now()])[0],
                        note=rtext(),
                        diagnosis=rtext(),
                        weight=round(uniform(5, 20), 1),
                        days=randint(1, 5),
                        followup=rtext(),
                        bill=int(random() * 1000) * 1000,
                        patient_id=(i + 1),
                        )
                  )
    return li


def sample_warehouse():
    li = []
    for i in sample_drugs:
        li.append(DrugWarehouse(
            id=i[0],
            name=i[1],
            element=i[2],
            quantity=i[3],
            usage_unit=i[4],
            sale_unit=i[5],
            purchase_price=i[6],
            sale_price=i[7],
            usage=i[8]))
    return li


def random_linedrug(k=10):
    li = []
    for i in range(k):
        for j in sample(sample_drugs, k=choices([1, 2, 3])[0]):
            a = choices(['1/3', '0.5', '2'])[0]
            b = choices([1, 2, 3])[0]
            try:
                quantity = float(a) * b
            except ValueError:
                quantity = fr(a) * b
            if j[5] == "chai":
                quantity = 1
            li.append(
                LineDrug(
                    drug_id=j[0],
                    dosage_per=a,
                    times=b,
                    quantity=math.ceil(quantity),
                    usage=f"Ngày {j[8]} {b} lần, lần {a} {j[4]}",
                    visit_id=i + 1))
    return li


def populate_db(k=10):
    li = [random_patient_list(k),
          random_visit_list(k),
          sample_warehouse(),
          random_linedrug(k),
          ]
    flatten_li = [obj for sublist in li for obj in sublist]
    sess = Session()
    sess.add_all(flatten_li)
    sess.commit()
    sess.close()
