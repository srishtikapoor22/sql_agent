import sqlite3
import instructor
from pydantic import BaseModel,Field
from groq import Groq
from core.schema import DatabaseMapper
from pydantic import BaseModel,Field
import os
from dotenv import load_dotenv
load_dotenv()

groq_client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
client = instructor.from_groq(
    groq_client, 
    mode=instructor.Mode.JSON
)

class SQLReflexion(BaseModel):
    failure_reason: str=Field(description="If the last attempt failed, explain why.")
    fix_strategy: str = Field(description="Detailed plan to fix the SQL based on the schema.")
    sql: str = Field(description="The valid SQLite query to run.")


def run_agentic_query(user_input:str):
    #load db schema
    mapper=DatabaseMapper("data/sample.db")
    schema_context=mapper.get_context()

    messages=[
        {"role": "system", "content": f"You are a SQL Expert. Schema:\n{schema_context}"},
        {"role": "user", "content": user_input}
    ]
    attempts=0
    while attempts<3:
        #generate response from the llm
        response=client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=messages,
            response_model=SQLReflexion
        )

        print(f"\n--- Attempt {attempts + 1} ---")
        print(f"Reflexion: {response.failure_reason}")
        print(f"SQL: {response.sql}")

        try:
            conn = sqlite3.connect("data/sample.db")
            cursor = conn.cursor()
            cursor.execute(response.sql)
            results = cursor.fetchall()
            conn.close()
            
            print("Success")
            return results

        except Exception as e:
            error_msg = str(e)
            print(f"Error: {error_msg}")
            
            messages.append({"role": "assistant", "content": f"I tried: {response.sql}\nError: {error_msg}"})
            messages.append({"role": "user", "content": "That failed. Please analyze the error and try again."})
            
            attempts += 1
    return "Failed to find a valid query after 3 attempts."

if __name__ == "__main__":
    query = "Show me the names of users who have 'shipped' orders."
    data = run_agentic_query(query)
    print("\nFINAL RESULT:", data)