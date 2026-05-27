from datetime import datetime
from typing import Any, Optional
import re

from fastapi import FastAPI
from pydantic import BaseModel, EmailStr, Field, ValidationError, field_validator, model_validator

app = FastAPI(title="User Registration Service")


class UserRegistration(BaseModel):
    username: str = Field(min_length=3, max_length=20)
    email: EmailStr
    password: str = Field(min_length=8)
    password_confirm: str = Field(exclude=True)
    age: int = Field(ge=18, le=120)
    registration_date: datetime = Field(default_factory=datetime.now)
    full_name: str = Field(min_length=2)
    phone: str

    @field_validator("username")
    @classmethod
    def validate_username(cls, v: str) -> str:
        if not re.fullmatch(r"[a-zA-Z0-9_]+", v):
            raise ValueError("Имя пользователя может содержать только латинские буквы, цифры и символ подчёркивания")
        return v

    @field_validator("password")
    @classmethod
    def validate_password(cls, v: str) -> str:
        if not re.search(r"\d", v):
            raise ValueError("Пароль должен содержать хотя бы одну цифру")
        if not re.search(r"[A-Z]", v):
            raise ValueError("Пароль должен содержать хотя бы одну заглавную букву")
        if not re.search(r"[a-z]", v):
            raise ValueError("Пароль должен содержать хотя бы одну строчную букву")
        return v

    @model_validator(mode="after")
    def validate_passwords_match(self) -> "UserRegistration":
        if self.password != self.password_confirm:
            raise ValueError("Пароли не совпадают")
        return self

    @field_validator("full_name")
    @classmethod
    def validate_full_name(cls, v: str) -> str:
        if not v[0].isupper():
            raise ValueError("Имя должно начинаться с заглавной буквы")
        return v

    @field_validator("phone")
    @classmethod
    def validate_phone(cls, v: str) -> str:
        if not re.fullmatch(r"\+\d-\d{3}-\d{2}-\d{2}", v):
            raise ValueError("Телефон должен быть в формате +X-XXX-XX-XX")
        return v


def register_user(data: dict) -> UserRegistration | list[dict]:
    try:
        return UserRegistration(**data)
    except ValidationError as e:
        return [
            {
                "field": " -> ".join(str(loc) for loc in error["loc"]),
                "message": error["msg"],
            }
            for error in e.errors()
        ]


class TreeNode(BaseModel):
    data: Any
    child: Optional["TreeNode"] = None


TreeNode.model_rebuild()


def build_tree(depth: int, data: Any = "any_data") -> TreeNode:
    if depth <= 1:
        return TreeNode(data=data)
    return TreeNode(data=data, child=build_tree(depth - 1, data))


@app.post("/register")
def register_endpoint(data: dict):
    result = register_user(data)
    if isinstance(result, list):
        return {"success": False, "errors": result}
    return {"success": True, "user": result.model_dump()}


@app.get("/tree/{depth}")
def tree_endpoint(depth: int, data: Any = "any_data"):
    return build_tree(depth, data).model_dump()
