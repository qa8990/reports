from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os, random, string

basedir = os.path.abspath(os.path.dirname(__file__))
print(basedir , "== basedir ")
SQLALCHEMY_DATABASE_URL = 'sqlite:///' + os.path.join(basedir, 'db.sqlite3')
# SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgresserver/db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()