import hashlib, base64
from fastapi import Depends, HTTPException
from fastapi_jwt_auth import AuthJWT
from starlette import status


def verify_odoo_password(password: str, stored_hash: str) -> bool:
    try:
        algo, iterations, salt_b64, hash_db = stored_hash.split('$')
        iterations = int(iterations)
        # decode base64 -> bytes gốc
        salt_bytes = base64.b64decode(salt_b64 + '=' * (-len(salt_b64) % 4))

        dk = hashlib.pbkdf2_hmac(
            'sha512',
            password.encode('utf-8'),
            salt_bytes,
            iterations
        )
        computed_hash = base64.b64encode(dk).decode('utf-8')
        return computed_hash == hash_db
    except Exception as e:
        print("Error verify password:", e)
        return False


def require_access_token(Authorize: AuthJWT = Depends()):
    try:
        Authorize.jwt_required()
        current_user = Authorize.get_jwt_subject()
        return current_user
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))