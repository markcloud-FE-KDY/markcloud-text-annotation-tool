from fastapi import FastAPI
from app.domain.markdict.markdict_router import router as MarkdictRouter

app = FastAPI()
app.include_router(MarkdictRouter, tags=["Markdict"], prefix="/markdict")


@app.get("/", tags=["Root"])
def read_root():
    return {"messeage": "fastapi markdict"}
