from setuptools import setup

APP = ['main.py']
DATA_FILES = []
OPTIONS = {
    'argv_emulation': True,
    'site_packages': True,
    'iconfile': 'logo.icns',
    'packages': ['wx', 'sqlalchemy', 'core', 'database'],
    'plist': {
        'CFBundleName': 'Phần mềm phòng mạch tư',
        'CFBundleShortVersionString': '1.0.0',
        'CFBundleVersion': '1.0.0',
        'NSHumanReadableCopyright': '@ Bs Vuong Kien Thanh 2021',
    }
}
setup(
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)
