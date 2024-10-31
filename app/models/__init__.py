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