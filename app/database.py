from pymongo import MongoClient

from dotenv import load_dotenv
import os
from .domain.markdict.markdict_schema import *


load_dotenv()
MONGO_USER = os.environ["MONGO_USER"]
MONGO_PWD = os.environ["MONGO_PWD"]
MONGO_HOST = os.environ["MONGO_HOST"]
MONGO_PORT = os.environ["MONGO_PORT"]

MONGO_DETAILS = f"mongodb://{MONGO_USER}:{MONGO_PWD}@{MONGO_HOST}:{MONGO_PORT}"

client = MongoClient(MONGO_DETAILS)
database = client.text_review
mark_dict_collection = database.get_collection("mark_dict")
user_collection = database.get_collection("user")
