from rest_framework.views import APIView
from core.services.booking_service import BookingService
from core.utils.response import api_response
from core.auth.permissions import login_required, customer_required
from django.utils.decorators import method_decorator

class BookingListCreateView(APIView):
    @method_decorator(login_required)
    def get(self, request):
        user_id = request.user_data["user_id"]
        role = request.user_data["role"]
        bookings = BookingService.get_user_bookings(user_id, role)
        return api_response(True, data=bookings)

    @method_decorator(customer_required)
    def post(self, request):
        customer_id = request.user_data["user_id"]
        data = request.data
        service_id = data.get("service_id")
        scheduled_date = data.get("scheduled_date")
        notes = data.get("notes", "")

        if not all([service_id, scheduled_date]):
            return api_response(False, message="service_id and scheduled_date are required", status_code=400)

        booking_id, error = BookingService.create_booking(customer_id, service_id, scheduled_date, notes)
        if error:
            return api_response(False, message=error, status_code=400)
        
        return api_response(True, data={"id": booking_id}, message="Booking created successfully", status_code=201)

class BookingStatusView(APIView):
    @method_decorator(login_required)
    def patch(self, request, booking_id):
        user_id = request.user_data["user_id"]
        new_status = request.data.get("status")

        if not new_status:
            return api_response(False, message="status is required", status_code=400)

        success, error = BookingService.update_booking_status(booking_id, user_id, new_status)
        if error:
            return api_response(False, message=error, status_code=400)
        
        return api_response(True, message=f"Booking status updated to {new_status}")
