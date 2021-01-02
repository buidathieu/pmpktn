from .make_db import *
from initialize import *
import datetime as dt
from sqlalchemy import func


# left_panel_classes.py
def get_today_seen_patient_list(sess=None):
    return sess.query(Patient).\
        join(Visit).\
        filter(func.DATE(Visit.exam_date) == dt.date.today())


def get_all_patient_list(sess=None):
    return sess.query(Patient)


# picker popup
def query_linedrug_list(sess):
    return sess.query(DrugWarehouse).filter(DrugWarehouse.quantity > 0)


def query_therapy_list(sess):
    return sess.query(Therapy)


# patient dialog
def add_patient(name, gender, birthdate, address, sess=None):
    new_patient = Patient(name=name, gender=gender, birthdate=birthdate,
                          address=address)
    sess.add(new_patient)
    sess.commit_()
    return new_patient


def edit_patient(patient, name, gender, birthdate,
                 address, sess):
    patient.name = name
    patient.gender = gender
    patient.birthdate = birthdate
    patient.address = address
    sess.commit_()
    return patient


# save button

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


def save_old_visit(p, v, past_history,
                   note, diagnosis, weight, days,
                   followup, bill, linedrugs,
                   sess=None):
    p.past_history = past_history
    v.note = note
    v.diagnosis = diagnosis
    v.weight = weight
    v.days = days
    v.followup = followup
    v.bill = bill
    # restock
    for i in v.linedrugs:
        drug = sess.query(DrugWarehouse).get(i.drug_id)
        drug.quantity += i.quantity
        sess.delete(i)
    # takeout
    for i in linedrugs:
        v.linedrugs.append(LineDrug(**i))
        drug = sess.query(DrugWarehouse).get(i['drug_id'])
        drug.quantity -= i['quantity']
    sess.commit_()


def save_new_visit(p, past_history,
                   note, diagnosis, weight, days,
                   followup, bill, linedrugs,
                   sess=None):
    p.past_history = past_history
    new_visit = Visit(
        note=note,
        diagnosis=diagnosis,
        weight=weight,
        days=days,
        followup=followup,
        bill=bill,
        patient_id=p.id,
    )
    for i in linedrugs:
        new_visit.linedrugs.append(LineDrug(**i))
        drug = sess.query(DrugWarehouse).get(i['drug_id'])
        drug.quantity -= i['quantity']
    sess.add(new_visit)
    sess.commit_()


# report
def GetTodayReport():
    sess = Session()
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
    sess.commit_()
    return count, income, cost, sale, profit
