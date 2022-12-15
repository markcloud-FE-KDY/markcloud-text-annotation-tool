from passlib.context import CryptContext  # No module named passlib 에러
from app.domain.user.user_schema import UserCreate
from app.database import *

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def create_user(user_create: UserCreate):
    user_collection.insert_one(
        {
            "username": user_create.username,
            "password": pwd_context.hash(user_create.password),  # bcrypt 설치하기.=requirements.txt
        }
    )
    print("user created")


def get_user(username: str):
    return user_collection.find_one({"username": username})
