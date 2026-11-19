"""
Database connection for the SQL agent.
Credentials come from .env; settings (schema, tables, timeout) from src/config.py.
"""
import os

import sqlalchemy as sa
from langchain_community.utilities import SQLDatabase

from src import config


def build_postgres_uri():
    """Build the PostgreSQL connection string from .env. Never print the result: it contains the password."""
    return (f"postgresql+psycopg2://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}"
            f"@{os.getenv('POSTGRES_HOST')}:{os.getenv('POSTGRES_PORT')}/{os.getenv('POSTGRES_DBNAME')}?sslmode=require")
    


def get_engine():
    """Create the database engine and check the connection works."""
    engine = sa.create_engine(build_postgres_uri(),
                              pool_pre_ping=True,
                              connect_args={"options": f"-c statement_timeout={config.STATEMENT_TIMEOUT_MS}"} 
                             ) 

    # check the connection
    with engine.connect() as conn:
        conn.exec_driver_sql("select 1")
        

    return engine


def get_database():
    """SQLDatabase limited to the grocery_db schema and the two tables the agent may use."""
    db = SQLDatabase(engine=get_engine(),
                     schema=config.SCHEMA_NAME,
                     include_tables=config.TABLES,
                     sample_rows_in_table_info=config.SAMPLE_ROWS)
    return db


if __name__ == "__main__":
    from dotenv import load_dotenv

    load_dotenv()
    db = get_database()
    print("Usable tables:", db.get_usable_table_names())