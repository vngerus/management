import pymysql
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config.database_config import DB_HOST, DB_USER, DB_PASSWORD, DB_CHARSET

def crear_base_datos():
    try:
        connection = pymysql.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            charset=DB_CHARSET
        )
        
        with connection.cursor() as cursor:
            with open('BDD/base.sql', 'r', encoding='utf-8') as file:
                sql_content = file.read()
            
            sql_commands = [cmd.strip() for cmd in sql_content.split(';') if cmd.strip()]
            
            for command in sql_commands:
                if command:
                    cursor.execute(command)
            
            connection.commit()
            print("Base de datos creada exitosamente!")
            
    except Exception as e:
        print(f"Error: {e}")
        print("Verifica que XAMPP esté corriendo")
        
    finally:
        if 'connection' in locals():
            connection.close()

if __name__ == "__main__":
    crear_base_datos()