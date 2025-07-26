# Multi-Agent AI Framework (CLI-Based with Gemini + SQLite)

## Project Overview

This project provides a command-line interface (CLI) based framework for managing multiple AI agents. Each agent can be configured with a specific purpose, a base prompt, and a DBML (Database Markup Language) schema. The agents leverage the Ollama local LLM to interpret natural language queries, generate SQL, and interact with a SQLite database. This allows for dynamic, natural language interaction with structured data, making it easy to manage various types of information through specialized AI agents.

## Features

- **Agent Creation & Management**: Create, list, and edit AI agents with custom names, descriptions, base prompts, and natural language data model descriptions (from which DBML schemas are generated).
- **Natural Language to SQL**: Interact with agents using plain English queries, which are then translated into SQL commands by the Ollama LLM.
- **Conversation Logging**: All interactions, including user queries, generated SQL, and AI reasoning, are logged for review.
- **Schema Awareness**: Agents understand the database structure through provided DBML schemas, ensuring generated SQL conforms to the defined data model.
- **CLI-First Experience**: All functionalities are accessible directly from the command line.
- **Lightweight & Portable**: Built with SQLite and Ollama (local LLM), making it easy to set up and run locally.

## Setup Instructions

Follow these steps to set up and run the Multi-Agent AI Framework on your system.

### Prerequisites

- **Python 3.9+**: Ensure you have Python installed. You can download it from [python.org](https://www.python.org/downloads/).
- **Ollama**: Install Ollama from [ollama.com](https://ollama.com/). Make sure to pull the `llama3.2` model (or your preferred model) by running: `ollama pull llama3.2`

### Installation Steps

1.  **Clone the Repository (or create the project directory)**:

    If you haven't already, create the project directory:
    ```bash
    mkdir multi_agent_ai
    cd multi_agent_ai
    ```

2.  **Create a Virtual Environment**:

    It's highly recommended to use a virtual environment to manage project dependencies. This prevents conflicts with other Python projects.
    ```bash
    python3 -m venv venv
    ```

3.  **Activate the Virtual Environment**:

    -   **On macOS/Linux**:
        ```bash
        source venv/bin/activate
        ```
    -   **On Windows (Command Prompt)**:
        ```bash
        venv\Scripts\activate.bat
        ```
    -   **On Windows (PowerShell)**:
        ```powershell
        .\venv\Scripts\Activate.ps1
        ```

4.  **Install Dependencies**:

    With your virtual environment activated, install the required Python packages:
    ```bash
    pip install -r requirements.txt
    ```

5.  **Make the CLI Tool Executable**:

    Navigate to the `multi_agent_ai` directory and make the `ai-agent` script executable:
    ```bash
    chmod +x ai-agent
    ```

6.  **Add to PATH (Optional, but Recommended)**:

    For easier access, you can add the `multi_agent_ai` directory to your system's PATH. This allows you to run `ai-agent` from any directory.

    -   **For Zsh (macOS/Linux)**: Add the following line to your `~/.zshrc` file:
        ```bash
        export PATH="$PATH:/path/to/your/multi_agent_ai"
        ```
        (Replace `/path/to/your/multi_agent_ai` with the actual absolute path to your project directory, e.g., `/Users/manoj/multi_agent_ai`)

    -   **For Bash (Linux)**: Add the same line to your `~/.bashrc` or `~/.bash_profile` file.

    After editing, remember to `source` your shell configuration file (e.g., `source ~/.zshrc`) or restart your terminal.

## Usage Guide

All interactions with the framework are done via the `ai-agent` CLI tool. Ensure your virtual environment is activated before running commands.

### Initializing the Database

Before creating agents, ensure the core database tables are set up. This is automatically handled when you run any `ai-agent` command, but you can explicitly initialize it if needed:

```bash
python -m multi_agent_ai.database
```

### Agent Management

#### 1. Create a New Agent

To create a new AI agent, use the `create_agent` command. You'll need to provide a name, description, a base prompt, and a natural language description of the data model. The agent will then generate the DBML schema and create the necessary tables.

**Example: Creating a DSA Roadmap Tracker Agent**

First, create a base prompt file (e.g., `dsa_prompt.txt`):

```
You are a learning assistant. Your goal is to help the user manage their DSA learning roadmap. Based on the user's request, generate the correct SQL query to interact with the database defined by the provided DBML schema. Focus only on the immediate request and do not generate SQL for actions not explicitly asked for (e.g., do not create a roadmap if the request is to add a topic to an existing one). Ensure the generated SQL is syntactically correct for SQLite.

Generate ONLY the SQL query, enclosed within `BEGIN SQL` and `END SQL` markers. After the `END SQL` marker, on a new line, output '---REASONING---', and then provide a step-by-step reasoning for the query.

Example:
BEGIN SQL
SELECT * FROM users;
END SQL
---REASONING---
This query selects all users.
```

Now, create the agent:

```bash
ai-agent create_agent \
  --name "DSA Roadmap Tracker" \
  --description "An agent to manage a Data Structures and Algorithms learning roadmap." \
  --base_prompt "$(cat dsa_prompt.txt)" \
  --data_model_description "A database to track DSA roadmaps, topics, and questions. Roadmaps have a name and description. Topics belong to a roadmap and can have a parent topic, a name, and a description. Questions belong to a topic and have text, a difficulty rating, and a boolean indicating if they are done."
```

#### 2. List All Agents

To see a list of all configured agents and their IDs:

```bash
ai-agent list_agents
```

#### 3. Edit an Existing Agent

To modify an agent's details (name, description, base prompt, or DBML schema), use the `edit_agent` command with the agent's ID. You only need to provide the fields you want to change.

**Example: Updating an Agent's Description**

```bash
ai-agent edit_agent --id 1 --description "Updated description for the DSA agent."
```

**Example: Updating an Agent's Base Prompt (after modifying `dsa_prompt.txt`)**

```bash
ai-agent edit_agent --id 1 --base_prompt "$(cat dsa_prompt.txt)"
```

**Example: Updating an Agent's Data Model Description**

```bash
ai-agent edit_agent --id 1 --data_model_description "A database to track DSA roadmaps, topics, and questions. Roadmaps have a name and description. Topics belong to a roadmap and can have a parent topic, a name, and a description. Questions belong to a topic and have text, a difficulty rating, and a boolean indicating if they are done."
```

### Interacting with Agents

#### 1. Use an Agent to Ask a Question

To interact with an agent and ask a natural language question, use the `use_agent` command with the agent's ID and your query.

**Example: Creating a New Roadmap**

```bash
ai-agent use_agent --id 1 --query "Create a new roadmap called 'DSA Core Concepts'"
```

**Example: Listing All Roadmaps**

```bash
ai-agent use_agent --id 1 --query "List all roadmaps"
```

**Example: Adding a Topic to a Roadmap**

```bash
ai-agent use_agent --id 1 --query "Add a topic named 'Arrays' to the 'DSA Core Concepts' roadmap."
```

**Example: Adding a Question to a Topic**

```bash
ai-agent use_agent --id 1 --query "Add a question 'Implement a dynamic array' with difficulty 3 to the 'Arrays' topic."
```

**Example: Marking a Question as Done**

```bash
ai-agent use_agent --id 1 --query "Mark question 'Implement a dynamic array' as done."
```

**Example: Listing Questions under a Topic**

```bash
ai-agent use_agent --id 1 --query "List all questions under 'Arrays' topic."
```

## Troubleshooting

-   **`ModuleNotFoundError`**: Ensure your virtual environment is activated (`source venv/bin/activate`) and all dependencies are installed (`pip install -r requirements.txt`). If you added `ai-agent` to your PATH, ensure the shebang line (`#!/path/to/your/venv/bin/python3`) correctly points to your virtual environment's Python interpreter.
-   **`sqlite3.OperationalError: no such table`**: This indicates the database schema for your agent's data model has not been applied. Ensure you have run `ai-agent edit_agent --id <agent_id> --data_model_description "Your data model description"` for the agent, or explicitly run `python -m multi_agent_ai.database` to initialize the core tables.
-   **SQL Syntax Errors**: If the agent generates incorrect SQL, refine the `base_prompt` for that agent to provide clearer instructions and examples on the expected SQL format and constraints.
-   **`ai-agent: command not found`**: If you added `ai-agent` to your PATH, ensure you have sourced your shell configuration file (e.g., `source ~/.zshrc`) or restarted your terminal after adding the path.
