import os
import mysql.connector
from dotenv import load_dotenv

load_dotenv()

def get_connection():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST", "localhost"),
        user=os.getenv("DB_USER", "root"),
        password=os.getenv("DB_PASSWORD", ""),
        database=os.getenv("DB_NAME", "mapua_findr")
    )

if __name__ == "__main__":
    try:
        conn = get_connection()
        if conn.is_connected():
            print("Successfully connected to mapua_findr database!")
            conn.close()
    except Exception as e:
        print(f"Connection failed: {e}")