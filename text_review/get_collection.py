from pymongo import MongoClient


def get_collection(db_name, collection_name):
    print("> call get_collection...")  #

    MONGO_USER = "mark-user"
    MONGO_PWD = "kwanadm2021"
    MONGO_HOST = "211.47.7.6"
    MONGO_PORT = 27017

    client = MongoClient(f"mongodb://{MONGO_USER}:{MONGO_PWD}@{MONGO_HOST}:{MONGO_PORT}")

    db = client[db_name]
    coll = db[collection_name]
    return coll


def get_updated_data(coll, start_date, end_date):
    print(f"> get_updated_data... {start_date}-{end_date}")  #

    updated_data = list(
        coll.find(
            {
                "_dataUpdateDate": {"$gte": start_date, "$lte": end_date},
                "productNameEng": {"$ne": None},
            },
            {"_id": 0, "productNameEng": 1},
        )
    )

    return updated_data


# mark_dict 컬렉션에서 productNameEng 불러오기 (humanCheck true인 것만)
def get_markdict_eng(coll):
    print("> get_markdict_eng...")

    datas = list(coll.find({"humanCheck": True}))
    src_eng = [data["productNameEng"] for data in datas]

    return src_eng
