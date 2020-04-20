from .make_db import *
from .__init__ import *
from datetime import date
from sqlalchemy import func


def check_exist_staff_date(date=date.today(), sess=None):
    q = sess.query(WorkDay).filter(WorkDay.date == date)
    return sess.query(q.exists()).scalar()


def query_staff_list(sess=None):
    return sess.query(Staff)


def save_staff_workday(staff, date=date.today(), sess=None):
    d = WorkDay(date=date)
    staff.workdays.append(d)
    sess.commit()


def get_patient_list_by_name(s='', today=False, sess=None):
    if today:
        result = sess.query(Patient).\
            join(Visit).\
            filter(func.DATE(Visit.exam_date) == date.today()).\
            filter(Patient.name.contains(s))
    else:
        result = sess.query(Patient).filter(
            Patient.name.contains(s))
    return result


def query_linedrug_list_by_name(s):
    with session_scope() as sess:
        s = '%' + s + '%'
        return sess.query(DrugWarehouse).\
            filter(DrugWarehouse.name.like(s))


def create_new_patient(name, gender, birthdate, address, past_history, sess=None):
    new_patient = Patient(name=name, gender=gender, birthdate=birthdate,
                          address=address, past_history=past_history,
                          )
    sess.add(new_patient)
    sess.commit()
    return new_patient


def update_patient(pid, name, birthdate, address, past_history, sess):
    p = sess.query(Patient).get(pid)
    p.name = name
    p.birthdate = birthdate
    p.address = address
    p.past_history = past_history


def update_visit(vid, note, diag, weight, days, followup, bill, linedrugs, sess):
    v = sess.query(Visit).get(vid)
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


def save_old_visit(pid, name, birthdate, address, past_history,
                   vid, note, diag, weight, days, followup, bill, linedrugs,
                   sess=None):
    update_patient(pid, name, birthdate, address, past_history, sess)
    update_visit(vid, note, diag, weight, days,
                 followup, bill, linedrugs, sess)


def save_new_visit(pid, name, birthdate, address, past_history,
                   note, diag, weight, days, followup, bill, linedrugs,
                   sess=None):
    update_patient(pid, name, birthdate, address, past_history, sess)
    add_visit(pid, note, diag, weight, days,
              followup, bill, linedrugs, sess)


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


# Query with the same sess in functions related to SamplePrescription


def query_sample_prescription_list(sess):
    return sess.query(SamplePrescription)


def query_drugWH_list(sess):
    return sess.query(DrugWarehouse)


def del_sample_precription(ps, sess):
    sess.delete(ps)


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
