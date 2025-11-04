from datetime import date, datetime
from pydantic import BaseModel, EmailStr, field_validator
from typing import Optional

class Address(BaseModel):
    flat_no: Optional[str] = None
    area: Optional[str] = None
    city: str
    state: str
    country: str
    pin_code: str

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    first_name: str
    last_name: str
    dob: date
    gender: str
    address: Address

class UserProfile(BaseModel):
    email: EmailStr
    first_name: str
    last_name: str
    dob: date
    age: int
    gender: str
    address: Address

    @field_validator('age', mode='before')
    def calculate_age(cls, v, info):
        today = date.today()
        user_dob = info.data.get('dob')
        return today.year - user_dob.year - ((today.month, today.day) < (user_dob.month, user_dob.day))

class SportStat(BaseModel):
    metric: str
    value: str
    source: str

class Sport(BaseModel):
    id: int
    name: str
    description: str
    stats: list[SportStat]