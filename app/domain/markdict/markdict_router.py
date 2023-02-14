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
def markdict_list_search(m: MarkdictList = Depends(), current_user: User = Depends(get_current_user)):
    
    user_id = current_user["username"]
    search_option = assign_project(form_search_option(m), user_id)
    
    total = get_count(search_option)
    _markdict_list = retrieve_markdict_list(m, search_option)
    return {
        "meta": {
            "total": total, 
            "page": m.page, 
            "limit": m.size, 
            "page_count": math.ceil(total / m.size)
            },
        "data": _markdict_list,
    }


@router.get("/detail")
def get_markdict_data(oid: str, m: MarkdictList = Depends(), current_user: User = Depends(get_current_user)):
    try:
        user_id = current_user["username"]
        print("login :: [", user_id, "]")

        markdict = retrieve_markdict(oid)
        
        # assign project
        search_option = assign_project(form_search_option(m), user_id)
        
        # cache x & projectCode o
        prev_id = retrieve_prev_id(oid, search_option_prev=search_option[:])
        next_id = retrieve_next_id(oid, search_option_next=search_option[:])
        
        return {"previous": prev_id,
                "current": markdict,
                "next": next_id,
                }
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

    # markdict = retrieve_markdict(oid, req)
    markdict = retrieve_markdict(oid)

    if not markdict:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Data not found")

    modelResult = markdict["modelResult"]
    similarWords = markdict["similarWords"]
    
    user_input = req["userInput"]

    # 직접입력 공백제거, 콤마단위로 구분. 빈문자열 제외.
    user_input_list = [x.strip() for x in user_input.split(",") if x.strip()]

    resultStatus = ""

    value = user_input_list[0]
    if value == modelResult:
        resultStatus = "model"
    elif value in similarWords:
        resultStatus = "candidate"
    else:
        resultStatus = "direct"

    update_db(oid, user_input_list, resultStatus, worker)
    # update_cache(oid, user_input_list, resultStatus, worker)

    return {"status": "complete"}
