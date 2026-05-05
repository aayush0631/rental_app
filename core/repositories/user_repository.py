from bson import ObjectId
from core.db import users_collection

class UserRepository:
    @staticmethod
    def create(user_data: dict) -> str:
        result = users_collection.insert_one(user_data)
        return str(result.inserted_id)

    @staticmethod
    def find_by_email(email: str) -> dict:
        return users_collection.find_one({"email": email})

    @staticmethod
    def find_by_id(user_id: str) -> dict:
        if not ObjectId.is_valid(user_id):
            return None
        return users_collection.find_one({"_id": ObjectId(user_id)})

    @staticmethod
    def update(user_id: str, data: dict) -> bool:
        if not ObjectId.is_valid(user_id):
            return False
        result = users_collection.update_one(
            {"_id": ObjectId(user_id)},
            {"$set": data}
        )
        return result.modified_count > 0
