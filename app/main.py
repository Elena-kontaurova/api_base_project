from fastapi import FastAPI
from fastapi.responses import FileResponse
from pydantic import BaseModel
from models.__init__ import User, User_age, User_info_name, User_message, Feedback
import json

app = FastAPI()

user = User(name = 'John Doe', id = 1)

fake_db = [{'username': 'vasya', 'user_info': 'любит колбасу'},
            {'username': 'katya', 'user_info': 'любит петь'}]

fake_users = {
    1: {'username': 'john_doe', 'email': 'john@example.com'},
    2: {'username': 'jane_smith', 'email': 'jane@example.com'}
}

@app.post("/feedback")
def post_feesback(feedback: Feedback):
    ''' Метод, который принимает отзывы от клеентов, записывает их в файл
    и вывод информацию, что их отзыв успешно принят. '''
    with open('feedback.json', 'a') as f:
        json.dump(feedback.__dict__, f)
    return {'message': f'Отзыв принят. Списибо тебе, {feedback.name}'}



@app.get('/email_user/{user_email_id}')
def read_users_email(user_email_id: int):
    ''' Получаем информацию - имя и почту пользователя по айди'''
    if user_email_id in fake_users:
        return fake_users[user_email_id]
    return {'error': 'Юзера с таким номером нет'}

@app.get("/email_user/")
def read_user_email(limit: int = 10):
    ''' Вывод ограниченно количества пользователей из списка fake_users'''
    return dict(list(fake_users.items())[:limit])

@app.get('/users_all_server')
async def get_all_users():
    ''' функция которая, будет выводить всех пользователей, которых мы добавили \
    в add_users и из списка fake_db'''
    return fake_db


@app.post("/add_user", response_model=User_info_name)
async def add_users(user_info_name: User_info_name):
    ''' мутод который будет записывать имя пользователя и инфорамцию о нем
    и обнавлять список fake_db'''
    fake_db.append({"username": user_info_name.username, 'user_info': user_info_name.user_info})
    return user_info_name


# @app.post('/add_user')
# async def add_users(username: str, user_info: str):
# ''' метод который, тоже записывал информацию и имя пользователя. 
# обнавлял список и добалял его в базу данных'''
#     fake_db.append({'username': username, 'user_info': user_info})
#     return {'message': 'user успешно добавлен в базу данных'}

@app.get('/userid/{user_id}')
async def search_user_by_id(user_id: int):
    ''' Ищем юзера по айди которые передаем в адресе строки'''
    return {'вы просили найти юзера с id': user_id}


@app.post("/user_age")
async def get_user_age(user_age: User_age):
    ''' метод который вывод имя, возраст и True - если пользователь 
    совершеннолетний, в ином случае - false. '''
    return {
        "name" : user_age.name,
        "age" : user_age.age,
        'is_adult' : user_age.is_adult()
    }


@app.get("/users_get_info")
async def get_users():
    '''вывод, получает информацию о пользователе
    тобишь - это имя и айди, которые хранятся в экземляре класса User'''
    return user

# class User(BaseModel):
#     username: str
#     message: str
# класс был перенесен в __init__.models - теперь User_message

@app.post('/user_message_get')
async def get_user_message(user_message: User_message):
    ''' Тут мы можем с переменной user, которая в себе содержит объекты класса
    User с соответвующими полями (и указанными типами), делать любую логику
    - например, мы можем сохранить информацию в базу данных
    - или передать их в другую функцию
    - или другое '''
    print(f'Мы получили от юзера {user_message.username} такое сообщение: {user_message.message}')
    return user_message

@app.get("/message_read")
async def read_message():
    ''' чтение сообщения от пользователя'''
    return {"message": "Hello World"}

# новый роут
@app.get("/custom")
def read_custom_message():
    ''' изменное сообщение'''
    return {"message": "This is a custom message!"}

@app.get("/html_read")
async def get_html():
    ''' вывод html файла'''
    return FileResponse('index.html')

@app.post("/calculate_sum")
async def get_sum(a: int, b: int):
    ''' получение суммы двух чисел'''
    return {"result": a+b}