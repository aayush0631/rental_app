from django import views
from django.urls import path
from .views import create_service, delete_service, get_services, login_user, protected_view, register_user, test_mongo, update_service

urlpatterns = [
    path("test-mongo/", test_mongo),
    path("register/", register_user),
    path("login/", login_user),
    path('protected/', protected_view)
]

urlpatterns += [
    path("services/", get_services),
    path("services/create/", create_service),
    path("services/update/<str:service_id>/", update_service),
    path("services/delete/<str:service_id>/", delete_service),
]