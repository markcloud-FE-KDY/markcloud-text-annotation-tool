from app.domain.markdict.markdict_schema import *
from app.database import *
from app.cache import *
from app.utils import *

from bson.objectid import ObjectId
import time


markdictCache = MarkdictCache()


# 전체보기
def retrieve_markdict_list(m: MarkdictList, search_option: list):
    # 캐시 삭제
    markdictCache.clear_cache()

    markdicts = []
    # markdict_list = (
    #     (mark_dict_collection.find({"$and": search_option})).sort("_id", 1).skip(m.page * m.size).limit(m.size)
    # )
    markdict_list = (
        (mark_dict_collection.find({"$and": search_option}))
        .sort([("date_modified", -1), ("_id", 1)])
        .skip(m.page * m.size)
        .limit(m.size)
    )
    for idx, markdict in enumerate(markdict_list):
        markdicts.append(markdict_list_helper(idx + m.page * m.size + 1, markdict))
    return markdicts


# 캐시에 값이 없을 때 db에서 캐시에 새로 넣을 데이터를 가져오는 함수.
def retrieve_markdict_list_range(search_option: str, sort_order: int):
    markdicts = []
    # search 조건을 만족하는(+oid보다 큰/작은 값들 중에) RANGE_CNT개 가져오기.
    markdict_list = mark_dict_collection.find({"$and": search_option}).sort("_id", sort_order).limit(RANGE_CNT)
    # markdict_list = mark_dict_collection.find({"$and": search_option}).sort("date_modified", sort_order).limit(RANGE_CNT)
    for markdict in markdict_list:
        markdicts.append(markdict_detail_helper(markdict))
    return markdicts


# 함수이름 바꾸기
def get_range_and_add_to_cache(oid: str, search_option: str, query_option: str):
    if query_option == "gte":
        option_gte = [{"_id": {"$gte": ObjectId(oid)}}]
        markdicts = retrieve_markdict_list_range(search_option + option_gte, 1)
        return markdictCache.insert_data(markdicts)

    else:
        option_lt = [{"_id": {"$lte": ObjectId(oid)}}]
        markdicts = retrieve_markdict_list_range(search_option + option_lt, -1)
        return markdictCache.insert_data(markdicts)


# current
def retrieve_markdict(oid: str, m: MarkdictData) -> dict:
    cache_hit = markdictCache.find_by_oid(oid)
    if cache_hit:
        print(" C A C H E   H I T !")
        print(cache_hit)
        return cache_hit

    print(f"{oid} is not in cache ")
    # 캐시에 없을 경우 새로 추가.
    search_option = form_search_option(m)
    get_range_and_add_to_cache(oid, search_option, "gte")
    get_range_and_add_to_cache(oid, search_option, "lte")

    markdictCache._cache_key_list.sort()
    return markdictCache._cache[oid]


# previous
def retrieve_previous(oid: str, m: MarkdictData):
    curr_idx = markdictCache._cache_key_list.index(oid)
    if curr_idx == 0:
        search_option = form_search_option(m)
        result = get_range_and_add_to_cache(oid, search_option, "lte")
        if not result:
            return None

    prev_idx = curr_idx - 1
    prev_oid = markdictCache._cache_key_list[prev_idx]
    return prev_oid


# next
def retrieve_next(oid: str, m: MarkdictData):
    curr_idx = markdictCache._cache_key_list.index(oid)
    if curr_idx == len(markdictCache._cache_key_list) - 1:
        search_option = form_search_option(m)
        result = get_range_and_add_to_cache(oid, search_option, "gte")
        if not result:
            return None

    next_idx = curr_idx + 1
    next_oid = markdictCache._cache_key_list[next_idx]
    return next_oid


# Update cache
def update_cache(oid: str, modelResult: str, previousResult: str):
    markdictCache._cache[oid]["modelResult"] = modelResult
    markdictCache._cache[oid]["humanCheck"] = True
    markdictCache._cache[oid]["passCheck"] = False
    markdictCache._cache[oid]["previousResult"] = previousResult


# Update database
def update_db(oid: str, modelResult: str, previousResult: str):
    oid = ObjectId(oid)
    mark_dict_collection.update_one(
        {"_id": oid},
        {
            "$set": {
                "modelResult": modelResult,
                "previousResult": previousResult,
                "date_modified": int(time.time()),
                "humanCheck": True,
                "passCheck": False,
            }
        },
    )


# 보류(pass)
def add_pass_list(oid: str):
    markdictCache._cache[oid]["passCheck"] = True
    oid = ObjectId(oid)
    mark_dict_collection.update_one({"_id": oid}, {"$set": {"passCheck": True}})
