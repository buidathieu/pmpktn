import os
import json
# High DPI aware
import ctypes
try:
    ctypes.windll.shcore.SetProcessDpiAwareness(True)
except Exception:
    pass


scripts_path = os.path.dirname(os.path.abspath(__file__))
dir_path = os.path.dirname(scripts_path)

# bm_path_paths
bm_path = os.path.join(dir_path, 'bitmaps')

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


# excel path
default_exlpath = os.path.join(dir_path, "excel")


with open(os.path.join(scripts_path, "setting.json"), "r", encoding="utf-8-sig") as f:
    setting = json.load(f)
