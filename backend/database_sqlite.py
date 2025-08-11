import sqlite3
import logging
from pathlib import Path

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DatabaseManager:
    def __init__(self, db_path="chatbot.db"):
        self.db_path = db_path
        self.connection = None
        
    def connect(self):
        try:
            self.connection = sqlite3.connect(self.db_path, check_same_thread=False)
            self.connection.row_factory = sqlite3.Row  # This enables column access by name
            logger.info(f"Successfully connected to SQLite database: {self.db_path}")
            self.create_tables()
        except Exception as e:
            logger.error(f"Error while connecting to SQLite: {e}")
            
    def create_tables(self):
        try:
            cursor = self.connection.cursor()
            
            # Create conversations table
            create_conversations_table = """
            CREATE TABLE IF NOT EXISTS conversations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
            
            # Create messages table
            create_messages_table = """
            CREATE TABLE IF NOT EXISTS messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                conversation_id INTEGER,
                role TEXT NOT NULL CHECK (role IN ('user', 'assistant')),
                content TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (conversation_id) REFERENCES conversations(id)
            )
            """
            
            cursor.execute(create_conversations_table)
            cursor.execute(create_messages_table)
            self.connection.commit()    # commits the current transaction to the database
            logger.info("SQLite tables created successfully")   # write log to the Terminal
            
        except Exception as e:
            logger.error(f"Error creating tables: {e}")
            
    def save_message(self, conversation_id: int, role: str, content: str):
        try:
            cursor = self.connection.cursor()
            query = "INSERT INTO messages (conversation_id, role, content) VALUES (?, ?, ?)"
            cursor.execute(query, (conversation_id, role, content))
            self.connection.commit()
            return cursor.lastrowid
        except Exception as e:
            logger.error(f"Error saving message: {e}")
            return None
            
    def create_conversation(self, user_id: str):
        try:
            cursor = self.connection.cursor()
            query = "INSERT INTO conversations (user_id) VALUES (?)"
            cursor.execute(query, (user_id,))
            self.connection.commit()
            return cursor.lastrowid
        except Exception as e:
            logger.error(f"Error creating conversation: {e}")
            return None
            
    def get_conversation_history(self, conversation_id: int):
        try:
            cursor = self.connection.cursor()
            query = """
            SELECT role, content FROM messages 
            WHERE conversation_id = ? 
            ORDER BY created_at ASC
            """
            cursor.execute(query, (conversation_id,))
            return cursor.fetchall()
        except Exception as e:
            logger.error(f"Error fetching conversation history: {e}")
            return []
    
    def get_all_conversations(self, user_id: str):
        try:
            cursor = self.connection.cursor()
            query = """
            SELECT c.id, c.user_id, c.created_at,
                   COUNT(m.id) as message_count,
                   MAX(m.created_at) as last_message_at,
                   SUBSTR(MIN(CASE WHEN m.role = 'user' THEN m.content END), 1, 100) as preview
            FROM conversations c
            LEFT JOIN messages m ON c.id = m.conversation_id
            WHERE c.user_id = ?
            GROUP BY c.id, c.user_id, c.created_at
            ORDER BY COALESCE(MAX(m.created_at), c.created_at) DESC
            """
            cursor.execute(query, (user_id,))
            return cursor.fetchall()
        except Exception as e:
            logger.error(f"Error fetching all conversations: {e}")
            return []
    
    def get_conversation_with_messages(self, conversation_id: int):
        try:
            cursor = self.connection.cursor()
            
            # Get conversation details
            conv_query = """
            SELECT id, user_id, created_at FROM conversations WHERE id = ?
            """
            cursor.execute(conv_query, (conversation_id,))
            conversation = cursor.fetchone()
            
            if not conversation:
                return None
            
            # Get all messages for this conversation
            messages_query = """
            SELECT id, role, content, created_at FROM messages 
            WHERE conversation_id = ? 
            ORDER BY created_at ASC
            """
            cursor.execute(messages_query, (conversation_id,))
            messages = cursor.fetchall()
            
            return {
                'conversation': dict(conversation),
                'messages': [dict(msg) for msg in messages]
            }
        except Exception as e:
            logger.error(f"Error fetching conversation with messages: {e}")
            return None
    
    def delete_conversation(self, conversation_id: int):
        try:
            cursor = self.connection.cursor()
            
            # Delete all messages for this conversation first
            delete_messages_query = "DELETE FROM messages WHERE conversation_id = ?"
            cursor.execute(delete_messages_query, (conversation_id,))
            
            # Delete the conversation
            delete_conversation_query = "DELETE FROM conversations WHERE id = ?"
            cursor.execute(delete_conversation_query, (conversation_id,))
            
            self.connection.commit()
            
            # Return the number of rows affected
            return cursor.rowcount > 0
        except Exception as e:
            logger.error(f"Error deleting conversation: {e}")
            return False
            
    def close(self):
        if self.connection:
            self.connection.close()
            logger.info("SQLite connection closed")

db_manager = DatabaseManager()
