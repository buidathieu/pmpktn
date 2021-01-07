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
    return sess.query(DrugWarehouse)


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


# save
def save_old_visit(p, v, past_history,
                   note, diagnosis, weight, days,
                   bill, followup, linedrugs,
                   sess=None):
    p.past_history = past_history
    v.note = note
    v.diagnosis = diagnosis
    v.weight = weight
    v.days = days
    v.bill = bill
    v.followup = followup
    # restock
    for i in v.linedrugs:
        drug = sess.query(DrugWarehouse).get(i.drug_id)
        if drug.quantity == -1:
            continue
        else:
            drug.quantity += i.quantity
        sess.delete(i)
    # takeout
    for i in linedrugs:
        drug = sess.query(DrugWarehouse).get(i['drug_id'])
        if drug.quantity == -1:
            continue
        else:
            v.linedrugs.append(LineDrug(**i))
            drug = sess.query(DrugWarehouse).get(i['drug_id'])
            if drug.quantity < i['quantity']:
                sess.rollback()
                return -1
            else:
                drug.quantity -= i['quantity']
    sess.commit_()


def save_new_visit(p, past_history,
                   note, diagnosis, weight, days,
                   bill, followup, linedrugs,
                   sess=None):
    p.past_history = past_history
    new_visit = Visit(
        note=note,
        diagnosis=diagnosis,
        weight=weight,
        days=days,
        bill=bill,
        followup=followup,
        patient_id=p.id,
    )
    for i in linedrugs:
        new_visit.linedrugs.append(LineDrug(**i))
        drug = sess.query(DrugWarehouse).get(i['drug_id'])
        if drug.quantity == -1:
            continue
        elif drug.quantity < i['quantity']:
            sess.rollback()
            return -1
        else:
            drug.quantity -= i['quantity']
    sess.add(new_visit)
    sess.commit_()
