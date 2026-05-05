from core.repositories.service_repository import ServiceRepository
from core.models.service_model import ServiceModel, Location
from core.repositories.user_repository import UserRepository
from bson import ObjectId

class ServiceService:
    @staticmethod
    def create_service(provider_id, data):
        provider = UserRepository.find_by_id(provider_id)
        if not provider:
            return None, "Provider not found"

        location_data = data.get("location", {})
        location = Location(
            type="Point",
            coordinates=location_data.get("coordinates", [0.0, 0.0])
        )

        service = ServiceModel(
            title=data.get("title"),
            description=data.get("description"),
            category=data.get("category"),
            price=float(data.get("price", 0)),
            provider_id=provider_id,
            provider_name=provider.get("name"),
            address=data.get("address", ""),
            location=location
        )

        service_id = ServiceRepository.create(service.to_dict())
        return service_id, None

    @staticmethod
    def get_all_services(page=1, limit=20):
        skip = (page - 1) * limit
        services = ServiceRepository.find_all(skip=skip, limit=limit)
        for s in services:
            s["id"] = str(s.pop("_id"))
        return services

    @staticmethod
    def get_service_by_id(service_id):
        service = ServiceRepository.find_by_id(service_id)
        if not service:
            return None, "Service not found"
        service["id"] = str(service.pop("_id"))
        return service, None

    @staticmethod
    def update_service(service_id, provider_id, data):
        service = ServiceRepository.find_by_id(service_id)
        if not service:
            return False, "Service not found"
        
        if service.get("provider_id") != provider_id:
            return False, "Unauthorized: You do not own this service"

        # Handle location update if present
        if "location" in data:
            loc_data = data.pop("location")
            data["location"] = {
                "type": "Point",
                "coordinates": loc_data.get("coordinates", service["location"]["coordinates"])
            }

        success = ServiceRepository.update(service_id, data)
        return success, None if success else "Update failed"

    @staticmethod
    def delete_service(service_id, provider_id):
        service = ServiceRepository.find_by_id(service_id)
        if not service:
            return False, "Service not found"
        
        if service.get("provider_id") != provider_id:
            return False, "Unauthorized: You do not own this service"

        success = ServiceRepository.delete(service_id)
        return success, None if success else "Delete failed"

    @staticmethod
    def filter_services(category=None, min_price=None, max_price=None, search=None, page=1, limit=20):
        query = {"is_active": True}
        if category:
            query["category"] = category
        
        if min_price is not None or max_price is not None:
            price_query = {}
            if min_price is not None:
                price_query["$gte"] = float(min_price)
            if max_price is not None:
                price_query["$lte"] = float(max_price)
            query["price"] = price_query

        if search:
            query["$or"] = [
                {"title": {"$regex": search, "$options": "i"}},
                {"description": {"$regex": search, "$options": "i"}}
            ]

        skip = (page - 1) * limit
        services = ServiceRepository.filter_services(query, skip, limit)
        for s in services:
            s["id"] = str(s.pop("_id"))
        return services

    @staticmethod
    def search_nearby(lng, lat, radius_meters=5000, page=1, limit=20):
        skip = (page - 1) * limit
        services = ServiceRepository.find_nearby(lng, lat, radius_meters, skip, limit)
        for s in services:
            s["id"] = str(s.pop("_id"))
        return services
