import warnings
from contextlib import contextmanager
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

PG_DB_USER = "pguser"
PG_DB_PASS = "123123"
PG_DB_HOST = "localhost"
PG_DB_PORT = 5432
PG_DB_NAME = "test3db"

SQLALCHEMY_DATABASE_URL = "sqlite:///./sql.db"
# SQLALCHEMY_DATABASE_URL = 'mysql+pymysql://root:@localhost:3306/botdb'
# SQLALCHEMY_DATABASE_URL = f'postgresql+psycopg2://{PG_DB_USER}:{PG_DB_PASS}@{PG_DB_HOST}:{PG_DB_PORT}/{PG_DB_NAME}'

engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


@contextmanager
def get_db():
    db = SessionLocal()
    try:
        yield db
    except:
        warnings.warn("Xatolik yuz berdi va rollback qilib yuborildi")
        db.rollback()
        raise
    finally:
        db.close()
