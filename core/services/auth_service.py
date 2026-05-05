import bcrypt
from core.repositories.user_repository import UserRepository
from core.models.user_model import UserModel
from core.auth.jwt_handler import generate_access_token

class AuthService:
    @staticmethod
    def register_user(name, email, password, role="customer", phone=None):
        # Check if user already exists
        if UserRepository.find_by_email(email):
            return None, "Email already registered"

        # Hash password
        hashed_pw = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        
        user = UserModel(
            name=name,
            email=email,
            password=hashed_pw,
            role=role,
            phone=phone
        )
        
        user_id = UserRepository.create(user.to_dict())
        token = generate_access_token(user_id, email, role)
        
        user_data = user.to_dict()
        user_data.pop("password")
        user_data["id"] = user_id
        
        return {"token": token, "user": user_data}, None

    @staticmethod
    def login_user(email, password):
        user_dict = UserRepository.find_by_email(email)
        if not user_dict:
            return None, "Invalid email or password"

        if not bcrypt.checkpw(password.encode('utf-8'), user_dict["password"].encode('utf-8')):
            return None, "Invalid email or password"

        user_id = str(user_dict["_id"])
        role = user_dict["role"]
        token = generate_access_token(user_id, email, role)
        
        user_dict.pop("password")
        user_dict["id"] = user_id
        user_dict.pop("_id")
        
        return {"token": token, "user": user_dict}, None

    @staticmethod
    def get_user_profile(user_id):
        user_dict = UserRepository.find_by_id(user_id)
        if not user_dict:
            return None, "User not found"
        
        user_dict.pop("password")
        user_dict["id"] = str(user_dict.pop("_id"))
        return user_dict, None
