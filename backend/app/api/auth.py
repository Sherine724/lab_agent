#专门用来做验证客户登录，注册，验证密码
from fastapi import APIRouter,Depends
from app.schemas.auth import LoginRequest,RegisterRequest
from sqlalchemy.orm import Session
from app.database import get_db
from app.common.response import Response
from app.services.auth_service import login_service,register_service

router=APIRouter(prefix="/auth",tags=["权限验证"])
@router.post("/login")
def login(data:LoginRequest,db:Session=Depends(get_db)):
    result=login_service(db,data)
    return Response.success(
        message="登录成功",
        data=result
    )

@router.post("/register")
def register(data:RegisterRequest,db:Session=Depends(get_db)):
    register_service(db,data)
    return Response.success(
        message="注册成功"
    )

