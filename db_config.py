# db_config.py
import mysql.connector
import env # type: ignore

def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password=env.password, 
        database="contact_db"
    )
