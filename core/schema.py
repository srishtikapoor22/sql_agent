import sqlite3
from sqlalchemy import create_engine, inspect,text

class DatabaseMapper:
    def __init__(self,db_path:str):
        self.db_url=f"sqlite:///{db_path}"
        self.engine=create_engine(self.db_url)
        self.inspector=inspect(self.engine)

    #extract tables n colums from the db
    def get_context(self)->str:
        schema_output="Database Schema:\n"
        tables=self.inspector.get_table_names()

        for table in tables:
            columns=self.inspector.get_columns(table)
            col_details=[f"{c['name']} ({c['type']})" for c in columns]

            #exxtracting first 3 rows of sample data
            with self.engine.connect() as conn:
                sample=conn.execute(text(f"SELECT * FROM {table} LIMIT 3")).mappings().all()
                sample_rows=[dict(row) for row in sample]

            schema_output += f"\nTable: {table}\n"
            schema_output += f"Columns: {', '.join(col_details)}\n"
            schema_output += f"Sample Data: {sample_rows}\n"
            schema_output += "-" * 30 + "\n"

        return schema_output

mapper = DatabaseMapper("data/sample.db")
print(mapper.get_context())
                
                

