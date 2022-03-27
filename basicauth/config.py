import os

from dotenv import load_dotenv

load_dotenv(".env")


class Config:
    SECRET_KEY = os.getenv("QUART_SECRET")
    TOKEN_SECRET = os.getenv("TOKEN_SECRET")
    REFRESH_SECRET = os.getenv("REFRESH_SECRET")
    DATABASE = os.getenv("DATABASE")

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True


class ProductionConfig(Config):
    DEBUG = False


config = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
}
