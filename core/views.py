from bson import ObjectId
from django.http import JsonResponse
from .db import db, users_collection,services_collection
import json
from django.contrib.auth.hashers import make_password, check_password
from django.views.decorators.csrf import csrf_exempt
import jwt
from django.conf import settings
from datetime import datetime, timedelta, timezone

now = datetime.now(timezone.utc)


# 🔹 Test Mongo
def test_mongo(request):
    collections = db.list_collection_names()
    return JsonResponse({
        "status": "success",
        "collections": collections
    })


# 🔹 Register
@csrf_exempt
def register_user(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            name = data.get("name")
            email = data.get("email")
            password = data.get("password")
            role = data.get("role", "customer")

            if not name or not email or not password:
                return JsonResponse({"status": "error", "message": "All fields are required."}, status=400)

            if users_collection.find_one({"email": email}):
                return JsonResponse({"status": "error", "message": "User already exists."}, status=400)

            users_collection.insert_one({
                "name": name,
                "email": email,
                "password": make_password(password),
                "role": role
            })

            return JsonResponse({"status": "success", "message": "User registered successfully."})

        except json.JSONDecodeError:
            return JsonResponse({"status": "error", "message": "Invalid JSON."}, status=400)

    return JsonResponse({"status": "error", "message": "Only POST allowed"}, status=405)


# 🔹 Login (NOW RETURNS JWT)
@csrf_exempt
def login_user(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            email = data.get("email")
            password = data.get("password")

            if not email or not password:
                return JsonResponse({"status": "error", "message": "Email and password required"}, status=400)

            user = users_collection.find_one({"email": email})

            if user and check_password(password, user["password"]):

                payload = {
                    "email": user["email"],
                    "role": user["role"],
                    "exp": now + timedelta(hours=1),
                    "iat": now
                }

                token = jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")

                return JsonResponse({
                    "status": "success",
                    "token": token
                })

            return JsonResponse({"status": "error", "message": "Invalid credentials"}, status=401)

        except json.JSONDecodeError:
            return JsonResponse({"status": "error", "message": "Invalid JSON"}, status=400)

    return JsonResponse({"status": "error", "message": "Only POST allowed"}, status=405)


# 🔹 Protected Route
def protected_view(request):
    auth_header = request.headers.get("Authorization")

    if not auth_header:
        return JsonResponse({"error": "No token provided"}, status=401)

    try:
        token = auth_header.split(" ")[1]
        decoded = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])

        return JsonResponse({
            "status": "success",
            "message": "Access granted",
            "user": decoded
        })

    except jwt.ExpiredSignatureError:
        return JsonResponse({"error": "Token expired"}, status=401)

    except jwt.InvalidTokenError:
        return JsonResponse({"error": "Invalid token"}, status=401)
    
@csrf_exempt
def create_service(request):
    if request.method == "POST":
        data = json.loads(request.body)

        service = {
            "title": data.get("title"),
            "category": data.get("category"),
            "provider_email": data.get("provider_email"),
            "price": data.get("price"),
            "description": data.get("description")
        }

        services_collection.insert_one(service)

        return JsonResponse({"message": "Service created"})

    return JsonResponse({"error": "POST required"})

def get_services(request):
    services = list(services_collection.find())

    for s in services:
        s["_id"] = str(s["_id"])  # fix ObjectId

    return JsonResponse(services, safe=False)

@csrf_exempt
def update_service(request, service_id):
    if request.method == "PUT":
        data = json.loads(request.body)

        services_collection.update_one(
            {"_id": ObjectId(service_id)},
            {"$set": data}
        )

        return JsonResponse({"message": "Service updated"})

    return JsonResponse({"error": "PUT required"})

@csrf_exempt
def delete_service(request, service_id):
    if request.method == "DELETE":
        services_collection.delete_one({"_id": ObjectId(service_id)})

        return JsonResponse({"message": "Service deleted"})

    return JsonResponse({"error": "DELETE required"})