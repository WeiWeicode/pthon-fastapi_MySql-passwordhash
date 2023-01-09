from pydantic import BaseModel


class User(BaseModel):
    # id: int
    account: str
    password: str
    name: str

    class Config:
        orm_mode = True

class UserPassword(BaseModel):
    password: str

    class Config:
        orm_mode = True

class UserAccPassword(BaseModel):
    account: str
    password: str

    class Config:
        orm_mode = True

class Userdelete(BaseModel):
    account: str

    class Config:
        orm_mode = True