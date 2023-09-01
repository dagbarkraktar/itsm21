import os

from dotenv import load_dotenv


load_dotenv()

SECRET_KEY = os.environ.get('SECRET_KEY') or 'SOME_SECRET_KEY'
SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI') or ''
SQLALCHEMY_TRACK_MODIFICATIONS = False
REDIS_HOST = os.environ.get('REDIS_HOST') or ''
REDIS_PORT = os.environ.get('REDIS_PORT') or ''
