from sqlalchemy.orm import Session
from app.schemas.auth import LoginRequest,RegisterRequest

from app.schemas.user import UserResponse
from sqlalchemy.orm import Session
from app.models.user import User
from app.utils.password import verify_password,hash_password
from app.utils.jwt import create_access_token
from app.common.exceptions import BusinessException
from app.schemas.auth import LoginResponse

def login_service(db:Session,data:LoginRequest):
    user=db.query(User).filter(User.username==data.username).first()

    if not user or not verify_password(data.password,user.password):
        raise BusinessException(code=400,message="账号或密码错误")
    
    if user.status!=1:
        raise BusinessException(code=403,message="账号被禁用")
    
    token=create_access_token(user.id)
    return LoginResponse(token=token,user=UserResponse.model_validate(user))

def register_service(db:Session,data:RegisterRequest):
    user=db.query(User).filter(User.username==data.username).first()
    if user:
        raise BusinessException(code=400,message="账号已存在")

    user_model=User(
        username=data.username,
        password=hash_password(data.password),
        name=data.name or data.username,
        role="student",
        status=1
    )
    db.add(user_model)
    db.commit()