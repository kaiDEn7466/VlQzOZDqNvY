# 代码生成时间: 2025-10-23 05:43:12
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from typing import Optional
from jose import JWTError, jwt
from datetime import datetime, timedelta
from passlib.context import CryptContext
from passlib.hash import bcrypt

# 定义Pydantic模型
class User(BaseModel):
    username: str
    password: str

class UserInDB(User):
    hashed_password: str

# 创建FastAPI应用
app = FastAPI()

# OAuth2认证
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# 密码上下文
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# 模拟数据库
fake_db_users = {
    "johndoe": {
        "username": "johndoe",
        "hashed_password": bcrypt.hash("secret"),
        "disabled": False,
    }
}
fake_access_tokens = set()

# 错误处理
async def get_current_user(token: str = Depends(oauth2_scheme)):
    if token not in fake_access_tokens:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Invalid authentication credentials",
                            headers={"WWW-Authenticate": "Bearer"})
    # 这里应该是验证token并获取用户信息的逻辑
    return fake_db_users.get("johndoe")

# 生成token
def generate_access_token(*, username: str):
    expire = datetime.utcnow() + timedelta(minutes=30)
    to_encode = {
        "exp": expire,
        "sub": username,
    }
    encoded_jwt = jwt.encode(to_encode, "secret", algorithm="HS256")
    fake_access_tokens.add(encoded_jwt)
    return encoded_jwt

# 获取token端点
@app.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends(), current_user: User = Depends(get_current_user)):
    fake_db_user = fake_db_users.get(form_data.username)
    if fake_db_user is None or not pwd_context.verify(form_data.password, fake_db_user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Incorrect username or password")
    access_token = generate_access_token(username=form_data.username)
    return {"access_token": access_token, "token_type": "bearer"}

# 受保护的端点
@app.get("/users/me")
async def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user