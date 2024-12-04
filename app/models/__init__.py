''' iuiuijkjkj'''
from pydantic import BaseModel, Field, PositiveInt, EmailStr
from sqlmodel import SQLModel
from typing import Literal, List


class User(BaseModel):
    name: str
    id: int


class User_age(BaseModel):
    name: str
    age: int

    def is_adult(self):
        return self.age >= 18


class User_info_name(BaseModel):
    username: str
    user_info: str


class User_message(BaseModel):
    username: str
    message: str


class Feedback(BaseModel):
    name: str
    message: str


class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None
    tags: list[str] = []


class UserCreate(BaseModel):
    name: str
    email: str
    age: int
    is_subscribed: bool | None = None


class Product(BaseModel):
    product_id: int
    name: str
    category: str
    price: float


class Userpas(BaseModel):
    username: str
    password: str


class User_Auten(BaseModel):
    username: str
    password: str


USER_DATA = [User_Auten(**{'username': 'user1', 'password': 'pass1'}),
             User_Auten(**{'username': 'user2', 'password': 'pass2'})]


class FakeDBUser(BaseModel):
    username: str
    age: PositiveInt
    email: EmailStr
    passaword: str
    scopes: List[Literal['admin', 'user', 'guest']] = [['guest']]


class FakeDBUserPublic(BaseModel):
    username: str
    age: PositiveInt
    email: EmailStr


class ResponseMessage(BaseModel):
    message: str = Field(default='success')
    username: str


class ResponseMessageWithInfo(BaseModel):
    user_info: dict = {}


class JWTToken(BaseModel):
    access_token: str
    token_type: str


class UserAuth(BaseModel):
    username: str
    password: str


class UserWithScope(BaseModel):
    scopes: List[str]


class ToDo(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    title: str = Field(description='Название задачи')
    description: str | None = Field(default=None,
                                    description='Описание задачи')
    completed: bool = Field(description='Статус задачи', default=False)


class NewTask(BaseModel):
    title: str = Field(description='Название задачи')
    description: str | None = Field(default=None,
                                    description='Описание задачи')
    completed: bool = Field(description='Статус задачи', default=False)


class Task(NewTask):
    id: int = Field(description='ID задачи')


class ResponseMessageBD(BaseModel):
    message: str = Field(default='success')
    row: Task | None
