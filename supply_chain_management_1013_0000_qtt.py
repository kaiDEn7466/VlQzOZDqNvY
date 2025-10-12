# 代码生成时间: 2025-10-13 00:00:40
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, ValidationError
from typing import List, Optional
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from fastapi import APIRouter
from fastapi.openapi.utils import get_openapi

class SupplyChainItem(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    price: float
    in_stock: bool

    # Pydantic模型的额外验证
    @property
    def validate_price(self):
        if self.price < 0:
            raise ValueError("Price cannot be negative")

    @property
    def validate_in_stock(self):
        if not isinstance(self.in_stock, bool):
            raise ValueError("In stock must be a boolean")

class SupplyChainAPIRouter(APIRouter):

    def __init__(self):
        super().__init__(tags=['supply-chain'])
        self.supply_chain_items: List[dict] = []

    # 获取供应链项目列表
    @router.get("/items/", response_model=List[SupplyChainItem])
    async def read_items(self):
        return self.supply_chain_items

    # 获取单个供应链项目
    @router.get("/items/{item_id}", response_model=SupplyChainItem)
    async def read_item(self, item_id: int):
        item = next(filter(lambda x: x['id'] == item_id, self.supply_chain_items), None)
        if item is not None:
            return item
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Item with id {item_id} not found")

    # 创建新的供应链项目
    @router.post("/items/", response_model=SupplyChainItem)
    async def create_item(self, item: SupplyChainItem):
        if any(item['id'] == x['id'] for x in self.supply_chain_items):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Item with this id already exists")
        item_data = jsonable_encoder(item)
        self.supply_chain_items.append(item_data)
        return item_data

    # 更新供应链项目
    @router.put("/items/{item_id}", response_model=SupplyChainItem)
    async def update_item(self, item_id: int, item: SupplyChainItem):
        item_data = next((item for item in self.supply_chain_items if item['id'] == item_id), None)
        if item_data is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Item with id {item_id} not found")
        if any((item['id'] == item_id) and (x != item_data) for x in self.supply_chain_items):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Item with this id already exists")
        item_data.update(jsonable_encoder(item))
        return item_data

    # 删除供应链项目
    @router.delete("/items/{item_id}", response_model=SupplyChainItem)
    async def delete_item(self, item_id: int):
        item_data = next((item for item in self.supply_chain_items if item['id'] == item_id), None)
        if item_data is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Item with id {item_id} not found")
        self.supply_chain_items = [item for item in self.supply_chain_items if item['id'] != item_id]
        return item_data

# 创建FastAPI应用
app = FastAPI()

# 添加API文档
app.openapi()

# 初始化API路由器并添加到FastAPI应用中
router = SupplyChainAPIRouter()
app.include_router(router)

# 错误处理中间件
@app.exception_handler(ValidationError)
async def validation_exception_handler(request, exc):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"detail": exc.errors()}
    )

# 获取OpenAPI文档信息
def custom_openapi():
    if app.openapi_schema:
        yield app.openapi_schema

app.get("/openapi")(
    custom_openapi
)
