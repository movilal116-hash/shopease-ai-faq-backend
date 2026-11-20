# Pydantic models

from pydantic import BaseModel, EmailStr

class UserRequest(BaseModel):
    request: str


class AIResponse(BaseModel):
    ans: str

### We need schemas to handle the registration and login requests.
class UserRegister(BaseModel):
    name: str
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: int
    name: str
    email: str

    class config:
        from_attributes=True

class Token(BaseModel):
    access_token:str
    token_type:str