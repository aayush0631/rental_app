from bson import ObjectId
from core.db import services_collection

class ServiceRepository:
    @staticmethod
    def create(service_data: dict) -> str:
        result = services_collection.insert_one(service_data)
        return str(result.inserted_id)

    @staticmethod
    def find_all(skip: int = 0, limit: int = 20) -> list:
        return list(services_collection.find().skip(skip).limit(limit))

    @staticmethod
    def find_by_id(service_id: str) -> dict:
        if not ObjectId.is_valid(service_id):
            return None
        return services_collection.find_one({"_id": ObjectId(service_id)})

    @staticmethod
    def find_by_provider(provider_id: str) -> list:
        return list(services_collection.find({"provider_id": provider_id}))

    @staticmethod
    def update(service_id: str, data: dict) -> bool:
        if not ObjectId.is_valid(service_id):
            return False
        result = services_collection.update_one(
            {"_id": ObjectId(service_id)},
            {"$set": data}
        )
        return result.modified_count > 0

    @staticmethod
    def delete(service_id: str) -> bool:
        if not ObjectId.is_valid(service_id):
            return False
        result = services_collection.delete_one({"_id": ObjectId(service_id)})
        return result.deleted_count > 0

    @staticmethod
    def filter_services(query: dict, skip: int = 0, limit: int = 20) -> list:
        return list(services_collection.find(query).skip(skip).limit(limit))

    @staticmethod
    def find_nearby(lng: float, lat: float, max_distance_meters: int, skip: int = 0, limit: int = 20) -> list:
        query = {
            "location": {
                "$near": {
                    "$geometry": {
                        "type": "Point",
                        "coordinates": [lng, lat]
                    },
                    "$maxDistance": max_distance_meters
                }
            }
        }
        return list(services_collection.find(query).skip(skip).limit(limit))
