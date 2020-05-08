import os
import json
import logging
# High DPI aware
import ctypes
try:
    ctypes.windll.shcore.SetProcessDpiAwareness(True)
except Exception:
    pass


SCRIPTS_PATH = os.path.dirname(os.path.abspath(__file__))
DIR_PATH = os.path.dirname(SCRIPTS_PATH)

# logo_path
logo = os.path.join(DIR_PATH, "logo.png")

# fonts_path
fonts = os.path.join(DIR_PATH, "fonts")

# BM_PATH_paths
BM_PATH = os.path.join(DIR_PATH, 'bitmaps')

new_p_bm = os.path.join(BM_PATH, 'new_patient.png')
del_p_bm = os.path.join(BM_PATH, 'delete_patient.png')

save_drug_bm = os.path.join(BM_PATH, 'save_drug.png')
erase_drug_bm = os.path.join(BM_PATH, 'erase_drug.png')

new_visit_bm = os.path.join(BM_PATH, 'new_visit.png')
save_visit_bm = os.path.join(BM_PATH, 'save_visit.png')
del_visit_bm = os.path.join(BM_PATH, 'del_visit.png')

print_bm = os.path.join(BM_PATH, 'print.png')
refresh_bm = os.path.join(BM_PATH, 'refresh.png')

plus_bm = os.path.join(BM_PATH, 'plus.png')
pencil_bm = os.path.join(BM_PATH, 'pencil.png')
minus_bm = os.path.join(BM_PATH, 'minus.png')

weight_bm = os.path.join(BM_PATH, 'weight.png')

# excel path
default_exlpath = os.path.join(DIR_PATH, "excel")


with open(os.path.join(DIR_PATH, "setting.json"), "r", encoding="utf-8-sig") as f:
    setting = json.load(f)
    
with open(os.path.join(DIR_PATH, 'config.json'), 'r') as f:
    DEBUG = json.load(f)['DEBUG']
    if DEBUG:
        logging.basicConfig(level=logging.DEBUG)
