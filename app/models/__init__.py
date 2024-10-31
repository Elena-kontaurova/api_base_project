from pydantic import BaseModel

class User(BaseModel):
    name : str
    id : int

class User_age(BaseModel):
    name : str
    age : int
    
    def is_adult(self):
        return self.age >= 18

class User_info_name(BaseModel):
    username : str
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
    name : str
    email : str
    age : int
    is_subscribed : bool | None = None 

class Product(BaseModel):
    product_id: int
    name : str
    category : str
    price : float


class Userpas(BaseModel):
    username : str
    password: str