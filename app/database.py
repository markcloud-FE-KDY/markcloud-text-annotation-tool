from pymongo import MongoClient
import re
from bson.objectid import ObjectId
from typing import Optional
from dotenv import load_dotenv
import os
import time

load_dotenv()
MONGO_USER = os.environ["MONGO_USER"]
MONGO_PWD = os.environ["MONGO_PWD"]
MONGO_HOST = os.environ["MONGO_HOST"]
MONGO_PORT = os.environ["MONGO_PORT"]

MONGO_DETAILS = f"mongodb://{MONGO_USER}:{MONGO_PWD}@{MONGO_HOST}:{MONGO_PORT}"

client = MongoClient(MONGO_DETAILS)
database = client.text_review
mark_dict_collection = database.get_collection("mark_dict")


def markdict_helper(markdict) -> dict:
    return {
        "id": str(markdict["_id"]),
        "productNameEng": str(markdict["productNameEng"]),
        "modelResult": str(markdict["modelResult"]),
        "similarWords": re.findall(r"'(.*?)'", markdict["similarWords"]) if "similarWords" in markdict else "",
        "originalEng": re.findall(r"'(.*?)'", markdict["originalEng"]) if "originalEng" in markdict else "",
        "humanCheck": bool(markdict["humanCheck"]),
    }


def retrieve_markdict_list(skip: int = 0, limit: int = 20, tf: int = 0, keyword: str = ""):
    markdicts = []
    reg = re.compile(r"[a-zA-Z]")
    rgx = re.compile(f".*{keyword}.*", re.IGNORECASE)
    if reg.match(keyword):
        filter_keyword = {"productNameEng": rgx}
    else:
        filter_keyword = {"modelResult": rgx}
    filter_tf = {0: {"humanCheck": False}, 1: {"humanCheck": True}, 2: {}}
    total = mark_dict_collection.count_documents({"$and": [filter_keyword, filter_tf[tf]]})
    markdict_list = list(
        mark_dict_collection.find({"$and": [filter_keyword, filter_tf[tf]]}).sort("_id", 1).skip(skip).limit(limit)
    )
    for markdict in markdict_list:
        markdicts.append(markdict_helper(markdict))
    return total, markdicts


def retrieve_markdict(oid: Optional[str] = None) -> dict:
    if not oid:
        markdict = list(mark_dict_collection.find().sort("_id", 1).limit(1))[0]
    else:
        markdict = mark_dict_collection.find_one({"_id": ObjectId(oid)})
    if markdict:
        return markdict_helper(markdict)


def retrieve_previous(oid: Optional[str] = None) -> dict:
    if not oid:
        return None
    previous_data = list(
        mark_dict_collection.find({"_id": {"$lt": ObjectId(oid)}, "humanCheck": False}).sort("_id", -1).limit(1)
    )
    if previous_data:
        return str(previous_data[0]["_id"])


def retrieve_next(oid: Optional[str] = None) -> dict:
    if not oid:
        next_data = list(mark_dict_collection.find({"humanCheck": False}).sort("_id", 1).skip(1).limit(1))[0]
    else:
        next_data = mark_dict_collection.find_one({"_id": {"$gt": ObjectId(oid)}, "humanCheck": False})
    if next_data:
        return str(next_data["_id"])


# Update
def update_modelResult(oid: str, data: dict):
    if len(data) < 1:
        return False
    oid = ObjectId(oid)
    mark_dict_collection.update_one(
        {"_id": oid},
        {"$set": data},
    )


def update_humanCheck(oid: str):
    oid = ObjectId(oid)
    mark_dict_collection.update_one({"_id": oid}, {"$set": {"humanCheck": True}})


def add_previousResult(oid: str, previousResult: str):
    oid = ObjectId(oid)
    mark_dict_collection.update_one(
        {"_id": oid},
        {"$set": {"previousResult": previousResult}},
    )


def add_date_modified(oid: str):
    oid = ObjectId(oid)
    mark_dict_collection.update_one({"_id": oid}, {"$set": {"date_modified": int(time.time())}})
