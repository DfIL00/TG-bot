import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'bot_database.db')

class Database:
    def __init__(self):
        self.conn = sqlite3.connect(DB_PATH, check_same_thread=False)
        self.cursor = self.conn.cursor()
        self._create_tables()

    def _create_tables(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS sessions (
            id_session INTEGER PRIMARY KEY AUTOINCREMENT,
            id_chat_user INTEGER NOT NULL,
            request_user_data TEXT,
            id_key_chat TEXT)''')
        self.conn.commit()

    def add_session(self, chat_id: int, request: str, key: str = 'default'):
        self.cursor.execute('''INSERT INTO sessions 
                            (id_chat_user, request_user_data, id_key_chat)
                            VALUES (?, ?, ?)''', (chat_id, request, key))
        self.conn.commit()

    def get_sessions(self, chat_id: int):
        self.cursor.execute('SELECT * FROM sessions WHERE id_chat_user = ?', (chat_id,))
        return self.cursor.fetchall()

    def close(self):
        self.conn.close()