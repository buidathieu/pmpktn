from .make_db import DrugWarehouse
from initialize import *


import pandas as pd

def import_drug():
    sess = Session()
    df = pd.read_excel(warehouse_path, index_col=0)
    li = []
    for r in df.iterrows():
        i = r[1]
        li.append(DrugWarehouse(
            name=i['name'], quantity=i['quantity'], element=i['element'],
            expire=pd.to_datetime(i['expire']).date(), manufacturer=i['manufacturer'],
            usage_unit=i['usage_unit'], sale_unit=i['sale_unit'],
            sale_price=i['sale_price'], usage=i['usage'],
            purchase_price=i['purchase_price']))
    sess.add_all(li)
    commit_(sess)

def export_drug():
    sess = Session()
    drugs = sess.query(DrugWarehouse).all()
    columns = [x.__str__().split('.')[1] for x in DrugWarehouse.__table__.columns]
    df = pd.DataFrame([{c:getattr(d, c) for c in columns} for d in drugs])
    df.to_excel(warehouse_path, index=False)
