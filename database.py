import sqlite3
import re

def create_connection():
    conn = sqlite3.connect('/Users/manoj/multi_agent_ai/agents.db')
    return conn

def create_tables():
    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS agents (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,
            description TEXT,
            base_prompt TEXT,
            dbml_schema TEXT
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS conversation_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            agent_id INTEGER,
            user_query TEXT,
            generated_sql TEXT,
            reasoning TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (agent_id) REFERENCES agents (id)
        )
    ''')

    conn.commit()
    conn.close()

def execute_sql_schema(sql_schema):
    conn = create_connection()
    cursor = conn.cursor()
    try:
        cursor.executescript(sql_schema)
        conn.commit()
        print("Schema SQL executed successfully.")
    except sqlite3.Error as e:
        print(f"Error executing schema SQL: {e}")
        conn.rollback()
    conn.close()

if __name__ == '__main__':
    create_tables()