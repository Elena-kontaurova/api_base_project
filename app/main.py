from fastapi import Cookie,  FastAPI, File, UploadFile, BackgroundTasks, Response, status
from fastapi.responses import FileResponse
from pydantic import BaseModel
from models.__init__ import User, User_age, User_info_name, \
                            User_message, Feedback, Item, UserCreate, \
                            Product, Userpas
import json
from typing import Annotated
from datetime import datetime
from string import ascii_letters
from random import sample
import uvicorn


app = FastAPI()

product_spisok = {
    1: Product(
        product_id=1, \
        name = 'Smarthon', \
        category='Electronica', \
        price= 123.00),
    2: Product(
        product_id = 2, \
        name = 'Phone Case', \
        category= 'Accessories', \
        price = 500.00),
    3: Product(
        product_id= 3, \
        name = 'Iphone', \
        category= 'Electronica', \
        price = 235.00),
    4: Product(
        product_id= 4, \
        name = 'Headphonees', \
        category= 'Accessories', \
        price= 875.00), 
    5: Product(
        product_id= 5, \
        name= 'Smartwatch', \
        category= 'Electronica', \
        price = 120.00
    ),
}

@app.get('/product/{product_id}')
async def get_product(product_id: int):
    ''' Поиск товара по айди'''
    if product_id in product_spisok:
        return product_spisok[product_id]
    return "Товар c данным айди не найден"

@app.get('/products/search')
async def find_tovar(keyword: str, category : str, limit: int = 10):
    ''' Поиск товара по ключу (имени) и категории товара'''
    if category:
        res = [p for p in product_spisok if p['category'].lower() == category.lower() and 
            keyword.lower() in p['name'].lower()]
    else:
        res = [p for p in product_spisok if keyword.lower() in p['name'].lower()]
    return res[:limit]

@app.post('/create_user')
async def create_user(usercreate : UserCreate):
    ''' Маршрут который принимаем json в соответвии с моделью UserCreate
    Функция ждя обработки входящих пользовательских данных и возврата ответа
    с полученной информацией '''
    return usercreate

fake_items_dp = [{'item_name': 'Foo'}, {'item_name': 'Bar'}, {'item_name': 'Baz'}]

@app.get('/items_request/')
async def read_item(skip: int = 0, limit = 10):
    ''' Обработка параметров запроса'''
    return fake_items_dp[skip: skip + limit]

@app.post('/items_create/')
async def create_item(item: Item):
    return item

@app.post('/items/')
async def create_item(item: Item) -> Item:
    ''' Проверка всех запросов на соответвие этой модели'''
    return item

@app.get('/items/')
async def read_items() -> list[Item]:
    ''' Возращем список, который будет содержать pydantic модели'''
    return [
        Item(name = 'Portal Gun', price=42.0),
        Item(name='Plumbus', price=32.0)
    ]

@app.post('/files/')
async def create_file(file: Annotated[bytes, File()]):
    ''' определение длинны файла'''
    return {'file_size': len(file)}

@app.post('/uploadfile/')
async def create_upload_file(file: UploadFile):
    ''' создаем загружаемый файл'''
    return {'filename': file.filename}


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

def write_notificarion(email: str, message = ''):
    with open('log.txt', mode='w') as email_file:
        content = f'Предупреждение для {email}:{message}'
        email_file.write(content)

@app.post('/send-notification/{email}')
async def send_notofication(email: str, background_tasks: BackgroundTasks):
    ''' Фоновая задача - отправка уведовления на email
    Асинхронный обработчик'''
    background_tasks.add_task(write_notificarion, email, message='Какое то уведомление')
    return {"message": 'Уведовление отправленно в фоновом режиме'}

@app.get('/items')
async def read_items(ads_id: str | None = Cookie(default=None)):
    ''' Использование Cookie'''
    return {'ads_id': ads_id}

@app.get('/')
def root(last_visit = Cookie()):
    ''' Использование Cookie'''
    return {'Последний визит': last_visit}

@app.get('/')
def get_cookie(response: Response):
    ''' Получаем текущею дату и время - последний визит с помощью Cookie'''
    now = datetime.noow().strftime('%d/%m/%Y, %H:%M:%S')
    response.set_cookie(key='последний визит', value=now)
    return {'message': 'куки установленны'}



db = {f'user{n}': f'pass{n}' for n in range(5)}

tokens = {}

def gen_token():
    return ''.join(sample(ascii_letters, 16))

@app.get('/user')
def gutuser(response: Response, session_token=Cookie()):
    if not session_token or session_token not in tokens:
        response.status_code = status.HTTP_401_UNAUTHORIZED
        return {'message': "Unauthorized"}
    userename = tokens[session_token]
    return {userename: db[userename]}

@app.post('/login')
def login(userpas: Userpas, responce: Response):
    if userpas.username not in db:
        responce.status_code = status.HTTP_404_NOT_FOUND
        return {'error': 'пользователь не найден'}
    if db[userpas.username] != userpas.password:
        responce.status_code = status.HTTP_401_UNAUTHORIZED
        return {'error': 'неверный пароль'}
    token = gen_token()
    responce.set_cookie(key='session_token', value = token, httponly=True)
    tokens[token] = userpas.username
    return {'userpass': userpas}

@app.post('/signup')
def signup(userpass: Userpas, response: Response):
    if userpass.username in db:
        response.status_code = status.HTTP_409_CONFLICT
        return {'error': 'Имя пользователя занято'}
    db[userpass.username] = userpass.password
    return {'message': f'аккаунт {userpass.username} отличный'}

@app.post('/signout')
def signout(responce: Response, session_token = Cookie()):
    if not session_token or session_token not in tokens:
        return
    tokens.pop(session_token, None)
    responce.delete_cookie('session_token', httponly=True)
    return {'message': 'Вы успешно вышли из системы'}

@app.get('/users')
def users():
    return db

@app.get('/t')
def get_t():
    return tokens

if __name__ == '__main__':
    uvicorn.run(
        'main:app',
        host = 'localhost',
        port = 8000,
        reload = True
    )