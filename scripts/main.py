from db_sql.sampling import commit_population
from db_sql.make_db import make_db, drop_db
from log_in_dialog.log_in_dialog import LogInDialog
from core.main_view import MainView
from nurse_view.nurse_view import NurseView

import wx

import argparse


def mainloop():
    app = wx.App()
    with LogInDialog(None) as dlg:
        if dlg.ShowModal() == wx.ID_OK:
            dlg.save_staff_workday()
            job = dlg.get_staff_job()
    if job == 'Doctor':
        MainView(None).Show()
    elif job == 'Nurse':
        NurseView(None).Show()
    else:
        quit()

    app.MainLoop()


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("-n", "--new", action="store_true",
                    help="make a new db")
    ap.add_argument("-s", "--sample", action="store_true",
                    help="sample 10 patients")
    ap.add_argument("-tpdf", "--testpdf", action="store_true",
                    help="make test pdf")
    args = vars(ap.parse_args())

    if args['new']:
        drop_db()
        make_db()
    if args["sample"]:
        commit_population()
    if args["testpdf"]:
        from print_func import test
    if not any(args.values()):
        mainloop()
