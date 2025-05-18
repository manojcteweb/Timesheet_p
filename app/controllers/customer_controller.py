from fastapi import APIRouter, HTTPException

router = APIRouter()

# In-memory storage for customers
customers_db = {}

# Define customer-related endpoints

@router.post("/customers")
async def add_customer(customer: dict):
    try:
        customer_id = customer.get("id")
        if not customer_id:
            raise HTTPException(status_code=400, detail="Customer ID is required")
        if customer_id in customers_db:
            raise HTTPException(status_code=400, detail="Customer already exists")
        customers_db[customer_id] = customer
        return {"message": "Customer created", "customer": customer}
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")