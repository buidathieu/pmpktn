# db name
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
# import os
from contextlib import contextmanager

name = 'postgres'
password = ''
host = 'localhost'
port = '5433'
db_name = 'pmpktn'
engine = create_engine(f'postgresql://{name}:{password}@{host}:{port}/{db_name}', echo=False)


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
