# db name
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
import os
from contextlib import contextmanager

sqlfilename = "thankinhnhi.db"
sql_path = os.path.join(os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__)))), "sqlite", sqlfilename)
engine = create_engine('sqlite:///{}'.format(sql_path), echo=False)


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
