import os
import json
# High DPI aware
import ctypes
try:
    ctypes.windll.shcore.SetProcessDpiAwareness(True)
except Exception:
    pass
from wx import NewId, Colour
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

background_color = Colour(206, 219, 186)

# app structure
DIR_PATH = os.path.dirname(os.path.abspath(__file__))
BITMAPS_PATH = os.path.join(DIR_PATH, 'core', 'bitmaps')
DB_PATH = os.path.join(DIR_PATH, "database")
SETTINGS_PATH = os.path.join(DIR_PATH, "settings")
if not os.path.exists(DB_PATH):
    os.mkdir(DB_PATH)

# bitmaps
new_p_bm = os.path.join(BITMAPS_PATH, 'new_patient.png')
del_p_bm = os.path.join(BITMAPS_PATH, 'delete_patient.png')
save_drug_bm = os.path.join(BITMAPS_PATH, 'save_drug.png')
erase_drug_bm = os.path.join(BITMAPS_PATH, 'erase_drug.png')
new_visit_bm = os.path.join(BITMAPS_PATH, 'new_visit.png')
save_visit_bm = os.path.join(BITMAPS_PATH, 'save_visit.png')
del_visit_bm = os.path.join(BITMAPS_PATH, 'del_visit.png')
print_bm = os.path.join(BITMAPS_PATH, 'print.png')
refresh_bm = os.path.join(BITMAPS_PATH, 'refresh.png')
plus_bm = os.path.join(BITMAPS_PATH, 'plus.png')
pencil_bm = os.path.join(BITMAPS_PATH, 'pencil.png')
minus_bm = os.path.join(BITMAPS_PATH, 'minus.png')
weight_bm = os.path.join(BITMAPS_PATH, 'weight.png')

#  menu ids
id_new_patient = NewId()
id_edit_patient = NewId()
id_del_patient = NewId()
id_new_visit = NewId()
id_save_visit = NewId()

# some size
window_size = (1250, 690)
ma_bn_width = 50
bn_width = 250
gender_width = 50
ns_width = 100
date_width = 150
ma_lk_width = 130
days_size = (70, -1)
name_size = (bn_width, -1)
gender_size = (gender_width, -1)
bd_size = (ns_width, -1)
note_size = (-1, 60)
dose_size = (50, -1)
drugctrl_size = (200, -1)
popup_size = (700, 280, 280)
d_stt_w = 40
d_name_w = 150
d_l1cu_w = 80
d_socu_w = 60
d_tc_w = 80

tree_size = (400, 300)
add_edit_prescription_dialog_size = (-1, 600)


# DB_SETTING ------------------------------------------------------------
with open(os.path.join(SETTINGS_PATH, "db_setting.json"), "r") as f:
    db_setting = json.load(f)


SQLITE_PATH = os.path.join(DB_PATH, db_setting['sqlite_filename'])
egn = 'sqlite:///' + SQLITE_PATH
engine = create_engine(egn, echo=db_setting["echo"])
Session = sessionmaker(bind=engine)


def commit_(sess):
    def inner():
        try:
            sess.commit()
        except Exception as e:
            sess.rollback()
            print('sess rollback: ', e)
    return inner


def make_session():
    sess = Session()
    sess.commit_ = commit_(sess)
    return sess


# USER_SETTING ------------------------------------------------------------
with open(os.path.join(SETTINGS_PATH, "user_setting.json"), "r", encoding="utf-8-sig") as f:
    user_setting = json.load(f)


with open(os.path.join(SETTINGS_PATH, "setting.json"),
          "r", encoding="utf-8-sig") as f:
    setting = json.load(f)
