import os


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'SOME_SECRET_KEY'
    STUB_URI = 'postgresql+psycopg2://user:pass@127.0.0.1:5432/itsm21'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI') or STUB_URI
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    REDIS_HOST = '192.168.10.210'
    REDIS_PORT = '6379'
