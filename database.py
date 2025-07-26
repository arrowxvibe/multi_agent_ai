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

def create_tables_from_dbml(dbml_schema):
    conn = create_connection()
    cursor = conn.cursor()

    # Regex to find table definitions
    table_pattern = re.compile(r'Table\s+(\w+)\s*\{([^}]+)\}', re.DOTALL)
    # Regex to find column definitions within a table
    column_pattern = re.compile(r'(\w+)\s+(\w+)(?:\s+\[([^\]]+)\])?')

    tables = table_pattern.findall(dbml_schema)

    for table_name, columns_str in tables:
        columns = []
        for match in column_pattern.finditer(columns_str):
            col_name, col_type, col_constraints = match.groups()
            sqlite_type = col_type.upper() # Simple type mapping
            constraints = []

            if col_constraints:
                if 'primary key' in col_constraints:
                    constraints.append('PRIMARY KEY')
                if 'not null' in col_constraints:
                    constraints.append('NOT NULL')
                if 'unique' in col_constraints:
                    constraints.append('UNIQUE')
                if 'default:' in col_constraints:
                    default_val = re.search(r'default:\s*([^,\]]+)', col_constraints)
                    if default_val: # Add quotes for text defaults
                        if col_type.lower() in ['varchar', 'text']:
                            constraints.append(f"DEFAULT '{default_val.group(1).strip()}'")
                        else:
                            constraints.append(f"DEFAULT {default_val.group(1).strip()}")
                if 'auto_increment' in col_constraints:
                    constraints.append('AUTOINCREMENT')

            columns.append(f"{col_name} {sqlite_type} {' '.join(constraints)}".strip())
        
        # Add foreign key constraints separately after all columns are processed
        fk_pattern = re.compile(r'(\w+)\s+\w+\s+\[ref:\s*([<>])\s*(\w+)\.(\w+)\]')
        for match in fk_pattern.finditer(columns_str):
            local_col, direction, remote_table, remote_col = match.groups()
            # SQLite only supports REFERENCES, not direction indicators like <> 
            columns.append(f"FOREIGN KEY ({local_col}) REFERENCES {remote_table}({remote_col})")

        create_table_sql = f"CREATE TABLE IF NOT EXISTS {table_name} ({', '.join(columns)})"
        try:
            cursor.execute(create_table_sql)
            conn.commit()
            print(f"Table {table_name} created/verified.")
        except sqlite3.Error as e:
            print(f"Error creating table {table_name}: {e}")
            conn.rollback()

    conn.close()

if __name__ == '__main__':
    create_tables()