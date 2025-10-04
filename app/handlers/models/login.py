from pydantic import BaseModel

class Login(BaseModel):
    phone_number: str
    password: str