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
        "similarWords": re.findall(r"'(.*?)'", markdict["similarWords"]) if "similarWords" in markdict else "",
        "humanCheck": bool(markdict["humanCheck"]),
    }


# Retrieve all markdicts(humanCheck:false) present in the database
def retrieve_markdicts():
    markdicts = []
    for markdict in mark_dict_collection.find({"humanCheck": False}):
        markdicts.append(markdict_helper(markdict))
    return markdicts


def retrieve_markdict(oid: Optional[str] = None) -> dict:
    if not oid:
        markdict = list(mark_dict_collection.find({"humanCheck": False}).sort("_id", 1).limit(1))[0]
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
        return markdict_helper(previous_data[0])


def retrieve_next(oid: Optional[str] = None) -> dict:
    if not oid:
        next_data = list(mark_dict_collection.find({"humanCheck": False}).sort("_id", 1).skip(1).limit(1))[0]
    else:
        next_data = mark_dict_collection.find_one({"_id": {"$gt": ObjectId(oid)}, "humanCheck": False})
    if next_data:
        return markdict_helper(next_data)


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


def save_checklist(productNameEng: str, data: dict):
    with open("result_txt/humancheck.csv", "a", encoding="utf-8-sig") as f:
        wr = csv.writer(f)
        dt = datetime.today().strftime("%Y%m%d")
        wr.writerow([dt, productNameEng, data["modelResult"]])
