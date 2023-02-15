import re
from app.domain.markdict.markdict_schema import *
from app.database import *

RANGE_CNT = 20


def markdict_list_helper(idx: int, markdict: dict) -> dict:
    return {
        "index": idx,
        "id": str(markdict["_id"]),
        "productNameEng": markdict["productNameEng"],
        "modelResult": markdict["modelResult"],
        "originalEng": markdict["originalEng"],
        "worker": markdict["worker"],
        "dateModified": markdict["dateModified"],
        "finalCheck": markdict["Check"]["finalCheck"],
        "humanCheck": markdict["Check"]["humanCheck"],
        "passCheck": markdict["Check"]["passCheck"],
        "directInput": markdict["directInput"],
        "resultStatus": markdict["resultStatus"]
    }


def markdict_detail_helper(markdict: dict) -> dict:
    return {
        "id": str(markdict["_id"]),
        "productNameEng": markdict["productNameEng"],
        "modelResult": markdict["modelResult"],
        "similarWords": markdict["similarWords"],
        "originalEng": markdict["originalEng"],
        "worker": markdict["worker"],
        "dateModified": markdict["dateModified"],
        "finalCheck": markdict["Check"]["finalCheck"],
        "humanCheck": markdict["Check"]["humanCheck"],
        "passCheck": markdict["Check"]["passCheck"],
        "directInput": markdict["directInput"],
        "resultStatus": markdict["resultStatus"]
    }


def search_by_keyword(keyword: str):
    reg = re.compile(r"[a-zA-Z]")
    rgx = re.compile(f".*{keyword}.*", re.IGNORECASE)
    if reg.match(keyword):
        filter_keyword = {"productNameEng": rgx}
    else:
        filter_keyword = {"modelResult": rgx}
    return filter_keyword


def search_by_worker(worker: str):
    rgx = re.compile(f".*{worker}.*", re.IGNORECASE)
    filter_worker = {"worker": rgx}
    return filter_worker


def search_by_time(time_start: int, time_end: int):
    filter_time = {"dateModified": {"$gte": time_start, "$lte": time_end}}
    return filter_time


def form_search_option(m: MarkdictList):
    filter_tf = {
        0: {"Check.humanCheck": False},
        1: {"Check.humanCheck": True},
        2: {"Check.humanCheck": True},
        3: {"Check.humanCheck": True},
        4: {"Check.humanCheck": True},
        5: {"Check.passCheck": True},
        6: {},
    }

    search_option = [filter_tf[m.tf]]

    if m.tf == 0:
        search_option.append({"Check.passCheck":False})
    
    # if m.tf in [1,2,3,4]:
    #     search_option.append({"Check.finalCheck":False})
    if m.tf == 2:
        search_option.append({"resultStatus": "model"})
    if m.tf == 3:
        search_option.append({"resultStatus": "candidate"})
    if m.tf == 4:
        search_option.append({"resultStatus": "direct"})

    if m.keyword:
        search_option.append(search_by_keyword(m.keyword))
    if m.worker:
        search_option.append(search_by_worker(m.worker))
    if m.date_start:
        search_option.append(search_by_time(m.date_start, m.date_end))
    return search_option


def assign_project(search_option:list, user_id:str):
    prj = {
        "work1": 1,
        "work2": 2,
        "work3": 3
    }
    if user_id not in prj:
        return search_option
    search_option.append({"projectCode":prj[user_id]})
    return search_option


def get_count(search_option: list):
    total = mark_dict_collection.count_documents({"$and": search_option})
    return total
