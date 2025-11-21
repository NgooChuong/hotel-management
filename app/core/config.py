from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    POSTGRES_SERVER: str
    POSTGRES_PORT: str
    POSTGRES_DB: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    authjwt_secret_key: str
    authjwt_access_token_expires: int = 15 * 60
    authjwt_refresh_token_expires: int = 60 * 60 * 24 * 7

    class Config:
        env_file = "../.env"


settings = Settings()

#
# @AuthJWT.load_config
# def get_config():
#     return settings
