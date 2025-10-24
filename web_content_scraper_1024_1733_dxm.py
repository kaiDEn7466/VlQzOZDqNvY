# 代码生成时间: 2025-10-24 17:33:52
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from requests import get
from bs4 import BeautifulSoup
from typing import Optional

# Pydantic模型定义
class ScrapeRequest(BaseModel):
    url: str

app = FastAPI()

# 错误处理装饰器
def validate_url(request: ScrapeRequest):
    if not request.url.startswith('http'):
        raise HTTPException(status_code=400, detail="URL must start with 'http'")

@app.post("/crawl")
async def crawl_content(request: ScrapeRequest):
    # 验证URL
    validate_url(request)
    try:
        # 发起请求获取网页内容
        response = get(request.url)
        response.raise_for_status()
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)
    
    # 使用BeautifulSoup解析网页内容
    soup = BeautifulSoup(response.content, 'html.parser')
    content = soup.get_text()
    
    # 返回网页内容
    return {"content": content}

# 添加FastAPI文档
@app.get("/")
async def read_root():
    return {"message": "Welcome to Web Content Scraper API"}

# 错误处理
@app.exception_handler(Exception)
async def custom_http_exception_handler(request, exc):
    return JSONResponse(
        status_code=500,
        content={"detail": f"An error occurred: {str(exc)}"},
    )

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)