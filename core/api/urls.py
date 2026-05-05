from django.urls import path
from .auth_views import RegisterView, LoginView, ProfileView
from .service_views import (
    ServiceListView, ServiceCreateView, ServiceDetailView, 
    ServiceFilterView, ServiceNearbyView
)
from .booking_views import BookingListCreateView, BookingStatusView

urlpatterns = [
    # Auth
    path("auth/register/", RegisterView.as_view(), name="register"),
    path("auth/login/", LoginView.as_view(), name="login"),
    path("auth/profile/", ProfileView.as_view(), name="profile"),

    # Services
    path("services/", ServiceListView.as_view(), name="service-list"),
    path("services/create/", ServiceCreateView.as_view(), name="service-create"),
    path("services/filter/", ServiceFilterView.as_view(), name="service-filter"),
    path("services/nearby/", ServiceNearbyView.as_view(), name="service-nearby"),
    path("services/<str:service_id>/", ServiceDetailView.as_view(), name="service-detail"),

    # Bookings
    path("bookings/", BookingListCreateView.as_view(), name="booking-list-create"),
    path("bookings/<str:booking_id>/status/", BookingStatusView.as_view(), name="booking-status"),
]
