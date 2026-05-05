from core.repositories.booking_repository import BookingRepository
from core.repositories.service_repository import ServiceRepository
from core.repositories.user_repository import UserRepository
from core.models.booking_model import BookingModel
from datetime import datetime
from bson import ObjectId

class BookingService:
    @staticmethod
    def create_booking(customer_id, service_id, scheduled_date_str, notes=""):
        # Validate service
        service = ServiceRepository.find_by_id(service_id)
        if not service:
            return None, "Service not found"
        
        if service.get("provider_id") == customer_id:
            return None, "You cannot book your own service"

        # Validate customer
        customer = UserRepository.find_by_id(customer_id)
        if not customer:
            return None, "Customer not found"

        try:
            scheduled_date = datetime.fromisoformat(scheduled_date_str)
        except ValueError:
            return None, "Invalid date format. Use ISO format (YYYY-MM-DDTHH:MM:SS)"

        booking = BookingModel(
            service_id=service_id,
            service_title=service.get("title"),
            customer_id=customer_id,
            customer_name=customer.get("name"),
            provider_id=service.get("provider_id"),
            scheduled_date=scheduled_date,
            notes=notes
        )

        booking_id = BookingRepository.create(booking.to_dict())
        return booking_id, None

    @staticmethod
    def get_user_bookings(user_id, role):
        if role == "provider":
            bookings = BookingRepository.find_by_provider(user_id)
        else:
            bookings = BookingRepository.find_by_customer(user_id)
        
        for b in bookings:
            b["id"] = str(b.pop("_id"))
        return bookings

    @staticmethod
    def update_booking_status(booking_id, user_id, new_status):
        booking = BookingRepository.find_by_id(booking_id)
        if not booking:
            return False, "Booking not found"
        
        # Valid statuses
        valid_statuses = ["pending", "accepted", "rejected", "completed", "cancelled"]
        if new_status not in valid_statuses:
            return False, f"Invalid status. Must be one of: {valid_statuses}"

        # Permission check
        # Providers can accept/reject/complete
        # Customers can cancel
        is_provider = booking.get("provider_id") == user_id
        is_customer = booking.get("customer_id") == user_id

        if new_status in ["accepted", "rejected", "completed"] and not is_provider:
            return False, "Only providers can update status to accepted/rejected/completed"
        
        if new_status == "cancelled" and not (is_customer or is_provider):
            return False, "Only participants can cancel this booking"

        success = BookingRepository.update_status(booking_id, new_status)
        return success, None if success else "Update failed"
