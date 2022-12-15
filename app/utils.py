import re
from app.domain.markdict.markdict_schema import *
from app.database import *

RANGE_CNT = 20


def split_originalEng_list(s):
    delimiter = "', '"
    d1 = "\", '"
    d2 = "', \""
    result = s[2:-2].replace(d1, delimiter).replace(d2, delimiter).split(delimiter)
    return result


def markdict_list_helper(idx: int, markdict: dict) -> dict:
    tmp = markdict["directInput"]
    if isinstance(tmp, list):
        markdict["directInput"] = tmp[0]
        pass
    else:
        markdict["directInput"] = []
        
    return {
        "index": idx,
        "id": str(markdict["_id"]),
        "productNameEng": markdict["productNameEng"],
        "modelResult": markdict["modelResult"],
        "originalEng": split_originalEng_list(markdict["originalEng"])[0],
        "worker": markdict["worker"] if "worker" in markdict else "",
        "date_modified": markdict["date_modified"],
        "finalCheck": markdict["finalCheck"],
        "humanCheck": markdict["humanCheck"],
        "passCheck": markdict["passCheck"],
        "directInput": markdict["directInput"] if "directInput" in markdict else "",
        "inputFilter": markdict["inputFilter"] if "inputFilter" in markdict else "",
    }


def markdict_detail_helper(markdict: dict) -> dict:
    tmp = markdict["directInput"]
    if isinstance(tmp, str):
        markdict["directInput"] = []
    return {
        "id": str(markdict["_id"]),
        "productNameEng": markdict["productNameEng"],
        "modelResult": markdict["modelResult"],
        "similarWords": re.findall(r"'(.*?)'", markdict["similarWords"]) if "similarWords" in markdict else "",
        "originalEng": split_originalEng_list(markdict["originalEng"]),
        "passCheck": markdict["passCheck"] if "passCheck" in markdict else "",
        "humanCheck": markdict["humanCheck"],
        "directInput": markdict["directInput"] if "directInput" in markdict else "",
        "inputFilter": markdict["inputFilter"] if "inputFilter" in markdict else "",
        "worker": markdict["worker"] if "worker" in markdict else "",
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
    filter_time = {"date_modified": {"$gte": time_start, "$lte": time_end}}
    return filter_time


def form_search_option(m: MarkdictList):
    filter_tf = {
        0: {"humanCheck": False},
        1: {"humanCheck": True},
        2: {"humanCheck": True},
        3: {"humanCheck": True},
        4: {"humanCheck": True},
        5: {"passCheck": True},
        6: {},
    }

    search_option = [filter_tf[m.tf]]

    if m.tf == 2:
        search_option.append({"inputFilter": "model"})
    if m.tf == 3:
        search_option.append({"inputFilter": "candidate"})
    if m.tf == 4:
        search_option.append({"inputFilter": "direct"})
    # 코드 개선할 수 있는지 생각해보기.

    if m.keyword:
        search_option.append(search_by_keyword(m.keyword))
    if m.worker:
        search_option.append(search_by_worker(m.worker))
    if m.date_start:
        search_option.append(search_by_time(m.date_start, m.date_end))
    return search_option


def get_count(search_option: list):
    total = mark_dict_collection.count_documents({"$and": search_option})
    return total
