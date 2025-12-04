from typing import List
from pydantic import Field
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DB_USERNAME: str
    DB_PASSWORD: str
    CLUSTER: str
    DB_NAME: str
    AUTH0_DOMAIN: str
    AUDIENCE: str = Field(alias="AUTH0_AUDIENCE")
    ISSUER: str | None = None
    ALGORITHMS: List[str] = ["RS256"]

    class Config:
        env_file = ".env"

settings = Settings()
settings.ISSUER = f"https://{settings.AUTH0_DOMAIN}/"
