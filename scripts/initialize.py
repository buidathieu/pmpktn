import os
import json
# High DPI aware
import ctypes
try:
    ctypes.windll.shcore.SetProcessDpiAwareness(True)
except Exception:
    pass
import logging
from wx import NewId
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine


# app structure
SCRIPTS_PATH = os.path.dirname(os.path.abspath(__file__))
DIR_PATH = os.path.dirname(SCRIPTS_PATH)
USER_FILES_PATH = os.path.join(DIR_PATH, "user_files")
FONTS_PATH = os.path.join(DIR_PATH, "fonts")
BITMAPS_PATH = os.path.join(DIR_PATH, 'bitmaps')

# logo
logo = os.path.join(USER_FILES_PATH, "logo.png")

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


gender_dict = {0: 'nam',
               1: 'nữ',
               'nam': 0,
               'nữ': 1}

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


with open(os.path.join(DIR_PATH, "db_setting.json"), "r") as f:
    db_setting = json.load(f)

if db_setting['use_postgres']:
    egn = 'postgresql://{}:{}@{}:{}/{}?gssencmode={}'.format(
        db_setting['username'],
        db_setting['password'],
        db_setting['host'],
        db_setting['port'],
        db_setting['db_name'],
        db_setting['gssencmode'])
else:
    SQLITE_PATH = os.path.join(DIR_PATH, db_setting['sqlite_filename'])
    egn = 'sqlite:///' + SQLITE_PATH
engine = create_engine(egn, echo=db_setting["echo"])
Session = sessionmaker(bind=engine)


def commit_(sess):
    try:
        sess.commit()
    except Exception as e:
        sess.rollback()
        print('sess rollback: ', e)


with open(os.path.join(DIR_PATH, "user_setting.json"), "r") as f:
    user_setting = json.load(f)


followup_choices = user_setting["followup_list"]
followup_choices.extend(list(user_setting["followup_dict"]))

with open(os.path.join(DIR_PATH, "setting.json"),
          "r", encoding="utf-8-sig") as f:
    setting = json.load(f)

dst = os.path.join(DIR_PATH, "debugging.log")
if setting["DEBUG"]:
    logging.basicConfig(filename=dst, level=logging.DEBUG)
