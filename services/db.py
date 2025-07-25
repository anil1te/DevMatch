import mysql.connector
from mysql.connector import Error
from config.settings import DB_CONFIG

class Database:
    def __init__(self):
        self.connection = None
        self.connect()
    
    def connect(self):
        try:
            self.connection = mysql.connector.connect(**DB_CONFIG)
            print("Успешное подключение к базе данных")
        except Error as e:
            print(f"Ошибка подключения: {e}")
            raise
    
    async def check_user_exists(self, telegram_id: int) -> bool:
        query = "SELECT 1 FROM users WHERE telegram_id = %s"
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(query, (telegram_id,))
                return bool(cursor.fetchone())
        except Error as e:
            print(f"Ошибка проверки пользователя: {e}")
            return False
    
    async def add_user(self, user_data: dict) -> bool:
        query = """INSERT INTO users (
            telegram_id, username, country, city, age, 
            photo_url, descrip, skills, stack, banned
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, 0)"""
        
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(query, (
                    user_data['telegram_id'],
                    user_data['username'],
                    user_data['country'],
                    user_data['city'],
                    user_data['age'],
                    user_data.get('photo_url'),
                    user_data.get('descrip'),
                    user_data.get('skills'),
                    user_data.get('stack')
                ))
                self.connection.commit()
                return True
        except Error as e:
            print(f"Ошибка добавления пользователя: {e}")
            self.connection.rollback()
            return False
    
    async def is_banned(self, telegram_id: int) -> bool:
        query = "SELECT banned FROM users WHERE telegram_id = %s"
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(query, (telegram_id,))
                result = cursor.fetchone()
                return result[0] == 1 if result else False
        except Error as e:
            print(f"Ошибка проверки бана: {e}")
            return False

    async def get_user(self, telegram_id: int) -> dict | None:
        query = "SELECT * FROM users WHERE telegram_id = %s"
        try:
            with self.connection.cursor(dictionary=True) as cursor:
                cursor.execute(query, (telegram_id,))
                return cursor.fetchone()
        except Error as e:
            print(f"Ошибка получения пользователя: {e}")
            return None

db = Database()