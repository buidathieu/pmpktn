from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

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
    name="Phần mềm phòng mạch tư",
    version="1.0",
    author="Vương Kiến Thanh",
    author_email="thanhstardust@outlook.com",
    description="Phần mềm phòng mạch tư miễn phí, sử dụng sqlite và wxpython",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/vuongkienthanh/pmpktn",
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
)
