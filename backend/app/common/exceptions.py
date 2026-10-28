import logging

from fastapi import Request,HTTPException
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from fastapi.encoders import jsonable_encoder

from app.common.response import Response
from app.config import CORS_ORIGINS

logger=logging.getLogger(__name__)

def cors_headers(request:Request)->dict:
    """补齐跨域响应头

    Exception的处理器由ServerErrorMiddleware执行，它在CORSMiddleware外层，
    这条路径的响应不经过CORS中间件，不手动补头浏览器会把500当成跨域错误，
    前端只能看到“网络异常”，拿不到真正的错误信息。
    """
    origin=request.headers.get("origin")
    if origin in CORS_ORIGINS:
        return {
            "Access-Control-Allow-Origin":origin,
            "Access-Control-Allow-Credentials":"true",
            "Vary":"Origin"
        }
    return {}

class BusinessException(Exception):
    """自定义的业务异常"""
    def __init__(self,message:str,code:int=500):
        self.message=message
        self.code=code
        super().__init__(message)

async def business_exception_halder(request:Request,exc:BusinessException):
    """自定义业务异常处理器"""
    return JSONResponse(
        status_code=200,
        content=Response.error(code=exc.code,message=exc.message)
        .model_dump()
    )

async def http_exception_halder(request:Request,exc:HTTPException):
    """http异常处理器"""
    return JSONResponse(
        status_code=exc.status_code,
        content=Response.error(code=exc.status_code,message=exc.detail)
        .model_dump(),
        headers=exc.headers
    )

async def validation_exception_halder(request:Request,exc:RequestValidationError):
    """参数异常处理器"""
    return JSONResponse(
        status_code=422,
        content=Response.error(code=422,message="请求参数校验错误",
                               data=jsonable_encoder(exc.errors()))
        .model_dump()
    )

async def global_exception_halder(request:Request,exc:Exception):
    """全局异常处理器"""
    #把原始异常和堆栈打进日志，否则返回500时无从排查
    logger.error("未捕获异常",exc_info=exc)
    return JSONResponse(
        status_code=500,
        content=Response.error(code=500,message="服务器内部错误")
        .model_dump(),
        headers=cors_headers(request)
    )