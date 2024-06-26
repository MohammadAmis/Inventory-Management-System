import sqlite3

# Connect to the SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect('example.db')
cursor = conn.cursor()

# Create the table
cursor.execute('''
CREATE TABLE IF NOT EXISTS customer_orders (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_id INTEGER,
    customer_name TEXT,
    contact_number TEXT,
    email TEXT,
    address TEXT,
    products TEXT
)
''')

# Sample data for insertion
data = [
    (8, 'Patricia Jones', '4567890123', 'patricia.jones@example.com', '987 Maple St, City D', 'rice,wheat,pulse')
]

# Insert 20 records
for i in range(20):
    cursor.executemany('''
    INSERT INTO customer_orders (customer_id, customer_name, contact_number, email, address, products)
    VALUES (?, ?, ?, ?, ?, ?)
    ''', data)

# Commit the transaction
conn.commit()

# Verify the inserted records
cursor.execute('SELECT * FROM customer_orders')
rows = cursor.fetchall()

for row in rows:
    print(row)

# Close the connection
conn.close()
