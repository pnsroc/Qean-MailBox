import os

class Settings:
    DB_URL = os.getenv("DB_URL", "postgresql+psycopg2://mail:mail@db:5432/maildb")
    SECRET_KEY = os.getenv("SECRET_KEY", "change-me")
    AES_KEY = os.getenv("AES_KEY", "16byteslongkey!!")  # 16/24/32 bytes

settings = Settings()
