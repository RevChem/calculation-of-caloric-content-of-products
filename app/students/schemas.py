from datetime import datetime, date
from typing import Optional
import re

from pydantic import BaseModel, Field, field_validator, EmailStr, ConfigDict, model_validator


class SStudent(BaseModel):
    # model_config - нужен, чтобы Pydantic мог создавать модель из объекта с атрибутами
    model_config = ConfigDict(from_attributes=True)
    id: int
    phone_number: str = Field(..., description="Номер телефона в международном формате, начинающийся с '+'")
    first_name: str = Field(..., min_length=1, max_length=50, description="Имя студента, от 1 до 50 символов")
    last_name: str = Field(..., min_length=1, max_length=50,
                           description="Фамилия студента, от 1 до 50 символов")
    date_of_birth: date = Field(..., description="Дата рождения студента в формате ГГГГ-ММ-ДД")
    email: EmailStr = Field(..., description="Электронная почта студента")
    address: str = Field(..., min_length=4, max_length=200,
                         description="Адрес студента, не более 200 символов")
    enrollment_year: int = Field(..., ge=2002, description="Год поступления должен быть не меньше 2002")
    major_id: int = Field(..., ge=1, description="ID специальности студента")
    course: int = Field(..., ge=1, le=5, description="Курс должен быть в диапазоне от 1 до 5")
    special_notes: Optional[str] = Field(None, max_length=500,
                                         description="Дополнительные заметки, не более 500 символов")
    photo: Optional[str] = Field(None, max_length=100, description="Фото студента")
    major: Optional[str] = Field(..., description="Название факультета")
    food_id: Optional[int] = Field(None, description="ID предпочтений в еде")


    @model_validator(mode='after')
    def validate_phone_number(self):
        if not re.match(r'^\+\d{1,15}$', self.phone_number):
            raise ValueError('Номер телефона должен начинаться с "+" и содержать от 1 до 15 цифр')
        return self


    @model_validator(mode='after')
    def validate_date_of_birth(self):
        if self.date_of_birth and self.date_of_birth >= date.today():
            raise ValueError('Дата рождения должна быть в прошлом')
        return self


class SStudentAdd(BaseModel):
    phone_number: str = Field(..., description="Номер телефона в международном формате, начинающийся с '+'")
    first_name: str = Field(..., min_length=3, max_length=50, description="Имя студента, от 3 до 50 символов")
    last_name: str = Field(..., min_length=3, max_length=50,
                           description="Фамилия студента, от 3 до 50 символов")
    date_of_birth: date = Field(..., description="Дата рождения студента в формате ГГГГ-ММ-ДД")
    email: EmailStr = Field(..., description="Электронная почта студента")
    address: str = Field(..., min_length=10, max_length=200,
                         description="Адрес студента, не более 200 символов")
    enrollment_year: int = Field(..., ge=2002, description="Год поступления должен быть не меньше 2002")
    major_id: int = Field(..., ge=1, description="ID специальности студента")
    course: int = Field(..., ge=1, le=5, description="Курс должен быть в диапазоне от 1 до 5")
    special_notes: Optional[str] = Field(None, max_length=500,
                                         description="Дополнительные заметки, не более 500 символов")
    food_id: Optional[int] = Field(None, ge=1, description="ID предпочтений в еде")

    @model_validator(mode='after')
    def validate_phone_number(self):
        if not re.match(r'^\+\d{1,15}$', self.phone_number):
            raise ValueError('Номер телефона должен начинаться с "+" и содержать от 1 до 15 цифр')
        return self


    @model_validator(mode='after')
    def validate_date_of_birth(self):
        if self.date_of_birth and self.date_of_birth >= date.today():
            raise ValueError('Дата рождения должна быть в прошлом')
        return self
