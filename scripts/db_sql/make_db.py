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
    __tablename__ = 'patients'

    id = Column(Integer, primary_key=True)
    name = Column(String(50), index=True)
    gender = Column(Boolean, nullable=False)  # 0=nam, 1=nu
    birthdate = Column(Date, nullable=False)
    address = Column(Text, default="")
    past_history = Column(Text, default="")
    visits = relationship(
        "Visit", back_populates="patient", order_by='Visit.id',
        lazy='dynamic', cascade="all, delete-orphan")


class Visit(Base):
    __tablename__ = 'visits'

    id = Column(Integer, primary_key=True)
    exam_date = Column(DateTime, default=dt.datetime.now,
                       onupdate=dt.datetime.now)
    note = Column(Text)
    diag = Column(String(50), nullable=False)
    weight = Column(Float, default=0)
    days = Column(Integer, default=2)
    followup = Column(Text, default='')
    bill = Column(Integer, default=0)
    patient_id = Column(ForeignKey('patients.id'))
    patient = relationship("Patient", back_populates='visits')
    linedrugs = relationship(
        "LineDrug", lazy='selectin', cascade="all, delete-orphan")


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
    __tablename__ = 'linedrugs'
    __table_args__ = (CheckConstraint("quantity >= 0"),
                      CheckConstraint("times >= 0"),)

    id = Column(Integer, primary_key=True)
    drug_id = Column(ForeignKey("drugwarehouse.id"))
    dosage_per = Column(String(5), default=0)
    times = Column(Integer, default=0)
    quantity = Column(Integer, default=0)
    usage = Column(String(30), default='uống')
    visit_id = Column(ForeignKey("visits.id"))
    drug = relationship('DrugWarehouse', lazy='selectin')


class SamplePrescription(Base):
    __tablename__ = "sampleprescriptions"
    __table_args__ = (CheckConstraint("name != ''"),)

    id = Column(Integer, primary_key=True)
    name = Column(String(50), default='test', nullable=False)
    samplelinedrugs = relationship(
        "SampleLineDrug", lazy="selectin", cascade="all, delete-orphan")


class SampleLineDrug(Base):
    __tablename__ = "samplelinedrugs"
    __table_args__ = (CheckConstraint("times >= 0"),)

    id = Column(Integer, primary_key=True)
    drug_id = Column(ForeignKey("drugwarehouse.id"))
    times = Column(Integer, default=0)
    dosage_per = Column(String(5), default=0)
    sampleprescription_id = Column(ForeignKey("sampleprescriptions.id"))
    drug = relationship('DrugWarehouse', lazy='selectin')


class Staff(Base):
    __tablename__ = "staffs"

    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True, nullable=False, index=True)
    password = Column(String(20))
    job = Column(Enum('Doctor', 'Nurse', name='jobs'), nullable=False)
    workdays = relationship('WorkDay', lazy='dynamic', back_populates='staff')


class WorkDay(Base):
    __tablename__ = "workdays"

    id = Column(Integer, primary_key=True)
    time_login = Column(DateTime, nullable=False,
                        unique=True, default=dt.datetime.now)
    staff_id = Column(ForeignKey("staffs.id"))
    staff = relationship('Staff', back_populates='workdays')


class VisitQueue(Base):
    __tablename__ = 'visitqueue'
    id = Column(Integer, primary_key=True)
    time_added = Column(DateTime, nullable=False,
                        default=dt.datetime.now)
    is_seen = Column(Boolean, default=False, nullable=False)
    patient_id = Column(ForeignKey("patients.id"))
    patient = relationship('Patient', lazy='selectin')


class Therapy(Base):
    __tablename__ = "therapy"
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True, nullable=False, index=True)
    sale_price = Column(Integer, default=0)
    therapylinecost = relationship("TheparyLineCost", lazy="selectin",
                                   back_populates="therapy")

    def quantity(self):
        res = {}
        for lc in self.therapylinecost:
            res[lc.name] = lc.quantity
            print(f"{lc.name} has {lc.quantity} {lc.unit} left, \
                       each time use {lc.cost_on_1_use} => \
                       {lc.quantity / lc.cost_on_1_use} times left")
        return res


class TheparyLineCost(Base):
    __tablename__ = "therapylinecost"
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True, nullable=False, index=True)
    quantity = Column(Integer, default=0)
    unit = Column(String(10), nullable=False)
    cost_on_1_use = Column(Integer, default=1)
    therapy_id = Column(ForeignKey("therapy.id"))
    therapy = relationship("Therapy", lazy="selectin",
                           back_populates="therapylinecost")


def make_db():
    Base.metadata.create_all(engine)


def drop_db():
    Base.metadata.drop_all(engine)
