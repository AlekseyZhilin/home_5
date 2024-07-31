from pydantic import BaseModel, Field
from typing import List

LEN_USER_NAME = 32


class Item(BaseModel):
    id: int
    name: str = Field(title="Name", max_length=50)
    description: str = Field(title="Description", default=None, max_length=1024)
    price: float = Field(title="Price", gt=0.1, le=1_000_000)


class ItemIn(BaseModel):
    name: str = Field(max_length=50)
    description: str = Field(default=None, max_length=1024)
    price: float = Field(gt=0.1, le=1_000_000)


class User(BaseModel):
    id: int
    first_name: str = Field(max_length=LEN_USER_NAME)
    last_name: str = Field(max_length=LEN_USER_NAME)
    email: str = Field(max_length=128)
    password: str = Field(min_length=4, max_length=16)


class UserIn(BaseModel):
    first_name: str = Field(max_length=LEN_USER_NAME)
    last_name: str = Field(max_length=LEN_USER_NAME)
    email: str = Field(max_length=128)
    password: str = Field(min_length=4, max_length=16)


class Order(BaseModel):
    id: int
    items: List[Item]
    user: User
