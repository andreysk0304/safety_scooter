from pydantic import BaseModel

class Registration(BaseModel):
    phone_number: str
    password: str