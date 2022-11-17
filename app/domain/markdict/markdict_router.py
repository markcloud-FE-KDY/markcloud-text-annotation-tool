from fastapi import APIRouter, Body, HTTPException
from starlette import status

from app.database import *
from app.models import UpdateMarkDictModel

from typing import Optional

router = APIRouter()


@router.get("/")
def get_markdict_data(id: Optional[str] = None):
    markdict = retrieve_markdict(id)

    if not markdict:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    response = {
        "previous": retrieve_previous(id),
        "current": markdict,
        "next": retrieve_next(id),
    }
    return response


@router.post("/update")
def update_markdict_data(id: str, req: UpdateMarkDictModel = Body(...)):
    req = {k: v for k, v in req.dict().items() if v is not None}
    markdict = retrieve_markdict(id)
    if not markdict:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Data not found"
        )
    previousResult = markdict["modelResult"]

    update_modelResult(id, req)
    add_previousResult(id, previousResult)
    update_humanCheck(id)
    save_checklist(markdict["productNameEng"], req)
