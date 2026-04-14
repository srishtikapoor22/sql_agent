import sqlite3

def setup_sample_db():
    conn =sqlite3.connect("data/sample.db")
    cursor=conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY,
        full_name TEXT,
        email TEXT
    )""")

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS orders (
        order_id INTEGER PRIMARY KEY,
        buyer_id INTEGER,
        amount REAL,
        status TEXT,
        FOREIGN KEY(buyer_id) REFERENCES users(user_id)
    )""")

    # Insert Dummy Data
    cursor.executemany("INSERT INTO users VALUES (?,?,?)", [
        (1, 'Srishti', 'srishti@example.com'),
        (2, 'Tasneem', 'tasneem@example.com')
    ])
    
    cursor.executemany("INSERT INTO orders VALUES (?,?,?,?)", [
        (101, 1, 150.50, 'shipped'),
        (102, 2, 89.99, 'pending'),
        (103, 1, 45.00, 'cancelled')
    ])

    conn.commit()
    conn.close()
    print("Database 'sample.db' created")

if __name__ == "__main__":
    setup_sample_db()