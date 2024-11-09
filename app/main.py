from fastapi import Cookie,  FastAPI, File, UploadFile, BackgroundTasks, Response, status, \
                    Header, HTTPException, Depends, Request, Security, Body, Path
from fastapi.exceptions import HTTPException
from fastapi.security import OAuth2AuthorizationCodeBearer, OAuth2PasswordRequestForm, SecurityScopes
from fastapi.responses import FileResponse
from pydantic import BaseModel
from models.__init__ import User, User_age, User_info_name, \
                            User_message, Feedback, Item, UserCreate, \
                            Product, Userpas, User_Auten, USER_DATA, \
                            JWTToken, UserAuth, UserWithScope, ResponseMessage, \
                            ResponseMessageWithInfo, FakeDBUser, FakeDBUserPublic
from pydantic import ValidationError
from fastapi.security import HTTPBasic, HTTPBasicCredentials, HTTPAuthorizationCredentials, HTTPBearer
import json
import jwt
from typing import Annotated, Any, NoReturn
from datetime import datetime, timezone, timedelta
from string import ascii_letters
from random import sample
import uvicorn
from datetime import datetime, timedelta, timezone


app = FastAPI()


SECRET = 'secret'
ALGORITHMS = 'HS256'
EXPIRE = 1

security = HTTPBasic()


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
async def read_item(skip: int = 0, limit : int = 10):
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
    ''' Получение токена'''
    return ''.join(sample(ascii_letters, 16))

@app.get('/user')
def gutuser(response: Response, session_token=Cookie()):
    '''Провверка пользователя на авторизованность в системе '''
    if not session_token or session_token not in tokens:
        response.status_code = status.HTTP_401_UNAUTHORIZED
        return {'message': "Unauthorized"}
    userename = tokens[session_token]
    return {userename: db[userename]}

@app.post('/login')
def login(userpas: Userpas, responce: Response):
    ''' регистрация пользователя'''
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
    ''' Вход в систему'''
    if userpass.username in db:
        response.status_code = status.HTTP_409_CONFLICT
        return {'error': 'Имя пользователя занято'}
    db[userpass.username] = userpass.password
    return {'message': f'аккаунт {userpass.username} отличный'}

@app.post('/signout')
def signout(responce: Response, session_token = Cookie()):
    ''' Выход из системы'''
    if not session_token or session_token not in tokens:
        return
    tokens.pop(session_token, None)
    responce.delete_cookie('session_token', httponly=True)
    return {'message': 'Вы успешно вышли из системы'}

@app.get('/users')
def users():
    ''' Пользователи'''
    return db

@app.get('/t')
def get_t():
    ''' вывод токена'''
    return tokens

''' запуск кода'''
if __name__ == '__main__':
    uvicorn.run(
        'main:app',
        host = 'localhost',
        port = 8000,
        reload = True
    )

@app.get('/items/')
async def read_items(x_token: Annotated[str | None, Header()] = None):
    return {'X-token values': x_token}

@app.get('/')
def root(user_agent: str=Header()):
    return {'User-Agent': user_agent}

@app.get('/')
def root():
    data = 'Привет отсюда'
    return Response(content=data, media_type='text/plain', headers={'Secret-Code':'123459'})

@app.get('/')
def root(responce: Response):
    responce.headers['Secret-Code'] = '123459'
    return {'message': 'Привет из моего api'}


@app.get('/headers')
def root(user_agent: Annotated[str | None, Header()] = None, 
        accept_language: Annotated[str | None, Header()] = None):
    if user_agent is None or accept_language is None:
        raise HTTPException(
            status_code=400,
            detail='Must be User-Agent and Accept-Language'
        )
    if accept_language != 'en-US, en; 1=0.9, es; q=0.8':
        raise HTTPException(
            status_code=400,
            detail='Accept-Language id bad format'
        )
    return {
        'User-Agent': user_agent,
        'Accept-Language': accept_language
    }

# Аетинтификация и авторизация
# Реализация базовой аутентификации

def authenticate_user(creadentials: HTTPBasicCredentials = Depends(security)):
    user_auten = get_user_from_db(creadentials.username)
    if user is None or user_auten.password != creadentials.password:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid credentials')
    return user_auten

def get_user_from_db(username: str):
    for user_auten in USER_DATA:
        if user_auten.username == username:
            return user_auten
    return None
    
@app.get('/protected_resource/')
def get_protected_resource(user_auten: User_Auten = Depends(authenticate_user)):
    return {'message': 'You have access to the protected resourse!', 'user_info': user_auten}

@app.get('/login')
async def user_login(user_auten: User_Auten = Depends(authenticate_user)):
    return {'message': 'You goy my secret. Welcome!'}

@app.get('/logout')
async def user_logout():
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Logging out...',
                        headers={'WWW-Authenticate': 'Basic'})

# аутентификация на основе JWT

def generate_token():
    jwt_token = jwt.encode(
    {'exp': datetime.now(tz = timezone.utc) + timedelta(minutes=EXPIRE)},
    SECRET,
    algorithm = ALGORITHMS
)
    return jwt_token

def check_token(token: str):
    try:
        decoded = jwt.decode(token, SECRET, algorithms = [ALGORITHMS])
        if decoded:
            return {'message': 'access granted'}
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Signature had expired')
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid token')
    
def get_user_from_db_1(username: str):
    for user_auten in USER_DATA:
        if user_auten.username == username:
            return user
    return None

@app.post('/login')
async def basic_login(user_auten: User_Auten = Depends(authenticate_user)):
    token = generate_token()
    return {'access_token': token}

@app.get('/protected_resourse')
async def login_with_jwt_token(credentials: HTTPAuthorizationCredentials = Depends(HTTPBearer)):
    token = credentials.credentials
    return {'message': check_token(token)}

# управление доступом на основе ролей

oauth2 = OAuth2AuthorizationCodeBearer(
    tokenUrl ='login',
    scopes={
        'admin': 'grant all privileges',
        'user': 'read and update',
        'guest': 'read only'
    }
)

SECRET_KEY = 'a67a913a5443d6a2b18edaafbafd229617fb3d7d7da30582d86c240771f7'
EXPIRES = timedelta(seconds=60)
ALGORITHM = 'HS256'

fake_db_1 = {
    'john': {
        'username': 'john',
        'age': 40,
        'email': 'john@google.com',
        'passoword': 'securpassword123',
        'scopes': ['admin']
    },
    'alica': {
        'username': 'alica',
        'age': 29,
        'email': 'alica@google.com',
        'password': 'securepassword456',
        'scopes': ['user']
    },
    'ryan': {
        'username': 'ryan', 
        'age': 35,
        'email': 'ryan@google.com',
        'password': 'securepassword789',
        'scopes': ['guest']
    }
}

def create_jwt(data: dict[str, Any]) -> JWTToken:
    payload = data.copy()
    payload.update({'exp': datetime.now(tz=timedelta.utc)+ EXPIRES}) 
    token = jwt.encode(payload, SECRET_KEY, alorithm = ALGORITHM)
    return token

def user_authenticate(
        user: Annotated[OAuth2PasswordRequestForm, Depends()]
) -> NoReturn:
    if user.username not in fake_db_1:
        raise HTTPException(
            status_code= status.HTTP_401_UNAUTHORIZED, 
            detail='Пользователь не найден',
            headers={'WWW-Authenticate': 'Bearer'}
        )
    
    if user.password != fake_db_1[user.username]['password']:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail='Неправильный пароль',
            headers={'WWW-Authenticate': 'Bearer'}
        )
    

def check_credentials(
        scopes: SecurityScopes,
        token: Annotated[str, Depends(oauth2)]
):
    if scopes.scopes:
        header = f'Bearer scope= "{scopes.scope_str}"'
    else:
        header = 'Bearer'
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, 
        detail='Не удалось проверить учетные данные',
        headers={'WWW-Authenticate': header},
    )

    try:
        decoded_token =jwt.decode(token, SECRET_KEY, leeway = 0, algorithm = [ALGORITHM])
        username = decoded_token.get('sub')
        if not username:
            raise credentials_exception
    except (ValidationError):
        raise credentials_exception
    
    user = get_user_db(username)
    user_scopy = set(user.scopes)
    if not user:
        raise credentials_exception
    elif not user.scopes.issubset(set(scopes.scopes)):
        raise HTTPException(
            status_code= status.HTTP_401_UNAUTHORIZED, 
            detail='Недостаточно разрешений',
            headers={'WWW-Authenticate': header},
        )
    return user


def get_user_db(username: str):
    if username in fake_db_1:
        return UserWithScope(**fake_db_1.get(username))
    
def get_user_info(username: str):
    if username in fake_db_1:
        return FakeDBUserPublic(**fake_db_1[username])
    
def add_user_db(new_user: FakeDBUser, username: str):
    fake_db_1.update({username: new_user.model_dump()})

def delete_user_db(username: str):
    if username not in fake_db_1:
        raise ValueError('Пользователь не найден')
    del fake_db_1[username]

def update_user_db(username: str, user_data: dict):
    if username not in fake_db_1:
        raise ValueError('Невозсожно обнавить')
    fake_db_1[username].update(user_data)


@app.post('/login', dependencies=[Depends(user_authenticate)])
async def login_user(
    login_data: Annotated[OAuth2PasswordRequestForm, Depends()]
) -> JWTToken:
    return JWTToken(**{'access_token': create_jwt({'sub': login_data.username}),
                    'token_type': 'bearer'})

@app.get('/prorected_resourse', response_model=ResponseMessage)
async def get_resourse(
    user: Annotated[UserAuth, Security(check_credentials, scopes=['admin', 'user'])]
) -> ResponseMessage:
    return ResponseMessage(message='Доступ предоставлен', username=user.username)


@app.post('/user/{username}')
def add_user(
    user: Annotated[UserAuth, Security(check_credentials, scopes=['admin'])],
    username: Annotated[str, Path()],
    new_user: Annotated[FakeDBUser, Body()]
) -> ResponseMessage:
    add_user_db(new_user, username)
    return ResponseMessage(message='Новый пользователь добавлен', username=username)

@app.delete('/user/{username}')
def delete_user(
    user: Annotated[UserAuth, Security(check_credentials, scopes=['admin'])],
    username: Annotated[str, Path]
) -> ResponseMessage:
    delete_user_db(username)
    return ResponseMessage(message='Пользователь удален')

@app.patch('/user/{username}')
def update_user(
    user: Annotated[UserAuth, Security(check_credentials, scopes=['admin', 'user'])],
    username: Annotated[str, Path()],
    new_data: Annotated[dict, Body()]
) -> ResponseMessage:
    if user.username != username:
        if 'admin' not in user.scopes:
            raise HTTPException(
                status_code= status.HTTP_401_UNAUTHORIZED,
                detail='Недостаточно разрешений')
    update_user_db(username, new_data)
    return ResponseMessage(message='Пользователь обнавлен', username=username)

@app.get('/user/{username}')
def get_user(
    user: Annotated[UserAuth, Security(check_credentials, scopes=['admin', 'user', 'guest'])],
    username: Annotated[str, Path()]
) -> ResponseMessage:
    user = get_user_info(username)
    return ResponseMessageWithInfo(
        message = 'Полученнная информация о пользователе',
        username = user.username,
        user_info=user.model_dump()
    )

if __name__ == '__main__':
    uvicorn.run(
        'main:app',
        host = '127.0.0.1',
        port = 8000,
        reload=True
    )