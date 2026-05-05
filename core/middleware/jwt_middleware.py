from core.auth.jwt_handler import decode_token

class JWTMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        auth_header = request.headers.get("Authorization")
        request.user_data = None

        if auth_header and auth_header.startswith("Bearer "):
            token = auth_header.split(" ")[1]
            decoded = decode_token(token)
            if decoded:
                request.user_data = decoded

        response = self.get_response(request)
        return response
