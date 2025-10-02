# 代码生成时间: 2025-10-03 01:34:22
from typing import List
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field
from sklearn.cluster import KMeans
import numpy as np
from sklearn.datasets import make_blobs
from sklearn.preprocessing import StandardScaler
import joblib

# 定义输入数据模型
class InputData(BaseModel):
    data: List[List[float]] = Field(..., description="输入数据")

# 定义输出数据模型
class OutputData(BaseModel):
    cluster_centers: List[List[float]] = Field(..., description="聚类中心")
    labels: List[int] = Field(..., description="样本的聚类标签")

app = FastAPI()

# 用于生成测试数据的端点
@app.post("/generate-data/")
def generate_test_data():
    X, _ = make_blobs(n_samples=300, centers=4, cluster_std=0.60, random_state=0)
    scaler = StandardScaler()
    X = scaler.fit_transform(X)
    return {"data": X.tolist()}

# 聚类分析端点
@app.post("/cluster-analysis/\)
async def cluster_analysis(data: InputData):
    try:
        # 转换数据为Numpy数组
        X = np.array(data.data)
        
        # 进行KMeans聚类
        kmeans = KMeans(n_clusters=4, random_state=0).fit(X)
        cluster_centers = kmeans.cluster_centers_.tolist()
        labels = kmeans.labels_.tolist()
        
        # 返回聚类结果
        return OutputData(
            cluster_centers=cluster_centers,
            labels=labels,
        )
    except Exception as e:
        # 错误处理
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

# Swagger UI
@app.get("/docs/\)
def read_docs():
    return { "message": "Check out the Swagger UI at the /docs URL" }

# 红宝书 UI
@app.get("/redoc/\)
def read_redoc():
    return { "message": "Check out the Redoc UI at the /redoc URL" }
