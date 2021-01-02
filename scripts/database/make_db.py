# -*- coding: utf-8 -*-
from initialize import *

from sqlalchemy import Column, Integer, Float, String,\
    DateTime, Date, Enum,\
    Text, CheckConstraint, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

import datetime as dt


Base = declarative_base()


class Patient(Base):
    __tablename__ = 'patient'

    id = Column(Integer, primary_key=True)
    name = Column(String(50), index=True)
    gender = Column(Enum('nam', 'nữ', name='gender'), nullable=False)
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
    diagnosis = Column(String(50), nullable=False)
    weight = Column(Float(precision=1), default=0)
    days = Column(Integer, default=2)
    followup = Column(Text, default='')
    bill = Column(Integer, default=0)
    patient_id = Column(ForeignKey('patient.id'))
    linedrugs = relationship(
        "LineDrug", lazy='selectin', cascade="all, delete-orphan")


class DrugWarehouse(Base):
    __tablename__ = 'drugwarehouse'
    __table_args__ = (CheckConstraint("quantity >= 0"),
                      CheckConstraint("sale_price >= 0"))

    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True, index=True)
    element = Column(String(300), index=True)
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


def make_db():
    Base.metadata.create_all(engine)


def drop_db():
    Base.metadata.drop_all(engine)
