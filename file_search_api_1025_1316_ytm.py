# 代码生成时间: 2025-10-25 13:16:13
from fastapi import FastAPI, HTTPException, File, UploadFile
from fastapi.responses import JSONResponse
from pydantic import BaseModel, ValidationError
from typing import Optional
import os
import shutil
import uuid

# Pydantic模型用于文件搜索请求
class SearchQuery(BaseModel):
    path: str
    query: str

# FastAPI 应用实例
app = FastAPI()

# 文件搜索和索引工具端点
@app.post("/search")
async def search_files(query: SearchQuery):
    # 验证搜索路径是否存在
    if not os.path.exists(query.path):
        raise HTTPException(status_code=404, detail="Path not found")

    try:
        # 搜索文件
        results = []
        for root, dirs, files in os.walk(query.path):
            for file in files:
                if query.query.lower() in file.lower():
                    results.append(os.path.join(root, file))

        return JSONResponse(content={"results": results})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# 错误处理
@app.exception_handler(ValidationError)
async def validation_exception_handler(request, exc):
    return JSONResponse(
        status_code=400,
        content={"detail": "Validation error occurred", "errors": exc.errors()}
    )

@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail}
    )

# 以下是 FastAPI 自动生成的文档和Swagger UI
# 可以访问 /docs 和 /redoc 获取

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)