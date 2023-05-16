import pymongo
import os
import ujson
import datetime

from pymongo import MongoClient

files = os.listdir("grades")

x = []

for i in files:
    with open(f"grades/{i}", "r") as f:
        data = ujson.load(f)

        dupa = {}

        dupa = data[0]
        dupa["time"] = datetime.datetime.fromtimestamp(dupa["time"])

        x.append(dupa)

client = MongoClient("")
db = "bombunia_dev"

db = client.bombunia_dev.oceny

db.insert_many(x)
