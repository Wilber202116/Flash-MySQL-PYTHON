import os
import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv

load_dotenv(dotenv_path=".env")

def get_db():
    try:
        # Configuracion = cfg
        cfg = {
            "host" : os.environ["DB_HOST"] ,
            "user" : os.environ["DB_USER"],
            "password" : os.environ["PASSWORD"],
            "database" : os.environ["DB_NAME"],
            "port" : int(os.environ["DB_PORT"]),
        }

        # Conexion a mysql
        conn = mysql.connector.connect(**cfg)
        if conn.is_connected():
            print("conexion establecida a sql")
            return conn
        
    except Error as e:
        print("Error al conectarse: ", e)
        return None