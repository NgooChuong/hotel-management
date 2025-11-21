from fastapi_jwt_auth import AuthJWT

from app.core.db import SessionLocal
from app.core.config import settings

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



@AuthJWT.load_config
def get_config():
    return settings

