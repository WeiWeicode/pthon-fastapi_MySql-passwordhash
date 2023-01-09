from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker



SQL_URL = "mysql+pymysql://asdf0359:zxcv0359@192.168.68.60:3306/fastAPItest"

engine = create_engine(SQL_URL, echo=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()