# 代码生成时间: 2025-10-16 23:20:40
from fastapi import FastAPI, HTTPException, Request, File, UploadFile
from fastapi.responses import JSONResponse
from pydantic import BaseModel, ValidationError
from fastapi.encoders import jsonable_encoder
from typing import Optional
from PIL import Image, ImageDraw, ImageFont
import io
import os
import base64
import secrets


class WatermarkRequest(BaseModel):
    image: UploadFile  # 图片文件
    text: str        # 要添加的水印文本
    font_size: Optional[int] = None  # 字体大小
    font_path: Optional[str] = None  # 字体路径
    opacity: Optional[int] = 128  # 水印透明度（0-255）
    position: Optional[str] = "bottom-right"  # 水印位置

app = FastAPI()

# 错误处理
@app.exception_handler(ValidationError)
async def validation_exception_handler(request: Request, exc: ValidationError):
    return JSONResponse(
        status_code=400,
        content=jsonable_encoder({"detail": exc.errors()})
    )

# 添加水印到图片
@app.post("/add_watermark/")
async def add_watermark(request: WatermarkRequest):
    try:
        # 读取上传的图片
        image_bytes = await request.image.read()
        image = Image.open(io.BytesIO(image_bytes))

        # 设置水印文本
        watermark_text = request.text

        # 设置字体和透明度
        if request.font_size and request.font_path:
            font = ImageFont.truetype(request.font_path, request.font_size)
        else:
            font = ImageFont.load_default()
        opacity = request.opacity

        # 根据位置添加水印
        draw = ImageDraw.Draw(image)
        text_width, text_height = draw.textsize(watermark_text, font=font)
        if request.position == "bottom-right":
            x = image.width - text_width - 10
            y = image.height - text_height - 10
        elif request.position == "bottom-left":
            x = 10
            y = image.height - text_height - 10
        elif request.position == "top-right":
            x = image.width - text_width - 10
            y = 10
        elif request.position == "top-left":
            x = 10
            y = 10
        else:
            raise HTTPException(status_code=400, detail="Unsupported position")

        # 添加水印
        draw.text((x, y), watermark_text, font=font, fill=(255, 255, 255, opacity))

        # 保存水印后的图片
        buffered = io.BytesIO()
        image.save(buffered, format="PNG")
        buffered.seek(0)

        # 返回添加了水印的图片
        image_base64 = base64.b64encode(buffered.getvalue()).decode("utf-8")

        return JSONResponse(
            status_code=200,
            content=jsonable_encoder({"image": f"data:image/png;base64,{image_base64}"})
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
