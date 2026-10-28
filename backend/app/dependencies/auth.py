from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends,status,HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.utils.jwt import decode_access_token
from app.models.user import User
from app.common.exceptions import BusinessException
#from app.services.user_service import get_user_page_list


oauth2_scheme=OAuth2PasswordBearer(tokenUrl="/api/auth/login")
def get_current_user(token:str=Depends(oauth2_scheme),db:Session=Depends(get_db))->User:
    try:
        payload=decode_access_token(token)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="请检查携带的token是否正确")
    user_id=payload.get("user_id")  
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="无效的登录凭证")        
    user=db.query(User).filter(User.id==user_id).first()
    if not user or user.status!=1:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="用户被禁用")
    return user 

def get_current_admin(
        current_user:User=Depends(get_current_user)
    )->User:
    #判断jwt token内角色是否为admin
    if current_user.role!='admin':
        raise BusinessException(message="无权限访问",code=403)
    return current_user