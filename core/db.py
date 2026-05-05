import os
from pymongo import MongoClient
from decouple import config

MONGO_URI = config("MONGO_URI", default="mongodb://localhost:27017/")
MONGO_DB_NAME = config("MONGO_DB_NAME", default="smart_marketplace")

client = MongoClient(MONGO_URI)
db = client[MONGO_DB_NAME]

def get_db():
    return db

def get_collection(name):
    return db[name]

users_collection = db["users"]
services_collection = db["services"]
bookings_collection = db["bookings"]