from pydantic import BaseModel, field_validator


class Registration(BaseModel):
    phone_number: str
    password: str


    @field_validator('phone_number')
    def validate_phone_number(cls, v):
        if not v or not v.strip():
            raise ValueError("Номер телефона не может быть пустым.")

        if not v.startswith('+'):
            raise ValueError("Номер телефона должен начинаться с '+'.")

        digits = ''.join([ch for ch in v if ch.isdigit()])

        if len(digits) < 10 or len(digits) > 15:
            raise ValueError("Номер телефона должен содержать от 10 до 15 цифр.")

        return v


    @field_validator('password')
    def validate_password(cls, v):
        if not v or not v.strip():
            raise ValueError("Пароль не может быть пустым.")

        if len(v) < 8:
            raise ValueError("Пароль должен содержать не менее 8 символов.")

        return v