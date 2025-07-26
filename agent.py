
import sqlite3
import ollama
from database import create_connection, execute_sql_schema
from config import OLLAMA_MODEL

def generate_sql_schema(data_model_description):
    with open('/Users/manoj/multi_agent_ai/schema_generation_prompt.txt', 'r') as f:
        prompt_template = f.read()
    prompt = prompt_template.format(data_model_description=data_model_description)

    response = ollama.generate(
        model=OLLAMA_MODEL,
        prompt=prompt
    )
    return response['response'].strip()

def create_agent(name, description, base_prompt, data_model_description):
    generated_sql_schema = generate_sql_schema(data_model_description)
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO agents (name, description, base_prompt, dbml_schema) VALUES (?, ?, ?, ?)",
                   (name, description, base_prompt, generated_sql_schema))
    conn.commit()
    conn.close()
    execute_sql_schema(generated_sql_schema)

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

def edit_agent(agent_id, name=None, description=None, base_prompt=None, data_model_description=None):
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
    
    generated_sql_schema = None
    if data_model_description is not None:
        generated_sql_schema = generate_sql_schema(data_model_description)
    dbml_schema = generated_sql_schema if generated_sql_schema is not None else current_agent[4]

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
    execute_sql_schema(dbml_schema)
