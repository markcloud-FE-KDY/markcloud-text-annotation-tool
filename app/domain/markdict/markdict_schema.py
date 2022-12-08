from pydantic import BaseModel
from typing import Optional

DATE_END = 1922072400


class MarkdictData(BaseModel):
    tf: int = 0
    keyword: Optional[str] = None
    worker: Optional[str] = None
    date_start: Optional[int] = 0
    date_end: Optional[int] = DATE_END


class MarkdictList(MarkdictData):
    page: int = 0
    size: int = 20
