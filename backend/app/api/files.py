from fastapi import APIRouter,File,UploadFile
from app.common.exceptions import BusinessException
import os
from pathlib import Path
from app.config import ALLOWED_EXTENSIONS,MAX_FILE_SIZE,UPLOAD_DIR
import time
import uuid
import shutil
from app.common.response import Response
from app.schemas.file import FileResponse

router=APIRouter(prefix="/files",tags=["文件管理"])

@router.post("/upload")
def upload(file:UploadFile=File(...)):
    """文件上传接口"""
    if not file.filename:
        raise BusinessException(message="文件名不能为空")
    #原始文件名
    original_name=os.path.basename(file.filename)
    #文件后缀 比如.jpg
    ext=Path(original_name).suffix.lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise BusinessException(message=f"不支持该文件后缀:{ext}")

    #文件大小的校验
    if file.size and file.size>MAX_FILE_SIZE:
        raise BusinessException(message=f"上传的文件超过{MAX_FILE_SIZE//1024//1024}MB")

    #设置唯一文件名称
    disk_name=f"{int(time.time()*1000)}_{uuid.uuid4().hex[:8]}{ext}"
    save_path=UPLOAD_DIR/disk_name      #

    #流式上传文件，边读边写
    with open(save_path,"wb")as f:
        shutil.copyfileobj(file.file,f)

    return Response.success(
        data=FileResponse(
            original_name=original_name,
            disk_name=disk_name,
            size=file.size,
            url=f"/uploads/{disk_name}")
    )
