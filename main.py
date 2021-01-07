from core.main_view import MainView
from core.db.make_db import make_db
from core.db.sampling import populate_db
from initialize import SQLITE_PATH

import wx

import argparse
import os


def mainloop():
    app = wx.App()
    MainView(None).Show()
    app.MainLoop()


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("-c", "--create", action="store_true",
                    help="create database")
    ap.add_argument("-p", "--populate", action="store_true",
                    help="populate sample database")
    ap.add_argument("-d", "--delete", action="store_true",
                    help="delete")
    args = ap.parse_args()
    if args.create:
        if os.path.exists(SQLITE_PATH):
            print('Database existed, couldnt create a new one')
        else:
            make_db()
            print('New database created')
    elif args.populate:
        populate_db()
        print('Database populated')
    elif args.delete:
        if os.path.exists(SQLITE_PATH):
            os.remove(SQLITE_PATH)
        print('Database deleted')
    else:
        if not os.path.exists(SQLITE_PATH):
            make_db()
        mainloop()
