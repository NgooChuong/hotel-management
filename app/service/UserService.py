import base64
import hashlib
import os

from sqlalchemy.orm import Session

from app.crud.users import user_crud
from app.models.user import Users
from app.service.service import verify_odoo_password


class UserService:
    def register(self, db, username: str, password: str):
        if user_crud.get_by_username(db, username):
            raise ValueError("User already exists")

        iterations = 600000
        salt_bytes = os.urandom(16)  # bytes trực tiếp
        salt_b64 = base64.b64encode(salt_bytes).decode("utf-8")  # lưu base64 vào db

        dk = hashlib.pbkdf2_hmac(
            'sha512',
            password.encode('utf-8'),
            salt_bytes,  # dùng bytes trực tiếp
            iterations
        )

        password_hash = f"pbkdf2-sha512${iterations}${salt_b64}${base64.b64encode(dk).decode('utf-8')}"

        user = user_crud.create(db, username=username, password_hash=password_hash)
        return user

    def authenticate(self, db, username: str, password: str):
        user = user_crud.get_by_username(db, username)
        if not user:
            return None
        if verify_odoo_password(password, user.password):
            return user
        return None

    def get_user(self, db: Session, username: str):
        return user_crud.get_by_username(db, username)


user_service = UserService()


def get_user_service() -> UserService:
    return user_service
