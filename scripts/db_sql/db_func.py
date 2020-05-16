from .make_db import *
from initialize import *
import datetime as dt
from sqlalchemy import func, extract


#  login
def query_staff_list(sess=None):
    return sess.query(Staff)


def save_staff_workday(staff, sess=None):
    staff.workdays.append(WorkDay())
    sess.commit()


# nurseview
def search_patient(name, gender, birthyear, sess=None):
    query = sess.query(Patient).\
        filter(Patient.name.contains(name))
    if gender in [0, 1]:
        query = query.filter(Patient.gender == bool(gender))
    if birthyear.isnumeric():
        query = query.filter(
            extract(
                'year',
                Patient.birthdate) == int(birthyear))
    return query


def add_new_visitqueue(pid, sess=None):
    vq = sess.add(VisitQueue(patient_id=pid))
    sess.commit()
    return vq


def remove_visitqueue(queue, sess=None):
    sess.delete(queue)
    sess.commit()


def get_visitqueue(sess=None):
    return sess.query(VisitQueue).\
        filter(VisitQueue.is_seen == False)


# mainview
def get_today_patient_list(sess=None):
    return sess.query(Patient).\
        join(Visit).\
        filter(func.DATE(Visit.exam_date) == dt.date.today())


def get_queuing_patient_list(sess=None):
    return sess.query(Patient).\
        join(VisitQueue).\
        filter(VisitQueue.is_seen == False).\
        order_by(VisitQueue.id)


def query_linedrug_list_by_name(s):
    with session_scope() as sess:
        s = '%' + s + '%'
        return sess.query(DrugWarehouse).\
            filter(DrugWarehouse.name.like(s))


def add_patient(name, gender, birthdate, address, past_history, sess=None):
    new_patient = Patient(name=name, gender=gender, birthdate=birthdate,
                          address=address, past_history=past_history,
                          )
    sess.add(new_patient)
    sess.commit()
    return new_patient


def edit_patient(pid, name, gender, birthdate, address, past_history, sess):
    p = sess.query(Patient).get(pid)
    p.name = name
    p.gender = gender
    p.birthdate = birthdate
    p.address = address
    p.past_history = past_history
    sess.commit()
    return p


def update_visit(vid, note, diag, weight, days,
                 followup, bill, linedrugs, sess):
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


def do_seen_patient(pid, sess):
    vq = sess.query(VisitQueue).join(Patient).\
        filter(Patient.id == pid).\
        filter(VisitQueue.is_seen == False).first()
    vq.is_seen = True


def save_old_visit(pid, name, birthdate, address, past_history,
                   vid, note, diag, weight, days, followup, bill, linedrugs,
                   sess=None):
    update_patient(pid, name, birthdate, address, past_history, sess)
    update_visit(vid, note, diag, weight, days,
                 followup, bill, linedrugs, sess)
    sess.commit()


def save_new_visit(pid, name, birthdate, address, past_history,
                   note, diag, weight, days, followup, bill, linedrugs,
                   sess=None):
    update_patient(pid, name, birthdate, address, past_history, sess)
    add_visit(pid, note, diag, weight, days,
              followup, bill, linedrugs, sess)
    do_seen_patient(pid, sess)
    sess.commit()


def GetTodayReport():
    with session_scope() as sess:
        query = sess.query(Visit).filter(
            func.DATE(Visit.exam_date) == dt.date.today())
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
