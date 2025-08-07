from enum import Enum

from pydantic import BaseModel, EmailStr, Field, validator, field_validator, field_serializer
import re

from pydantic import ValidationInfo


class Role(str, Enum):
    USER = "USER"
    MANAGER = "MANAGER"
    ADMIN = "ADMIN"

class SUserRegister(BaseModel):
    email: EmailStr = Field(..., description="Электронная почта")

    password: str = Field(..., min_length=5, max_length=250, description="Пароль, от 5 до 50 знаков")
    password_two: str = Field(..., exclude=True, min_length=5, max_length=250, description="Пароль, от 5 до 50 знаков")

    phone_number: str = Field(..., description="Номер телефона в международном формате, начинающийся с '+'")
    first_name: str = Field(..., min_length=3, max_length=50, description="Имя, от 3 до 50 символов")
    last_name: str = Field(..., min_length=3, max_length=50, description="Фамилия, от 3 до 50 символов")
    role: Role = Role.USER

    @field_validator("password_two")
    def passwords_match(cls, value: str, info: ValidationInfo) -> str:
        if "password" in info.data and value != info.data["password"]:
            raise ValueError("Пароли не совпадают")
        return value

    @field_validator("role")
    @classmethod
    def role(cls, value: str) -> str:
        if not value == Role.USER.value:
            raise ValueError("Роли назначает администратор")

    @field_validator("phone_number")
    @classmethod
    def validate_phone_number(cls, value: str) -> str:
        if not re.match(r'^\+\d{5,15}$', value):
            raise ValueError('Номер телефона должен начинаться с "+" и содержать от 5 до 15 цифр')
        return value

    # @field_serializer("role")
    # def serialize_group(self, role: Role, _info):
    #     return role.name

class SUserAuth(BaseModel):
    email: EmailStr = Field(..., description="Электронная почта")
    password: str = Field(..., min_length=5, max_length=50, description="Пароль, от 5 до 50 знаков")

class SUserUpdRoles(BaseModel):
    user_id: int
    is_admin: bool = Field(..., description="Роль администратор")

class SUser(BaseModel):
    email: EmailStr = Field(..., description="Электронная почта")
    phone_number: str = Field(..., description="Номер телефона в международном формате, начинающийся с '+'")
    first_name: str = Field(..., min_length=3, max_length=50, description="Имя, от 3 до 50 символов")
    last_name: str = Field(..., min_length=3, max_length=50, description="Фамилия, от 3 до 50 символов")

class SUpdateUser(BaseModel):
    email: EmailStr = Field(..., description="Электронная почта")
    # password: str = Field(..., min_length=5, max_length=250, description="Пароль, от 5 до 50 знаков")
    # password_two: str = Field(...,exclude=True, min_length=5, max_length=250, description="Пароль, от 5 до 50 знаков")

    phone_number: str = Field(..., description="Номер телефона в международном формате, начинающийся с '+'")
    first_name: str = Field(..., min_length=3, max_length=50, description="Имя, от 3 до 50 символов")
    last_name: str = Field(..., min_length=3, max_length=50, description="Фамилия, от 3 до 50 символов")


    # @field_validator("password_two")
    # def passwords_match(cls, v: str, info: ValidationInfo) -> str:
    #     if "password" in info.data and v != info.data["password"]:
    #         raise ValueError("passwords do not match")
    #     return v

    @field_validator("phone_number")
    @classmethod
    def validate_phone_number(cls, value: str) -> str:
        if not re.match(r'^\+\d{5,15}$', value):
            raise ValueError('Номер телефона должен начинаться с "+" и содержать от 5 до 15 цифр')
        return value

    def to_dict(self) -> dict:
        data = {#'id': self.id,
                'email': self.email,
                # 'password': self.password,
                'phone_number': self.phone_number,
                'first_name': self.first_name,
                'last_name': self.last_name}
        # Создаем копию словаря, чтобы избежать изменения словаря во время итерации
        filtered_data = {key: value for key, value in data.items() if value is not None}
        return filtered_data

class SURole(BaseModel):
    id: int
    role: str

class UserLoginSchema(BaseModel):
    id: int
    access_token: str

