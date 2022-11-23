from fastapi import APIRouter, Body, HTTPException
from starlette import status

from app.database import *
from app.models import UpdateMarkDictModel

from typing import Optional
import math

router = APIRouter()


@router.get("/list")
def markdict_list(page: int = 0, size: int = 20, tf: int = 0, keyword: str = ""):
    total, _markdict_list = retrieve_markdict_list(skip=page * size, limit=size, tf=tf, keyword=keyword)
    return {
        "meta": {"total": total, "page": page, "limit": size, "page_count": math.ceil(total / size)},
        "data": _markdict_list,
    }


@router.get("/")
def get_markdict_data(oid: Optional[str] = None):
    markdict = retrieve_markdict(oid)

    if not markdict:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    return {
        "previous": retrieve_previous(oid),
        "current": markdict,
        "next": retrieve_next(oid),
    }


@router.post("/update")
def update_markdict_data(oid: str, req: UpdateMarkDictModel = Body(...)):
    req = {k: v for k, v in req.dict().items() if v is not None}
    markdict = retrieve_markdict(oid)
    if not markdict:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Data not found")
    previousResult = markdict["modelResult"]

    update_modelResult(oid, req)
    add_previousResult(oid, previousResult)
    update_humanCheck(oid)
    add_date_modified(oid)
