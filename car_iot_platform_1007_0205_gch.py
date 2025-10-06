# 代码生成时间: 2025-10-07 02:05:19
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
from typing import Optional
from fastapi.responses import JSONResponse

# Pydantic模型定义
class Car(BaseModel):
    id: int
    brand: str
    model: str
    year: int

# 创建FastAPI应用
app = FastAPI()

# 车联网平台端点
@app.get("/cars")
async def get_cars(year: Optional[int] = None):
    # 示例数据
    cars = [
        {
            "id": 1,
            "brand": "Toyota",
            "model": "Corolla",
            "year": 2021
        },
        {
            "id": 2,
            "brand": "Honda",
            "model": "Civic",
            "year": 2020
        },
        {
            "id": 3,
            "brand": "Ford",
            "model": "Mustang",
            "year": 2022
        }
    ]

    # 过滤年份
    if year:
        cars = [car for car in cars if car["year"] == year]

    return cars

# 错误处理
@app.exception_handler(ValueError)
async def value_error_handler(request, exc):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={
            "detail": "Invalid input"
        },
    )

# 启动应用
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)