from initialize import SQLITE_PATH, DIR_PATH
import os
import zipfile
import shutil
import subprocess


cwd = os.getcwd()


# unzip
try:
    target = os.path.join(cwd, "dist", "Phần mềm phòng mạch tư.app", "Contents", "Resources", "lib", "python38.zip")
    os.chdir(os.path.dirname(target))
    zipped = zipfile.ZipFile(target)
    zipped.extractall("unzipped")
    zipped.close()
    os.remove(target)
    os.rename("unzipped", "python38.zip")
    os.chdir(cwd)
except:
    pass

print(cwd)
# copy other

files = ['user_setting.json', 'setting.json', 'db_setting.json']
folders = [
    ('core', 'bitmaps')
]

copy_dst = os.path.join(cwd, "dist", "Phần mềm phòng mạch tư.app", "Contents", "Resources", "lib", "python38.zip", "settings")
try:
    os.mkdir(copy_dst)
except:
    pass
for f in files:
    print(f"{f} copied")
    shutil.copyfile(os.path.join(cwd, 'settings', f), os.path.join(copy_dst, f))

for fol in folders:
    print(f"{fol} copied")
    copy_dst = os.path.join(cwd, "dist", "Phần mềm phòng mạch tư.app", "Contents", "Resources", "lib", "python38.zip", *fol)
    # for i in range(len(fol)):
    #     copy_dst = os.path.join(copy_dst, fol[i])
    #     os.mkdir(copy_dst)
    shutil.copytree(os.path.join(DIR_PATH, *fol), copy_dst)


# copy database
db_src = SQLITE_PATH
db_dst = os.path.join(cwd, "dist", "Phần mềm phòng mạch tư.app", "Contents", "Resources", "lib", "python38.zip", "database.db")

if os.path.isfile(db_dst):
    print('removed file db in dst')
    os.remove(db_dst)
if not os.path.isfile(db_src):
    print("db src not found, create new")
    subprocess.run(['python', 'main.py', '-c'])
shutil.copy(db_src, db_dst)


# delete build folder
shutil.rmtree(os.path.join(cwd, "build"))
