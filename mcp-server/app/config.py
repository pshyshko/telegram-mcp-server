from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings



class ServiceSettings(BaseSettings):
    service_name: str = Field("aw-bot-service")
    environment: str = Field("DEV")
    telegram_token: str = Field()
    
    notification_chat_id_telegram: str = Field()
    notification_bot_telegram_token: str = Field()

    dashboard_admin_user: str = Field()
    dashboard_admin_password: str = Field()

    secret_key: str = Field()
    algorithm: str = "HS256"

    database_url: str = Field("")


@lru_cache
def get_settings():
    return ServiceSettings()


service_settings = get_settings()