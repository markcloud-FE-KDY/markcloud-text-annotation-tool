from pymongo import MongoClient
import re
import csv
from datetime import datetime
from bson.objectid import ObjectId
from typing import Optional
from dotenv import load_dotenv
import os

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
        "similarWords": re.findall(r"'(.*?)'", markdict["similarWords"])
        if "similarWords" in markdict
        else "",
        "humanCheck": bool(markdict["humanCheck"]),
    }


# Retrieve all markdicts(humanCheck:false) present in the database
def retrieve_markdicts():
    markdicts = []
    for markdict in mark_dict_collection.find({"humanCheck": False}):
        markdicts.append(markdict_helper(markdict))
    return markdicts


# Retrieve
# def retrieve_markdict(productNameEng: str) -> dict:
#     markdict = mark_dict_collection.find_one({"productNameEng": productNameEng})
#     if markdict:
#         return markdict_helper(markdict)


def retrieve_markdict(id: Optional[str] = None) -> dict:
    if not id:
        markdict = list(
            mark_dict_collection.find({"humanCheck": False}).sort("_id", 1).limit(1)
        )[0]
    else:
        markdict = mark_dict_collection.find_one({"_id": ObjectId(id)})
    if markdict:
        return markdict_helper(markdict)


def retrieve_previous(id: Optional[str] = None) -> dict:
    if not id:
        return None
    previous = list(
        mark_dict_collection.find({"_id": {"$lt": ObjectId(id)}, "humanCheck": False})
        .sort("_id", -1)
        .limit(1)
    )
    if previous:
        return markdict_helper(previous[0])


def retrieve_next(id: Optional[str] = None) -> dict:
    if not id:
        next = list(
            mark_dict_collection.find({"humanCheck": False})
            .sort("_id", 1)
            .skip(1)
            .limit(1)
        )[0]
    else:
        next = mark_dict_collection.find_one(
            {"_id": {"$gt": ObjectId(id)}, "humanCheck": False}
        )
    if next:
        return markdict_helper(next)


# Update
def update_modelResult(id: str, data: dict):
    if len(data) < 1:
        return False
    id = ObjectId(id)
    mark_dict_collection.update_one(
        {"_id": id},
        {"$set": data},
    )


def update_humanCheck(id: str):
    id = ObjectId(id)
    mark_dict_collection.update_one({"_id": id}, {"$set": {"humanCheck": True}})


def add_previousResult(id: str, previousResult: str):
    id = ObjectId(id)
    mark_dict_collection.update_one(
        {"_id": id},
        {"$set": {"previousResult": previousResult}},
    )


def save_checklist(productNameEng: str, data: dict):
    with open("result_txt/humancheck.csv", "a", encoding="utf-8-sig") as f:
        wr = csv.writer(f)
        dt = datetime.today().strftime("%Y%m%d")
        wr.writerow([dt, productNameEng, data["modelResult"]])
