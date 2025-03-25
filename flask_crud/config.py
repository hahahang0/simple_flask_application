import os 
from dotenv import load_dotenv 

load_dotenv()

class Config:
    MYSQL_HOST = os.getenv('MYSQL_HOST','localhost')
    MYSQL_USER = os.getenv('MYSQL_USER','root')
    MYSQL_PORT = int(os.getenv("MYSQL_PORT", 3310)) 
    MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD','hangtang@123L')
    MYSQL_DB = os.getenv('MYSQL_DB','flask_crud')
    MYSQL_CURSORCLASS = 'DictCursor'