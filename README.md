# ABC Grocery SQL Agent

An AI agent that answers questions about a grocery retailer's customer and transaction data in plain English. It writes a PostgreSQL query, runs it on a cloud database, and explains the result, so people who don't write SQL can still get answers from the data.

Built with LangChain, OpenAI (`gpt-4.1`), SQLAlchemy and PostgreSQL.

**Full write-up:** _coming soon_

---

## Results

I tested the agent on two questions and checked each answer by running my own SQL on the database.

| Question | Agent's answer | My check |
|---|---|---|
| On average, which gender lives furthest from the store? | Female, 3.98 miles | ✅ Female 3.98 (485 customers), unspecified 3.36 (5), male 0.87 (380) |
| What is the average transaction value in September 2020 for male customers with a credit score above 0.5? | $88.49 | ✅ $88.49 over 1,046 transactions |

### Key findings

- **The agent handled the tricky part of the data correctly.** The transactions table has one row per product area, so a single shopping trip can have several rows. For question 2, the agent added up each transaction's rows before averaging, so nothing was double counted.
- **Question 2 had a second fair answer, and the agent didn't mention it.** "Average transaction value" can mean the average over all transactions ($88.49), or the average of each customer's average ($101.32, 14% higher). The agent chose the first without saying so, even though the system prompt asks it to check when a question is ambiguous.
- **The agent decides which tools to use.** For question 1 it went straight to running a query, because the system prompt already describes the tables. For question 2 it used the query checker first. The tool descriptions guide it, but don't force it.
- **The wording of answers varies between runs,** even with `temperature=0`. The numbers stayed the same.

---

## How it works

1. **Connection:** a SQLAlchemy engine connects to PostgreSQL using credentials from `.env`, with an encrypted connection (`sslmode=require`), a 15-second query timeout and a health check on start-up.
2. **Scope:** LangChain's `SQLDatabase` limits the agent to the `grocery_db` schema and two tables, `customer_details` and `transactions`, and shows it 5 sample rows from each.
3. **Tools:** `SQLDatabaseToolkit` gives the agent four tools: list tables, get a table's schema, check a query, and run a query.
4. **System prompt:** describes the agent's role, read-only rules, the tables and how they join, the data's date range, rules for writing queries, and three worked examples.
5. **Agent:** `create_agent` combines the LLM, the tools and the system prompt. Given a question, it decides which tools to call, reads the results, and writes the answer.

---

## Project structure

```
sql_agent_bot/
├── notebooks/
│   ├── 01_database_connection.ipynb    # connect, health check, scope the tables, see what the agent sees
│   └── 02_sql_agent.ipynb              # build the agent, ask the two questions, check the answers
├── prompts/
│   └── sql-agent-system-prompt.txt     # the agent's system prompt
├── src/
│   ├── config.py                       # schema, tables, sample rows, timeout, model
│   ├── database.py                     # engine, health check and scoped SQLDatabase
│   └── agent.py                        # LLM + SQL tools + system prompt
├── .env.example
├── pyproject.toml
└── uv.lock
```

---

## Setup

Requires Python 3.12, [uv](https://docs.astral.sh/uv/), and access to a PostgreSQL database with the `grocery_db` tables. The database credentials are not included in this repo.

```bash
# 1. install the dependencies
uv sync

# 2. add your database credentials and OpenAI API key
cp .env.example .env
# then edit .env

# 3. check the database connection
uv run python -m src.database

# 4. ask the agent a question
uv run python -m src.agent
```

Run all commands from the project root.

---

## Known limitations

- **Read-only is enforced by the prompt only.** The query tool runs whatever SQL it's given, and the "SELECT only" rule lives in the system prompt. In production, the agent should connect with a read-only database user.
- **Ambiguous questions aren't always caught.** As question 2 showed, the agent can pick one reading of a question without saying so.
- **Small test:** two questions show the agent works on a simple and a more complex question, but don't cover every case.
- **Data window:** transactions only cover 2020-04-01 to 2020-09-30.

---

## Next steps

- Exposing additional tables and relationships as the data model grows
- Adding a light web UI so business users can ask questions without touching SQL
- Logging queries and answers for audit, training, and documentation
- Allowing the agent to ask clarification questions in more complex scenarios

---

## Tech stack

Python 3.12 · uv · LangChain · OpenAI (`gpt-4.1`) · SQLAlchemy · psycopg2 · PostgreSQL · Jupyter