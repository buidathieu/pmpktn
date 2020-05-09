from initialize import DIR_PATH
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
import os
from contextlib import contextmanager
import json


with open(os.path.join(DIR_PATH, "config.json"), "r", encoding="utf-8-sig") as f:
    setting = json.load(f)

username = setting['username']
password = setting['password']
host = setting['host']
port = setting['port']
db_name = setting['db_name']
gssencmode = setting['gssencmode']

engine = create_engine(
    f'postgresql://{username}:{password}@{host}:{port}/{db_name}?gssencmode={gssencmode}',
    echo=False)


Session = sessionmaker(bind=engine)


@contextmanager
def session_scope():
    """Provide a transactional scope around a series of operations."""
    session = Session()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()
