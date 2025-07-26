
import sqlite3
from database import create_connection, create_tables_from_dbml

def create_agent(name, description, base_prompt, dbml_schema):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO agents (name, description, base_prompt, dbml_schema) VALUES (?, ?, ?, ?)",
                   (name, description, base_prompt, dbml_schema))
    conn.commit()
    conn.close()
    create_tables_from_dbml(dbml_schema)

def list_agents():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM agents")
    agents = cursor.fetchall()
    conn.close()
    return agents

def get_agent(agent_id):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM agents WHERE id = ?", (agent_id,))
    agent = cursor.fetchone()
    conn.close()
    return agent

def edit_agent(agent_id, name=None, description=None, base_prompt=None, dbml_schema=None):
    conn = create_connection()
    cursor = conn.cursor()

    current_agent = get_agent(agent_id)
    if not current_agent:
        print(f"Agent with ID {agent_id} not found.")
        return

    # Use existing values if new ones are not provided
    name = name if name is not None else current_agent[1]
    description = description if description is not None else current_agent[2]
    base_prompt = base_prompt if base_prompt is not None else current_agent[3]
    dbml_schema = dbml_schema if dbml_schema is not None else current_agent[4]

    cursor.execute("""
        UPDATE agents
        SET name = ?,
            description = ?,
            base_prompt = ?,
            dbml_schema = ?
        WHERE id = ?
    """, (name, description, base_prompt, dbml_schema, agent_id))
    conn.commit()
    conn.close()
    create_tables_from_dbml(dbml_schema)
