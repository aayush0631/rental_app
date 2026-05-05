from functools import wraps
from core.utils.response import api_response

def login_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not hasattr(request, "user_data") or not request.user_data:
            return api_response(False, message="Authentication required", status_code=401)
        return view_func(request, *args, **kwargs)
    return _wrapped_view

def role_required(allowed_roles: list):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if not hasattr(request, "user_data") or not request.user_data:
                return api_response(False, message="Authentication required", status_code=401)
            
            user_role = request.user_data.get("role")
            if user_role not in allowed_roles:
                return api_response(False, message=f"Access denied. Required roles: {allowed_roles}", status_code=403)
            
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator

def provider_required(view_func):
    return role_required(["provider"])(view_func)

def customer_required(view_func):
    return role_required(["customer"])(view_func)
