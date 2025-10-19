# 代码生成时间: 2025-10-19 09:02:01
from fastapi import FastAPI, HTTPException, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Optional
from uuid import uuid4
import ssl
import os

# Pydantic model for SSL/TLS certificates
class Certificate(BaseModel):
    certificate: str
    private_key: str
    passphrase: Optional[str] = None

# In-memory storage for certificates
certificates_storage = {}

app = FastAPI()

# Create a new certificate endpoint
@app.post("/certificates/")
async def create_certificate(certificate: Certificate):
    # Generate a unique ID for the certificate
    cert_id = str(uuid4())
    # Save the certificate to the storage
    certificates_storage[cert_id] = certificate
    return {"cert_id": cert_id}

# Get a certificate endpoint
@app.get("/certificates/{cert_id}")
async def get_certificate(cert_id: str):
    # Check if the certificate exists
    if cert_id not in certificates_storage:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Certificate not found")
    # Return the certificate
    return certificates_storage[cert_id]

# Delete a certificate endpoint
@app.delete("/certificates/{cert_id}")
async def delete_certificate(cert_id: str):
    # Check if the certificate exists
    if cert_id not in certificates_storage:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Certificate not found")
    # Remove the certificate from the storage
    del certificates_storage[cert_id]
    return {"message": "Certificate deleted"}

# Error handler for 404 errors
@app.exception_handler(404)
async def not_found_exception_handler(request, exc):
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"message": exc.detail}
    )

# Error handler for 500 errors
@app.exception_handler(500)
async def server_error_exception_handler(request, exc):
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"message": "Internal server error"}
    )

# Run the API using Uvicorn
# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="0.0.0.0", port=8000)