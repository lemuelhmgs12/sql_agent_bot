"""
project settings - all notebooks use the same values.
"""
from pathlib import Path

# paths
PROJECT_ROOT = Path(__file__).resolve().parents[1]

# promot file
PROMPT_FILE = PROJECT_ROOT / "prompts" / "sql-agent-system-prompt.txt"

# DB
SCHEMA_NAME = "grocery_db"
TABLES = ["customer_details", "transactions"]
SAMPLE_ROWS = 5
STATEMENT_TIMEOUT_MS = 15000

# model
LLM_MODEL = "gpt-4.1"