# Self-Healing SQL Agent

Turning database errors into learning opportunities.

A lightweight autonomous agent that makes natural language to SQL queries more robust and reliable.

Instead of failing on the first error — such as a wrong column name, missing JOIN, or hallucinated table — the agent enters a **reflection loop**. This loop allows the agent to learn from its mistakes and intelligently repair the SQL query.


## The Idea

Most Text-to-SQL systems are stateless: the LLM generates one query, executes it, and if it fails, the process stops completely. Valuable information from the database error message is ignored.

We built an agent that treats the database like a tutor. When a query fails, it doesn't give up — it **reflects**, analyzes the error, and tries again.

## How the Reflection Loop Works

The agent follows this self-healing process (up to 3 attempts):

1. **Generate Initial Query**  
   The LLM converts the user's natural language question into an SQL query using the database schema.

2. **Execute the Query**  
   The generated SQL is run against the SQLite database.

3. **Handle Failure & Reflect**  
   If the query fails, the agent captures the **exact database error message** and adds it to the context along with:
   - Full database schema (DDL)
   - Sample rows from each table
   - History of previous attempts and errors

4. **Structured Reflection**  
   The LLM is prompted to fill a structured reflection form:
   - **Mistake Analysis**: What went wrong?
   - **Repair Strategy**: How should we fix it?
   - **Corrected SQL**: The improved query

5. **Retry or Fallback**  
   The corrected query is executed. This loop repeats up to 3 times.  
   If it still fails after 3 attempts, the agent gracefully explains the limitation to the user instead of crashing.

This reflection loop turns a brittle one-shot process into a resilient, self-correcting system.

## Features

- Autonomous self-repair using real database error messages
- Rich context injection (full schema, sample rows, and error history)
- Structured outputs for reliable and consistent LLM responses
- Graceful fallback when it cannot fix the query
- Simple and fast to run locally with SQLite

## Tech Stack

- **LLM**: GPT-4o-mini (strong reasoning at low cost)
- **Structured Output**: Instructor + Pydantic
- **Database**: SQLite (zero configuration)
- **Orchestration**: Simple retry loop with conversation history

## Quick Start

* git clone https://github.com/srishtikapoor22/sql_agent.git
* cd sql_agent
* pip install -r requirements.txt

Set your OpenAI API key and run the demo:
* python main.py

## What We Learned

* Forcing the model to articulate its own mistakes before fixing them leads to significantly better repairs.
* A simple while loop combined with careful prompt design and structured output can make even small models very robust.
* Treating database errors as useful feedback — rather than just failures — changes how we design agentic systems.

