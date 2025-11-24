from passlib.context import CryptContext
from sqlalchemy.orm import Session
from sqlalchemy.util import deprecated
from sqlalchemy import or_

from domain.user.user_schema import UserCreate
from models import User

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def create_user(db: Session, user_create: UserCreate):
    db_user = User(username=user_create.username,
                   password=pwd_context.hash(user_create.password1),
                   email=user_create.email)
    db.add(db_user)
    db.commit()

def get_existing_user(db: Session, user_create: UserCreate):
    return db.query(User).filter(
        or_(
            User.username == user_create.username,
            User.email == user_create.email
        )
    ).first()

def get_user(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()

def create_user_oauth(db: Session, username: str, email: str):
    db_user = User(username=username, email=email, password="oauth")  # 비밀번호는 OAuth 사용자에 대해 의미 없음
    db.add(db_user)
    db.commit()