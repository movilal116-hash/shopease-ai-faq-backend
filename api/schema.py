from pydantic import BaseModel

class UserRequest(BaseModel):
    request: str


class AIResponse(BaseModel):
    ans: str

