from pydantic import BaseModel


class User(BaseModel):
    username: str
    password: str


class UpdateMarkDictModel(BaseModel):
    userInput: str


def ResponseModel(data, message):
    return {
        "data": [data],
        "code": 200,
        "message": message,
    }


def ErrorResponseModel(error, code, message):
    return {"error": error, "code": code, "message": message}
