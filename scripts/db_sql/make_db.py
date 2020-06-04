# -*- coding: utf-8 -*-
from initialize import *

from sqlalchemy import Column, Integer, Float, String, DateTime,\
    Boolean, Date, Enum,\
    Text, CheckConstraint, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

import datetime as dt


Base = declarative_base()


class Patient(Base):
    __tablename__ = 'patient'

    id = Column(Integer, primary_key=True)
    name = Column(String(50), index=True)
    gender = Column(Boolean, nullable=False)  # 0=nam, 1=nu
    birthdate = Column(Date, nullable=False)
    address = Column(Text, default="")
    past_history = Column(Text, default="")
    visits = relationship(
        "Visit", order_by='desc(Visit.id)',
        lazy='dynamic', cascade="all, delete-orphan")


class Visit(Base):
    __tablename__ = 'visit'
    __table_args__ = (CheckConstraint("days > 0"),
                      CheckConstraint("weight >= 0"),
                      CheckConstraint("bill >= 0"))

    id = Column(Integer, primary_key=True)
    exam_date = Column(DateTime, default=dt.datetime.now,
                       onupdate=dt.datetime.now)
    note = Column(Text)
    diag = Column(String(50), nullable=False)
    weight = Column(Float(precision=1), default=0)
    days = Column(Integer, default=2)
    followup = Column(Text, default='')
    bill = Column(Integer, default=0)
    patient_id = Column(ForeignKey('patient.id'))
    linedrugs = relationship(
        "LineDrug", lazy='selectin', cascade="all, delete-orphan")
    linetherapies = relationship(
        "LineTherapy", lazy='selectin', cascade="all, delete-orphan")


class DrugWarehouse(Base):
    __tablename__ = 'drugwarehouse'
    __table_args__ = (CheckConstraint("quantity >= 0"),
                      CheckConstraint("sale_price >= 0"))

    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True, index=True)
    quantity = Column(Integer, default=0)
    usage_unit = Column(String(10), default='viên')  # ml
    sale_unit = Column(String(10), default='viên')  # chai
    purchase_price = Column(Integer, default=0)  # gia mua vo
    sale_price = Column(Integer, default=0)  # gia chai
    usage = Column(String(50), default='uống')  # cach dung


class LineDrug(Base):
    __tablename__ = 'linedrug'
    __table_args__ = (CheckConstraint("quantity >= 0"),
                      CheckConstraint("times >= 0"),)

    id = Column(Integer, primary_key=True)
    drug_id = Column(ForeignKey("drugwarehouse.id"))
    dosage_per = Column(String(5), default=0)
    times = Column(Integer, default=0)
    quantity = Column(Integer, default=0)
    usage = Column(String(30), default='uống')
    visit_id = Column(ForeignKey("visit.id"))
    drug = relationship('DrugWarehouse', lazy='selectin')


class SamplePrescription(Base):
    __tablename__ = "sampleprescription"
    __table_args__ = (CheckConstraint("name != ''"),)

    id = Column(Integer, primary_key=True)
    name = Column(String(50), default='test', nullable=False)
    samplelinedrugs = relationship(
        "SampleLineDrug", lazy="selectin", cascade="all, delete-orphan")


class SampleLineDrug(Base):
    __tablename__ = "samplelinedrug"
    __table_args__ = (CheckConstraint("times >= 0"),)

    id = Column(Integer, primary_key=True)
    drug_id = Column(ForeignKey("drugwarehouse.id"))
    times = Column(Integer, default=0)
    dosage_per = Column(String(5), default=0)
    sampleprescription_id = Column(ForeignKey("sampleprescription.id"))
    drug = relationship('DrugWarehouse', lazy='selectin')


class Staff(Base):
    __tablename__ = "staff"

    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True, nullable=False, index=True)
    password = Column(String(20))
    job = Column(Enum('Doctor', 'Nurse', name='jobs'), nullable=False)
    workdays = relationship('WorkDay', lazy='dynamic', back_populates='staff')


class WorkDay(Base):
    __tablename__ = "workday"

    id = Column(Integer, primary_key=True)
    time_login = Column(DateTime, nullable=False,
                        unique=True, default=dt.datetime.now)
    staff_id = Column(ForeignKey("staff.id"))
    staff = relationship('Staff', back_populates='workdays')


class VisitQueue(Base):
    __tablename__ = 'visitqueue'

    id = Column(Integer, primary_key=True)
    time_added = Column(DateTime, nullable=False,
                        default=dt.datetime.now)
    patient_id = Column(ForeignKey("patient.id"))
    patient = relationship('Patient', lazy='selectin')


class Therapy(Base):
    __tablename__ = "therapy"

    id = Column(Integer, primary_key=True)
    name = Column(String(200), unique=True, nullable=False, index=True)
    sale_price = Column(Integer, default=0)
    therapylinedrugs = relationship(
        "TherapyLineDrug", lazy="selectin", cascade="all, delete-orphan")

    def quantity(self):
        return min(
            [lc.drug.quantity / lc.cost_on_1_use for lc in self.therapylinedrugs])


class TherapyLineDrug(Base):
    __tablename__ = "therapylinedrug"
    id = Column(Integer, primary_key=True)
    drug_id = Column(ForeignKey("drugwarehouse.id"))
    cost_on_1_use = Column(Integer, default=1)
    therapy_id = Column(ForeignKey("therapy.id"))
    drug = relationship('DrugWarehouse', lazy='selectin')


class LineTherapy(Base):
    __tablename__ = "linetherapy"
    id = Column(Integer, primary_key=True)
    therapy_id = Column(ForeignKey("therapy.id"))
    visit_id = Column(ForeignKey("visit.id"))
    therapy = relationship(
        "Therapy", lazy="selectin")


def make_db():
    Base.metadata.create_all(engine)


def drop_db():
    Base.metadata.drop_all(engine)
