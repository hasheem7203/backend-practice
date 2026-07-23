import os 
from psycopg2 import pool
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")


connection_pool=pool.SimpleConnectionPool(1,10,DATABASE_URL)

def get_connection():
    return connection_pool.getconn()

def put_connection(conn):
    return connection_pool.putconn(conn)

