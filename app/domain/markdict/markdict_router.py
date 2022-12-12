from fastapi import APIRouter, Body, HTTPException, Depends
from starlette import status

from app.database import *
from app.models import UpdateMarkDictModel, User
from app.domain.markdict.markdict_schema import *
from app.domain.markdict.markdict_crud import *
from app.domain.user.user_router import get_current_user

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
def update_markdict_data(
    oid: str, _pass: bool, req: UpdateMarkDictModel = Body(...), current_user: User = Depends(get_current_user)
):
    req = {k: v for k, v in req.dict().items() if v is not None}

    worker = current_user["username"]

    if _pass == True:
        add_pass_list(oid)
        return {"status": "pass"}

    markdict = retrieve_markdict(oid, req)

    if not markdict:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Data not found")

    modelResult = markdict["modelResult"]
    similarWords = markdict["similarWords"]

    user_input = req["userInput"]

    # 직접입력 공백제거, 콤마단위로 구분. 빈문자열 제외.
    user_input_list = [x.strip() for x in user_input.split(",") if x.strip()]

    inputFilter = ""

    # else:
    value = user_input_list[0]
    if value == modelResult:
        inputFilter = "model"

    elif value in similarWords:
        inputFilter = "candidate"

    else:
        inputFilter = "direct"

    update_db_directInput(oid, user_input_list, inputFilter, worker)
    update_cache_directInput(oid, user_input_list, inputFilter, worker)

    return {"status": "complete"}
