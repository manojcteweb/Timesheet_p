from fastapi import HTTPException
import sqlite3

# Database connection
DATABASE = 'customers.db'

# Initialize the database
conn = sqlite3.connect(DATABASE)
cursor = conn.cursor()
cursor.execute('''
CREATE TABLE IF NOT EXISTS customers (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE
)
''')
conn.commit()


def add_customer_service(customer: dict):
    """
    Business logic for adding a new customer.
    """
    customer_id = customer.get("id")
    if not customer_id:
        raise HTTPException(status_code=400, detail="Customer ID is required")
    # Validate input data
    if not isinstance(customer.get("name"), str) or not customer.get("name"):
        raise HTTPException(status_code=400, detail="Customer name is required and must be a string")
    if not isinstance(customer.get("email"), str) or not customer.get("email"):
        raise HTTPException(status_code=400, detail="Customer email is required and must be a string")

    try:
        # Insert customer into the database
        cursor.execute('INSERT INTO customers (id, name, email) VALUES (?, ?, ?)',
                       (customer_id, customer.get("name"), customer.get("email")))
        conn.commit()
    except sqlite3.IntegrityError as e:
        raise HTTPException(status_code=400, detail="Customer with this ID or email already exists")
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")

    return {"message": "Customer created", "customer": customer}