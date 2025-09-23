# 代码生成时间: 2025-09-24 01:12:56
from fastapi import FastAPI, HTTPException, File, UploadFile
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import List
import pandas as pd
from io import StringIO
import xlsxwriter


# Pydantic模型定义
class ExcelData(BaseModel):
    data: List[List[str]]  # Excel数据，以二维列表形式提供
    sheet_name: str = 'Sheet1'  # 工作表名称，默认为'Sheet1'


# 创建FastAPI应用
app = FastAPI()


# 错误处理
@app.exception_handler(ValueError)
async def value_error_exception_handler(request, exc):
    return JSONResponse(
        status_code=400,
        content="{"message": "Invalid data provided"}"
    )


# Excel表格生成器端点
@app.post("/generate-excel")
async def generate_excel(data: ExcelData):
    try:
        # 将数据转换为DataFrame
        df = pd.DataFrame(data.data)

        # 使用StringIO作为文件缓冲区
        output = StringIO()
        writer = pd.ExcelWriter(output, engine='xlsxwriter')
        df.to_excel(writer, sheet_name=data.sheet_name, index=False)
        writer.save()
        writer.close()

        # 将StringIO的内容转换为字节流
        output.seek(0)
        excel_file = output.getvalue().encode('utf-8')
        output.close()

        # 返回文件流
        return Response(
            content=excel_file,
            media_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            headers={"Content-Disposition": f"attachment; filename={data.sheet_name}.xlsx"}
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# 启动文档服务器
if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='127.0.0.1', port=8000)