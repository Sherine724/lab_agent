from fastapi import FastAPI,HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.exceptions import RequestValidationError
from app.models.user import User
#显式导入模型，让Base.metadata.create_all能建出labs和equipments两张表
from app.models.lab import Lab
from app.models.equipment import Equipment
from app.database import Base,engine
from app.api import api
from app.config import CORS_ORIGINS,UPLOAD_DIR

from starlette.middleware.cors import CORSMiddleware
from app.common.exceptions import (
    BusinessException,
    business_exception_halder,
    http_exception_halder,
    validation_exception_halder,
    global_exception_halder
    )

Base.metadata.create_all(bind=engine)
app=FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,     #允许的前端源，不要直接写["*"]
    allow_credentials=True,         #关键:允许前端携带Authorization Token
    allow_methods=["*"],            #允许所有请求方法 GET POST PUT DELETE OPTIONS
    allow_headers=["*"],            #允许所有请求头(包含Authorization)

)
app.include_router(api)

#注册自定义异常
app.add_exception_handler(BusinessException,business_exception_halder)
app.add_exception_handler(HTTPException,http_exception_halder)
app.add_exception_handler(RequestValidationError,validation_exception_halder)
#全局异常兜底，必须放在最后注册
app.add_exception_handler(Exception,global_exception_halder)

#  挂载静态的文件目录
app.mount("/uploads",StaticFiles(directory=UPLOAD_DIR),name="uploads")


@app.get("/")
def root():
    return{"message":"" }