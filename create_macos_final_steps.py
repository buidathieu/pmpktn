from initialize import SQLITE_PATH
import os
import zipfile
import shutil
import subprocess


cwd = os.getcwd()


# unzip

target = os.path.join(cwd, "dist", "Phần mềm phòng mạch tư.app", "Contents", "Resources", "lib", "python38.zip")

os.chdir(os.path.dirname(target))
zipped = zipfile.ZipFile(target)
zipped.extractall("unzipped")

os.rename(target, target + ".bak")
os.rename("unzipped", "python38.zip")

os.chdir(cwd)

# copy other

files = ['user_setting.json', 'setting.json', 'db_setting.json']
folders = ['bitmaps']

copy_dst = os.path.join(cwd, "dist", "Phần mềm phòng mạch tư.app", "Contents", "Resources", "lib", "python38.zip")

for f in files:
    shutil.copyfile(f, os.path.join(copy_dst, f))

for fol in folders:
    shutil.copytree(fol, os.path.join(copy_dst, fol))


# copy database
db_src = SQLITE_PATH
db_dst = os.path.join(cwd, "dist", "Phần mềm phòng mạch tư.app", "Contents", "Resources", "lib", "python38.zip", "database.db")

if os.path.isfile(db_dst):
    os.remove(db_dst)
if not os.path.isfile(db_src):
    subprocess.run(['python', 'main.py', '-c'])
shutil.copy(db_src, db_dst)
