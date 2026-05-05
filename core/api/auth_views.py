from rest_framework.views import APIView
from core.services.auth_service import AuthService
from core.utils.response import api_response
from core.auth.permissions import login_required
from django.utils.decorators import method_decorator

class RegisterView(APIView):
    def post(self, request):
        data = request.data
        name = data.get("name")
        email = data.get("email")
        password = data.get("password")
        role = data.get("role", "customer")
        phone = data.get("phone")

        if not all([name, email, password]):
            return api_response(False, message="Name, email, and password are required", status_code=400)

        result, error = AuthService.register_user(name, email, password, role, phone)
        if error:
            return api_response(False, message=error, status_code=400)
        
        return api_response(True, data=result, message="Registration successful", status_code=201)

class LoginView(APIView):
    def post(self, request):
        data = request.data
        email = data.get("email")
        password = data.get("password")

        if not all([email, password]):
            return api_response(False, message="Email and password are required", status_code=400)

        result, error = AuthService.login_user(email, password)
        if error:
            return api_response(False, message=error, status_code=401)
        
        return api_response(True, data=result, message="Login successful")

class ProfileView(APIView):
    @method_decorator(login_required)
    def get(self, request):
        user_id = request.user_data["user_id"]
        profile, error = AuthService.get_user_profile(user_id)
        if error:
            return api_response(False, message=error, status_code=404)
        return api_response(True, data=profile)
