from fastapi import FastAPI
from app.routers import customer

# Initialize the FastAPI app
app = FastAPI()

# Include the customer router
app.include_router(customer.router)

# Example route
@app.get("/")
async def root():
    return {"message": "Hello, World!"}