from db_sql.sampling import commit_population
from db_sql.make_db import make_db, drop_db
from log_in_dialog import LogInDialog
from core.main_view import MainView
from nurse_view import NurseView
import wx

import argparse


def mainloop():
    app = wx.App()
    with LogInDialog(None) as dlg:
        ans = dlg.ShowModal()
        staff_id = dlg.staff.id
        job = dlg.staff.job
    if ans == wx.ID_OK:
        if job == "Doctor":
            MainView(None, staff_id=staff_id).Show()
        elif job == "Nurse":
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
    ap.add_argument("-ex", "--exportdrug", action="store_true",
                    help="export drugwarehouse")
    ap.add_argument("-im", "--importdrug", action="store_true",
                    help="import drugwarehouse")
    args = vars(ap.parse_args())

    if args['new']:
        drop_db()
        make_db()
    if args["sample"]:
        commit_population()
    if args["exportdrug"]:
        from db_sql.drugwarehouse_exim import export_drug
        export_drug()
    if args["importdrug"]:
        from db_sql.drugwarehouse_exim import import_drug
        import_drug()
    if not any(args.values()):
        mainloop()
