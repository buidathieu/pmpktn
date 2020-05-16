from .make_db import *
from initialize import session_scope
from datetime import date
from sqlalchemy import func


def query_all_patient(sess=None):
    return sess.query(Patient)


def query_today_patient(sess=None):
    return sess.query(Patient).\
        join(Visit).\
        filter(func.DATE(Visit.exam_date) == date.today())


def query_linedrug_list_by_name(s):
    with session_scope() as sess:
        s = '%' + s + '%'
        return sess.query(DrugWarehouse).\
            filter(DrugWarehouse.name.like(s))


def add_patient(name, gender, birthdate, address, past_history, sess=None):
    p = Patient(name=name, gender=gender, birthdate=birthdate,
                address=address, past_history=past_history,
                )
    sess.add(p)
    sess.commit()
    return p


def edit_patient(p, name, gender, birthdate, address, past_history, sess=None):
    p.name = name
    p.gender = gender
    p.birthdate = birthdate
    p.address = address
    p.past_history = past_history
    sess.commit()
    return p

def delete_patient(p, sess=None):
    sess.delete(p)
    sess.commit()

def update_visit(v, note, diag, weight, days, followup, bill, linedrugs, sess=None):
    v.note = note
    v.diag = diag
    v.weight = weight
    v.days = days
    v.followup = followup
    v.bill = bill
    for i in v.linedrugs:
        drug = sess.query(DrugWarehouse).get(i.drug_id)
        drug.quantity += i.quantity
        sess.delete(i)
    for i in linedrugs:
        v.linedrugs.append(LineDrug(**i))
        drug = sess.query(DrugWarehouse).get(i['drug_id'])
        drug.quantity -= i['quantity']


def add_visit(pid, note, diag, weight, days, followup, bill, linedrugs, sess):
    v = Visit(note=note,
              diag=diag,
              weight=weight,
              days=days,
              followup=followup,
              bill=bill,
              patient_id=pid)
    v.linedrugs = []
    for i in linedrugs:
        v.linedrugs.append(LineDrug(**i))
        drug = sess.query(DrugWarehouse).get(i['drug_id'])
        drug.quantity -= i['quantity']
    sess.add(v)


def save_old_visit(p, past_history,
                   v, note, diag, weight, days, followup, bill, linedrugs,
                   sess=None):
    p.past_history = past_history
    update_visit(v, note, diag, weight, days,
                 followup, bill, linedrugs, sess)
    sess.commit()


def save_new_visit(p, past_history,
                   note, diag, weight, days, followup, bill, linedrugs,
                   sess=None):
    p.past_history = past_history
    add_visit(p.id, note, diag, weight, days,
              followup, bill, linedrugs, sess)
    sess.commit()


def GetTodayReport():
    with session_scope() as sess:
        query = sess.query(Visit).filter(
            func.DATE(Visit.exam_date) == date.today())
        count = query.count()
        income = 0
        cost = 0
        sale = 0
        for visit in query:
            income += visit.bill
            for linedrug in visit.linedrugs:
                cost += (linedrug.drug.purchase_price * linedrug.quantity)
                sale += (linedrug.drug.sale_price * linedrug.quantity)
        profit = sale - cost
    return count, income, cost, sale, profit


def query_sample_prescription_list(sess):
    return sess.query(SamplePrescription)


def query_drugWH_list(sess):
    return sess.query(DrugWarehouse)


def del_sample_prescription(ps, sess):
    sess.delete(ps)
    sess.commit()


def add_sample_prescription(name, samplelinedrugs, sess):
    new_ps = SamplePrescription(name=name)
    new_ps.samplelinedrugs = []
    for drug_id, times, dosage_per in samplelinedrugs:
        new_ps.samplelinedrugs.append(
            SampleLineDrug(drug_id=drug_id,
                           times=times,
                           dosage_per=dosage_per)
        )
    sess.add(new_ps)
    sess.commit()
    return new_ps


def upd_sample_prescription(ps, name, samplelinedrugs, sess):
    ps.name = name
    for i in ps.samplelinedrugs:
        sess.delete(i)
    for drug_id, times, dosage_per in samplelinedrugs:
        ps.samplelinedrugs.append(
            SampleLineDrug(drug_id=drug_id,
                           times=times,
                           dosage_per=dosage_per)
        )
    sess.commit()
