import os
from dotenv import load_dotenv

load_dotenv()

# Database configuration
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_HOST = os.getenv('DB_HOST')
DB_DB = os.getenv('DB_DB')
DB_POOL_NAME = os.getenv('DB_POOL_NAME')
DB_POOL_SIZE = 20
DB_PORT=os.getenv('DB_PORT')

# Flask app configuration
DEBUG = os.getenv('DEBUG')
PORT = os.getenv('PORT')
HOST = os.getenv('HOST')
S3_BUCKET = os.getenv('S3_BUCKET')
S3_KEY_ID = os.getenv('S3_KEY_ID')
S3_SECRET_KEY = os.getenv('S3_SECRET_KEY')
S3_LOCATION = os.getenv('S3_LOCATION')
CLOUDFRONT = os.getenv('CLOUDFRONT')
