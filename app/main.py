from fastapi import FastAPI
from app.domain.markdict.markdict_router import router as MarkdictRouter
from app.domain.user.user_router import router as UserRouter

app = FastAPI()
app.include_router(MarkdictRouter, tags=["Markdict"], prefix="/markdict")
app.include_router(UserRouter, tags=["User"])


@app.get("/", tags=["Root"])
def read_root():
    return {"messeage": "fastapi markdict"}
