from pydantic import BaseModel,Field,field_validator
from app.schemas.user import UserResponse

class PasswordMixin(BaseModel):
    """带密码的请求体的公共约束

    bcrypt只处理前72字节，超长会直接抛ValueError变成500，所以在入口就拦成422。
    注意是按字节算的：中文一个字符占3字节，所以24个汉字就会超。
    """
    password:str

    @field_validator("password")
    @classmethod
    def password_within_bcrypt_limit(cls,value:str)->str:
        if len(value.encode("utf-8"))>72:
            raise ValueError("密码不能超过72字节")
        return value

class LoginRequest(PasswordMixin):
    username:str=Field(max_length=50)

class LoginResponse(BaseModel):
    token:str
    user:UserResponse

class RegisterRequest(PasswordMixin):
    username:str=Field(max_length=50)
    name:str|None=None
    