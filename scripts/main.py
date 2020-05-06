from db_sql.sampling import commit_population
from db_sql.make_db import make_db, drop_db
from core.gui import mainloop
import argparse


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("-n", "--new", action="store_true",
                    help="make a new db")
    ap.add_argument("-s", "--sample", action="store_true",
                    help="sample 10 patients")
    args = vars(ap.parse_args())

    if args['new']:
        drop_db()
        make_db()
    if args["sample"]:
        commit_population()
    if not any(args.values()):
        mainloop()
