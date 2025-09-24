# 代码生成时间: 2025-09-24 10:28:20
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, ValidationError
from fastapi.testclient import TestClient
from fastapi.responses import JSONResponse
import pytest

# Pydantic model
class Item(BaseModel):
    name: str
    price: float
    description: str = None

# FastAPI instance
app = FastAPI()

# Error handler
@app.exception_handler(ValidationError)
async def validation_exception_handler(request, exc):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"detail": str(exc)},
    )

# API endpoint
@app.post("/items/")
async def create_item(item: Item):
    return item

# Unit test using TestClient
def test_read_main():
    client = TestClient(app)
    response = client.post("/items/", json={"name": "Foo", "price": 10, "description": "Bar"})
    assert response.status_code == 200
    assert response.json() == {"name": "Foo", "price": 10, "description": "Bar"}

# Test error handling
def test_error_handling():
    client = TestClient(app)
    response = client.post("/items/", json={"name": "Foo", "price": "ten"})  # invalid price
    assert response.status_code == 422
    assert "detail" in response.json()

# Run tests
if __name__ == "__main__":
    pytest.main(["-v", __file__])