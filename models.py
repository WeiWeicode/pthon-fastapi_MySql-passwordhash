from sqlalchemy import Column, Integer, String, create_engine

from database import Base, engine


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True)
    account = Column(String(255))
    password = Column(String(255))
    name = Column(String(255))





if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)


