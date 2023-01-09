# uvicorn main:app  --reload --host 0.0.0.0 --port 8000
# 用IP方式架設

from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
import hashlib
from sqlalchemy.orm import Session

from database import SessionLocal
import models
import schemas


app = FastAPI()

origins = [
    "*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def main():
    return {"message": "Hello World"}


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/user/")
def create_user(user: schemas.User, db: Session = Depends(get_db)):
    # db_user = models.User()
    # db_user.password = hashlib.new("md5", user.password.encode()).hexdigest()
    # db_user.account, db_user.name = user.account, user.name
    # db.add(db_user)
    # db.commit()
    # db.refresh(db_user)

    # 判斷帳號是否重複
    db_useracc = db.query(models.User).filter(models.User.account == user.account).first()
    if db_useracc:
        return {
            'error': '帳號重複',
        }
    else:
        db_user = models.User()
        db_user.password = hashlib.new("md5", user.password.encode()).hexdigest()
        db_user.account, db_user.name = user.account, user.name
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return {
            'error': '成功',
            'id': db_user.id,
            'account': db_user.account,

        }
    

@app.get("/user/")
def get_user(db: Session = Depends(get_db)):
    # 取得使用者資料
    db_user = db.query(models.User).all()
    return db_user

@app.post("/user/check")
# body傳送帳號與密碼進行比對
def usercheckacc(user: schemas.UserAccPassword, db: Session = Depends(get_db)):
    # 取得使用者資料
    db_user = db.query(models.User).filter(models.User.account == user.account).first()
    if db_user:
        if hashlib.new("md5", user.password.encode()).hexdigest() == db_user.password:
            return {
                '狀態':'登入成功',
                'id': db_user.id,
                'account': db_user.account,
            }
        else:
            return {
                '狀態':'password 錯誤',
                'id': db_user.id,
                'account': db_user.account,
            }
    else:
        return {
            'error': 1,
            'data': 'user not found',
        }

@app.patch("/user/updatepassword")
# body傳送帳號進行比對，並更新密碼
def userupdate(user: schemas.User, db: Session = Depends(get_db)):
    # 取得使用者資料
    db_user = db.query(models.User).filter(models.User.account == user.account).first()
    # 判斷輸入name與資料庫是否相同,相同則更新password,name為空值則更新password,password為空值則更新name,皆不同則更新password與name
    if db_user:
        if user.name == db_user.name:
            db_user.password = hashlib.new("md5", user.password.encode()).hexdigest()
            db.commit()
            return {
                '狀態': '密碼更新成功',
            }
        elif user.name == "":
            db_user.password = hashlib.new("md5", user.password.encode()).hexdigest()
            db.commit()
            return {
                '狀態': '密碼更新成功',
            }
        elif user.password == "":
            db_user.name = user.name
            db.commit()
            return {
                '狀態': '名稱更新成功',
            }
        else:
            db_user.password = hashlib.new("md5", user.password.encode()).hexdigest()
            db_user.name = user.name
            db.commit()
            return {
                '狀態': '帳號與名稱更新成功',
            }


@app.delete("/user/delete")
# body傳送帳號進行比對，並刪除帳號
def userdelete(user: schemas.User, db: Session = Depends(get_db)):
    # 取得使用者資料
    db_user = db.query(models.User).filter(models.User.account == user.account).first()
    if db_user:
        db.delete(db_user)
        db.commit()
        return {
            '狀態': '刪除成功',
        }
    else:
        return {
            '狀態': '刪除失敗',
        }

@app.delete("/user/delete/{user_id}")
# 進行id比對，並刪除帳號
def userdeleteid(user_id: int, db: Session = Depends(get_db)):
    # 取得使用者資料
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if db_user:
        db.delete(db_user)
        db.commit()
        return {
            '狀態': '刪除成功',
        }
    else:
        return {
            '狀態': '刪除失敗',
        }

# 測試get user password hash轉換
@app.post("/user/{user_id}")
# body傳送密碼比對密碼
def usercheckid(user_id: int, user: schemas.UserPassword, db: Session = Depends(get_db)):
    # 取得使用者資料
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if db_user:
        if hashlib.new("md5", user.password.encode()).hexdigest() == db_user.password:
            return {
                '狀態':'登入成功',
            }
        else:
            return {
                '狀態':'password 錯誤',
            }
    else:
        return {
            'error': 1,
            'data': 'user not found',
        }

