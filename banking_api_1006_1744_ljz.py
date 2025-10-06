# 代码生成时间: 2025-10-06 17:44:37
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, ValidationError
from typing import Optional
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
import uvicorn


# Pydantic模型定义
class BankAccount(BaseModel):
    id: Optional[int] = None
    account_number: str
    account_holder: str
    balance: float


app = FastAPI()


# 错误处理
@app.exception_handler(ValidationError)
async def validation_exception_handler(request, exc):
    return JSONResponse(
        status_code=400,
        content=jsonable_encoder({"detail": exc.errors()})
    )


# 示例数据
bank_accounts = [
    {
        "id": 1,
        "account_number": "12345678",
        "account_holder": "John Doe",
        "balance": 1000.0,
    },
    {
        "id": 2,
        "account_number": "87654321",
        "account_holder": "Jane Doe",
        "balance": 2000.0,
    },
]


# 获取所有银行账户
@app.get("/accounts/", response_model=List[BankAccount])
async def read_accounts():
    return bank_accounts


# 获取单个银行账户
@app.get("/accounts/{account_number}")
async def read_account(account_number: str):
    account = next(filter(lambda a: a["account_number"] == account_number, bank_accounts), None)
    if account is None:
        raise HTTPException(status_code=404, detail="Account not found")
    return account


# 更新银行账户余额
@app.put("/accounts/{account_number}")
async def update_account(account_number: str, account: BankAccount):
    account_dict = next(filter(lambda a: a["account_number"] == account_number, bank_accounts), None)
    if account_dict is None:
        raise HTTPException(status_code=404, detail="Account not found")
    account_dict.update(account.dict())
    return account_dict


# 启动服务器
if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=8000)