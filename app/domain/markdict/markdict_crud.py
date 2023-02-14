from app.domain.markdict.markdict_schema import *
from app.database import *
from app.cache import *
from app.utils import *

from bson.objectid import ObjectId
import time


# markdictCache = MarkdictCache()


# 전체보기
def retrieve_markdict_list(m: MarkdictList, search_option: list):
    # 캐시 삭제
    # markdictCache.clear_cache()

    markdicts = []
    markdict_list = (
        (mark_dict_collection.find({"$and": search_option}))
        .sort([("dateModified", -1), ("_id", 1)])
        # .sort([("Check.passCheck", 1), ("dateModified", -1), ("_id", 1)])  # 보류 맨 뒤로
        .skip(m.page * m.size)
        .limit(m.size)
    )
    for idx, markdict in enumerate(markdict_list):
        markdicts.append(markdict_list_helper(idx + m.page * m.size + 1, markdict))
    return markdicts


# def add_cache(m: MarkdictList, search_option: str):
#     markdicts = []
#     markdict_list = (
#     (mark_dict_collection.find({"$and": search_option}))
#     .sort([("dateModified", -1), ("_id", 1)])
#     .skip(m.page * m.size)
#     .limit(m.size * 2)
#     )    
#     for markdict in markdict_list:
#         markdicts.append(markdict_detail_helper(markdict))
#     markdictCache.insert_data(markdicts)
    

# def add_prev_cache(m: MarkdictList, search_option: str):
#     markdicts = []
#     markdict_list = (
#     (mark_dict_collection.find({"$and": search_option}))
#     .sort([("dateModified", -1), ("_id", 1)])
#     .skip(m.page * m.size)
#     .limit(m.size * 2)
#     )    
#     for markdict in markdict_list:
#         markdicts.append(markdict_detail_helper(markdict))
#     markdictCache.insert_data_front(markdicts)
    
    
# current
# def retrieve_markdict(oid: str, m: MarkdictData) -> dict:
def retrieve_markdict(oid: str) -> dict:
    markdict = mark_dict_collection.find_one({"_id": ObjectId(oid)})
    if markdict:
        return markdict_detail_helper(markdict)
    return None

    """
    #### cache o
    # cache_hit = markdictCache.find_by_oid(oid)
    # if cache_hit:
    #     print(" C A C H E   H I T !")
    #     return cache_hit

    # print(f"{oid} is not in cache ")
    # # 캐시에 없을 경우 새로 추가.
    # search_option = form_search_option(m)

    # add_cache(m, search_option)
    # return markdictCache._cache[oid]
    
    """
    
    
# previous
def retrieve_previous(oid: str, m: MarkdictList):
    """
    # if not oid:
    #     print("not oid")
    #     return None
    # else:   
    #     search_option = form_search_option(m)
    #     search_option.append({"_id": {"$lt": ObjectId(oid)}})
        
    #     previous_data = list(
    #         mark_dict_collection
    #         .find({"$and": search_option})
    #         .sort("_id", -1)
    #         .limit(1)
    #         )
    """
    
    search_option = form_search_option(m)
    search_option.append({"_id": {"$lt": ObjectId(oid)}})
    
    previous_data = list(
        mark_dict_collection
        .find({"$and": search_option})
        .sort("_id", -1)
        .limit(1)
        )
    
    if previous_data:
        previous_data = previous_data[0]
        prev_oid = str(previous_data["_id"])
        return prev_oid
    else:
        return None
    
    """
    # #### cache o
    # curr_idx = markdictCache._cache_key_list.index(oid)
    
    # # 특정페이지의 가장 첫번째 데이터일 때
    # if curr_idx % m.size == 0:
        
    #     # 그 전값이 캐시에 있는지 확인
    #     if curr_idx > 0:
    #         prev_idx = curr_idx - 1
    #         prev_oid = markdictCache._cache_key_list[prev_idx]
    #         return prev_oid, True  
        
    #     # 캐시에 없으면 -> DB
    #     else:
    #         if m.page <= 0:
    #             return None, False
            
    #         m.page =  m.page - 1
    #         search_option = form_search_option(m)
    #         add_prev_cache(m, search_option)
            
    #         curr_idx = markdictCache._cache_key_list.index(oid)
    #         prev_idx = curr_idx - 1
    #         prev_oid = markdictCache._cache_key_list[prev_idx]
            
    #         return prev_oid, True
        
    # prev_idx = curr_idx - 1
    # prev_oid = markdictCache._cache_key_list[prev_idx]
    # return prev_oid, False
    """
    

# next
def retrieve_next(oid: str, m: MarkdictList):
    """
    # if not oid:
    #     next_data = list(mark_dict_collection.find({"humanCheck": False}).sort("_id", 1).skip(1).limit(1))[0]
    # else:
    #     search_option = form_search_option(m)
    #     search_option.append({"_id": {"$gt": ObjectId(oid)}})
    #     next_data = mark_dict_collection.find_one({"$and": search_option})
    
    """
    
    search_option = form_search_option(m)
    search_option.append({"_id": {"$gt": ObjectId(oid)}})
    
    next_data = mark_dict_collection.find_one({"$and": search_option})
    
    if next_data:
        next_oid = str(next_data["_id"])
        return next_oid
    else:
        return None
    
    """
    # #### cache o
    # curr_idx = markdictCache._cache_key_list.index(oid)
    
    # if (curr_idx+1)%m.size == 0:
    #     # 캐시에 있는지 확인
    #     if curr_idx+1 < len(markdictCache._cache_key_list):
    #         next_idx = curr_idx + 1
    #         next_oid = markdictCache._cache_key_list[next_idx]
    #         return next_oid, True
        
    #     # 캐시에 없으면 -> DB
    #     else:
    #         m.page = m.page + 1
    #         search_option = form_search_option(m)
    #         add_cache(m, search_option)
            
    #         next_idx = curr_idx + 1
    #         next_oid = markdictCache._cache_key_list[next_idx]
    #         return next_oid, True

    # if curr_idx+1 == len(markdictCache._cache_key_list):
    #     return None, False
    
    # next_idx = curr_idx + 1
    # next_oid = markdictCache._cache_key_list[next_idx]
    # return next_oid, False
    """
    


# projectCode ############################################################

def retrieve_prev_id(oid: str, search_option_prev: list):
    search_option_prev.append({"_id": {"$lt": ObjectId(oid)}})

    previous_data = mark_dict_collection.find_one({"$and": search_option_prev}, sort=[("_id", -1)])
    if previous_data:
        prev_oid = str(previous_data["_id"])
        return prev_oid
    else:
        return None
    

def retrieve_next_id(oid: str, search_option_next: list):
    search_option_next.append({"_id": {"$gt": ObjectId(oid)}})
    
    next_data = mark_dict_collection.find_one({"$and": search_option_next})
    if next_data:
        next_oid = str(next_data["_id"])
        return next_oid
    else:
        return None

##############################################################################

# Update
def update_db(oid: str, user_input_list: list, result_status: str, worker: str):
    oid = ObjectId(oid)
    mark_dict_collection.update_one(
        {"_id": oid},
        {
            "$set": {
                "dateModified": int(time.time()),
                "directInput": user_input_list,
                "Check.humanCheck": True,
                "Check.finalCheck": True if worker == "admin" else False,
                "Check.passCheck": False,
                "resultStatus": result_status,
                "worker": worker,
            }
        },
    )


# def update_cache(oid: str, user_input_list: list, input_filter: str, worker: str):
#     markdictCache._cache[oid]["humanCheck"] = True
#     markdictCache._cache[oid]["passCheck"] = False
#     markdictCache._cache[oid]["directInput"] = user_input_list
#     markdictCache._cache[oid]["resultStatus"] = input_filter
#     markdictCache._cache[oid]["worker"] = worker


# 보류(pass)
def add_pass_list(oid: str):
    # markdictCache._cache[oid]["passCheck"] = True
    oid = ObjectId(oid)
    mark_dict_collection.update_one({"_id": oid}, 
                                    {"$set": {"Check.passCheck": True}}
                                    )
