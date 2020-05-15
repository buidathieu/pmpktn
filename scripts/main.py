from initialize import *
from db_sql.sampling import commit_population
from db_sql.make_db import make_db
from core.mainview import mainloop
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
            if input('Delete old database? [y]/n: ').lower() == 'y':
                os.remove(sql_path)
        make_db()
        print('A New database is created')

    if args["sample"]:
        if os.path.exists(sql_path):
            if input('This will delete old database, continue? [y]/n: ').lower() == 'y':
                os.remove(sql_path)
                make_db()
                commit_population()
                print('A new database is created with 10 patients')
        else:
            print('A database was not created')               
    if not any(args.values()):
        mainloop()
