from bson import ObjectId
from core.db import bookings_collection

class BookingRepository:
    @staticmethod
    def create(booking_data: dict) -> str:
        result = bookings_collection.insert_one(booking_data)
        return str(result.inserted_id)

    @staticmethod
    def find_by_id(booking_id: str) -> dict:
        if not ObjectId.is_valid(booking_id):
            return None
        return bookings_collection.find_one({"_id": ObjectId(booking_id)})

    @staticmethod
    def find_by_customer(customer_id: str) -> list:
        return list(bookings_collection.find({"customer_id": customer_id}).sort("created_at", -1))

    @staticmethod
    def find_by_provider(provider_id: str) -> list:
        return list(bookings_collection.find({"provider_id": provider_id}).sort("created_at", -1))

    @staticmethod
    def update_status(booking_id: str, status: str) -> bool:
        if not ObjectId.is_valid(booking_id):
            return False
        result = bookings_collection.update_one(
            {"_id": ObjectId(booking_id)},
            {"$set": {"status": status, "updated_at": ObjectId().generation_time}} # Simplified timestamp for update
        )
        return result.modified_count > 0

    @staticmethod
    def update(booking_id: str, data: dict) -> bool:
        if not ObjectId.is_valid(booking_id):
            return False
        result = bookings_collection.update_one(
            {"_id": ObjectId(booking_id)},
            {"$set": data}
        )
        return result.modified_count > 0
