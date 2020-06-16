from .make_db import *
from initialize import *
import datetime as dt
from sqlalchemy import func, extract


#  login
def query_staff_list(sess=None):
    return sess.query(Staff)


def save_staff_workday(staff, sess=None):
    staff.workdays.append(WorkDay())
    commit_(sess)


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
    commit_(sess)
    return vq


def remove_visitqueue(queue, sess=None):
    sess.delete(queue)
    commit_(sess)


def get_visitqueue(sess=None):
    return sess.query(VisitQueue)


def edit_patient(p, name, gender, birthdate,
                 address, past_history, sess):
    p.name = name
    p.gender = gender
    p.birthdate = birthdate
    p.address = address
    p.past_history = past_history
    commit_(sess)
    return p


# left_panel_classes.py
def get_today_seen_patient_list(sess=None):
    return sess.query(Patient).\
        join(Visit).\
        filter(func.DATE(Visit.exam_date) == dt.date.today())


# picker popup
def query_linedrug_list(sess):
    return sess.query(DrugWarehouse)


def query_therapy_list(sess):
    return sess.query(Therapy)


# mainview
def add_patient(name, gender, birthdate, address, past_history, sess=None):
    new_patient = Patient(name=name, gender=gender, birthdate=birthdate,
                          address=address, past_history=past_history,
                          )
    sess.add(new_patient)
    commit_(sess)
    return new_patient


# save button
def update_patient(p, past_history, sess):
    p.past_history = past_history
    return p


def do_seen_patient(vq, sess):
    sess.delete(vq)
    return vq


def add_linedrugs_to_visit(v, linedrugs, sess):
    for i in v.linedrugs:
        drug = sess.query(DrugWarehouse).get(i.drug_id)
        drug.quantity += i.quantity
        sess.delete(i)
    for i in linedrugs:
        v.linedrugs.append(LineDrug(**i))
        drug = sess.query(DrugWarehouse).get(i['drug_id'])
        drug.quantity -= i['quantity']


def add_linetherapies_to_visit(v, linetherapies, sess):
    for lt in v.linetherapies:
        therapy = sess.query(Therapy).get(lt.therapy_id)
        for tld in therapy.therapylinedrugs:
            drug = sess.query(DrugWarehouse).get(tld.drug_id)
            drug.quantity += tld.cost_on_1_use
        sess.delete(lt)
    for t_id in linetherapies:
        v.linetherapies.append(LineTherapy(therapy_id=t_id))
        therapy = sess.query(Therapy).get(t_id)
        for tld in therapy.therapylinedrugs:
            drug = sess.query(DrugWarehouse).get(tld.drug_id)
            drug.quantity -= tld.cost_on_1_use


def update_visit(v, note, diag, weight, days,
                 followup, bill, linedrugs, linetherapies,
                 staff_id, sess):
    v.note = note
    v.diag = diag
    v.weight = weight
    v.days = days
    v.followup = followup
    v.bill = bill
    v.staff_id = staff_id
    add_linedrugs_to_visit(v, linedrugs, sess)
    add_linetherapies_to_visit(v, linetherapies, sess)
    return v


def add_visit(p, note, diag, weight, days,
              followup, bill, linedrugs, linetherapies,
              staff_id, sess):
    v = Visit(note=note,
              diag=diag,
              weight=weight,
              days=days,
              followup=followup,
              bill=bill,
              patient_id=p.id,
              staff_id=staff_id)
    add_linedrugs_to_visit(v, linedrugs, sess)
    add_linetherapies_to_visit(v, linetherapies, sess)
    sess.add(v)
    return v


def save_old_visit(p, v, staff_id, vq, past_history,
                   note, diag, weight, days,
                   followup, bill, linedrugs, linetherapies,
                   sess=None):
    patient = update_patient(p, past_history, sess)
    visit = update_visit(v, note, diag, weight, days,
                         followup, bill, linedrugs, linetherapies, staff_id, sess)
    commit_(sess)
    return patient, visit


def save_new_visit(p, v, staff_id, vq, past_history,
                   note, diag, weight, days,
                   followup, bill, linedrugs, linetherapies,
                   sess=None):
    patient = update_patient(p, past_history, sess)
    visit = add_visit(p, note, diag, weight, days,
                      followup, bill, linedrugs, linetherapies, staff_id, sess)
    do_seen_patient(vq, sess)
    commit_(sess)
    return patient, visit


# report
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


def del_sample_prescription(ps, sess):
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
    commit_(sess)
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
    commit_(sess)
