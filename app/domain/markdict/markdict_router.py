from fastapi import APIRouter, Body, HTTPException, Depends
from starlette import status

from app.database import *
from app.models import UpdateMarkDictModel
from app.domain.markdict.markdict_schema import *
from app.domain.markdict.markdict_crud import *

import math


router = APIRouter()


@router.get("/list_search")
def markdict_list_search(s: MarkdictList = Depends()):
    search_option = form_search_option(s)
    total = get_count(search_option)
    _markdict_list = retrieve_markdict_list(s, search_option)
    return {
        "meta": {"total": total, "page": s.page, "limit": s.size, "page_count": math.ceil(total / s.size)},
        "data": _markdict_list,
    }


@router.get("/detail")
def get_markdict_data(oid: str, m: MarkdictData = Depends()):
    try:
        markdict = retrieve_markdict(oid, m)
        if not markdict:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        return {"previous": retrieve_previous(oid, m), "current": markdict, "next": retrieve_next(oid, m)}
    except:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)


@router.post("/update")
def update_markdict_data(oid: str, _pass: bool, req: UpdateMarkDictModel = Body(...)):
    req = {k: v for k, v in req.dict().items() if v is not None}

    if _pass == True:
        print("pass clicked.")
        add_pass_list(oid)
        return {"status": "pass"}

    markdict = retrieve_markdict(oid, req)

    if not markdict:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Data not found")

    previousResult = markdict["modelResult"]
    modelResult = req["modelResult"]

    update_db(oid, modelResult, previousResult)
    update_cache(oid, modelResult, previousResult)

    return {"status": "complete"}
