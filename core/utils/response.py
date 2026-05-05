from rest_framework.response import Response

def api_response(success: bool, data=None, message: str = "", status_code: int = 200):
    """
    Consistent JSON response format for Flutter frontend.
    """
    return Response(
        {
            "success": success,
            "data": data,
            "message": message
        },
        status=status_code
    )
