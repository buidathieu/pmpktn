from db_sql.sampling import commit_population
from db_sql.make_db import make_db
from db_sql import sql_path
from mainview.gui import mainloop
import argparse
import os


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("-n", "--renew", action="store_true",
                    help="renew the db after changed")
    ap.add_argument("-s", "--sample", action="store_true",
                    help="sample 10 patients")
    args = vars(ap.parse_args())

    if args["renew"]:
        if os.path.exists(sql_path):
            os.remove(sql_path)
        make_db()
    if args["sample"]:
        if os.path.exists(sql_path):
            os.remove(sql_path)
        make_db()
        commit_population()
    if not any(args.values()):
        mainloop()
