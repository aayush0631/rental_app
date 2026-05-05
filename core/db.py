from pymongo import MongoClient

# Connect to local MongoDB
client = MongoClient("mongodb://localhost:27017/")

# Your database
db = client["rental_app"]

users_collection = db["users"]
services_collection = db["services"]