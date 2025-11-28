import pymysql
from pymysql.cursors import DictCursor
from config.database_config import DB_HOST, DB_USER, DB_PASSWORD, DB_NAME, DB_PORT, DB_CHARSET

class Database:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Database, cls).__new__(cls)
            try:
                cls._instance.connection = pymysql.connect(
                    host=DB_HOST,
                    user=DB_USER,
                    password=DB_PASSWORD,
                    database=DB_NAME,
                    port=DB_PORT,
                    cursorclass=DictCursor,
                    autocommit=True,
                    charset=DB_CHARSET
                )
            except Exception as e:
                print(f"Error conectando a BD: {e}")
                cls._instance.connection = None
        return cls._instance

    def get_connection(self):
        if self.connection:
            self.connection.ping(reconnect=True)
        return self.connection