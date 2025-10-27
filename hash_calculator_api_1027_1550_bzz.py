# 代码生成时间: 2025-10-27 15:50:59
from typing import Optional
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field
from hashlib import sha256, sha1, md5
from fastapi.responses import JSONResponse

# Pydantic model for request data
class HashRequest(BaseModel):
    data: str = Field(..., description="Data to be hashed")
    hash_type: str = Field("sha256", description="Type of hash to use")

    # Validate the hash_type
    @root_validator(pre=True)
    def validate_hash_type(cls, values):
        hash_type = values.get("hash_type")
        if hash_type not in ["sha256", "sha1", "md5"]:
            raise ValueError("Unsupported hash type")
        return values

app = FastAPI()

@app.post("/hash")
async def calculate_hash(data: HashRequest):
    """
    Calculate the hash of the provided data.
    ---
    parameters:
      - name: data
        in: body
        required: true
        schema:
          $ref: '#/components/schemas/HashRequest'
    responses:
      200:
        description: The hash of the provided data.
        schema:
          type: object
          properties:
            hash:
              type: string
   """
    try:
        hash_obj = eval(getattr(hashlib, f"{data.hash_type}"))()
        hash_obj.update(data.data.encode())
        return {"hash": hash_obj.hexdigest()}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"Error calculating hash: {str(e)}")

# Error handling
@app.exception_handler(ValueError)
async def value_error_exception_handler(request, exc):
    return JSONResponse(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, content={"detail": str(exc)})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)