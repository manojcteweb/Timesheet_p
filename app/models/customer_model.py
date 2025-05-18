import sqlite3
from fastapi import HTTPException

# Database connection
DATABASE = 'customers.db'

class CustomerModel:
    def __init__(self):
        self.conn = sqlite3.connect(DATABASE)
        self.cursor = self.conn.cursor()

    def create_table(self):
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS customers (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE
        )
        ''')
        self.conn.commit()

    def add_customer(self, customer: dict):
        customer_id = customer.get("id")
        if not customer_id:
            raise HTTPException(status_code=400, detail="Customer ID is required")
        if not isinstance(customer.get("name"), str) or not customer.get("name"):
            raise HTTPException(status_code=400, detail="Customer name is required and must be a string")
        if not isinstance(customer.get("email"), str) or not customer.get("email"):
            raise HTTPException(status_code=400, detail="Customer email is required and must be a string")

        try:
            self.cursor.execute('INSERT INTO customers (id, name, email) VALUES (?, ?, ?)',
                               (customer_id, customer.get("name"), customer.get("email")))
            self.conn.commit()
        except sqlite3.IntegrityError:
            raise HTTPException(status_code=400, detail="Customer with this ID or email already exists")
        except Exception:
            raise HTTPException(status_code=500, detail="Internal Server Error")

    def get_customer(self, customer_id: str):
        self.cursor.execute('SELECT * FROM customers WHERE id = ?', (customer_id,))
        customer = self.cursor.fetchone()
        if not customer:
            raise HTTPException(status_code=404, detail="Customer not found")
        return {"id": customer[0], "name": customer[1], "email": customer[2]}

    def update_customer(self, customer_id: str, customer_data: dict):
        if 'name' in customer_data:
            self.cursor.execute('UPDATE customers SET name = ? WHERE id = ?', (customer_data['name'], customer_id))
        if 'email' in customer_data:
            self.cursor.execute('UPDATE customers SET email = ? WHERE id = ?', (customer_data['email'], customer_id))
        self.conn.commit()

    def delete_customer(self, customer_id: str):
        self.cursor.execute('DELETE FROM customers WHERE id = ?', (customer_id,))
        self.conn.commit()