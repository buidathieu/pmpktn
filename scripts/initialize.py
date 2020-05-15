from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from wx import NewId

import os
import json
# High DPI aware
import ctypes
try:
    ctypes.windll.shcore.SetProcessDpiAwareness(True)
except Exception:
    pass
from contextlib import contextmanager


SCRIPTS_PATH = os.path.dirname(os.path.abspath(__file__))
DIR_PATH = os.path.dirname(SCRIPTS_PATH)

# bm_path_paths
bm_path = os.path.join(SCRIPTS_PATH, 'bitmaps')

new_p_bm = os.path.join(bm_path, 'new_patient.png')
del_p_bm = os.path.join(bm_path, 'delete_patient.png')

save_drug_bm = os.path.join(bm_path, 'save_drug.png')
erase_drug_bm = os.path.join(bm_path, 'erase_drug.png')

new_visit_bm = os.path.join(bm_path, 'new_visit.png')
save_visit_bm = os.path.join(bm_path, 'save_visit.png')
del_visit_bm = os.path.join(bm_path, 'del_visit.png')

print_bm = os.path.join(bm_path, 'print.png')
refresh_bm = os.path.join(bm_path, 'refresh.png')

plus_bm = os.path.join(bm_path, 'plus.png')
pencil_bm = os.path.join(bm_path, 'pencil.png')
minus_bm = os.path.join(bm_path, 'minus.png')



with open(os.path.join(DIR_PATH, "setting.json"), "r", encoding="utf-8-sig") as f:
    setting = json.load(f)

sql_path = os.path.join(DIR_PATH, setting["database_name"])
engine = create_engine('sqlite:///{}'.format(sql_path), echo=setting["echo"])
Session = sessionmaker(bind=engine)




#  my ids
id_new_patient = NewId()
id_new_visit = NewId()
id_save_visit = NewId()

# some size
ma_bn_width = 50
bn_width = 250
gioi_width = 50
ns_width = 100
date_width = 150
ma_lk_width = 130
days_size = (70, -1)
name_size = (bn_width, -1)
bd_size = (ns_width, -1)
note_size = (-1, 60)
dose_size = (50, -1)
drugctrl_size = (200, -1)
popup_size = (500, 300, 300)
d_stt_w = 40
d_name_w = 150
d_l1cu_w = 80
d_socu_w = 60
d_tc_w = 80

gender_dict = {0: 'nam',
               1: 'nữ',
               'nam': 0,
               'nữ': 1}

tree_size = (-1, 300)
add_edit_prescription_dialog_size = (-1, 600)

@contextmanager
def session_scope():
    """Provide a transactional scope around a series of operations."""
    session = Session()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()