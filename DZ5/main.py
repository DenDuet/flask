# Создать API для добавления нового пользователя в базу данных, обновления информации о пользователе в базе данных, удаления информации о пользователе из базы данных. 
# Приложение должно иметь возможность принимать POST, PUT, DELETE запросы с данными пользователя и сохранять их в базу данных.
# 📌 Создайте модуль приложения и настройте сервер и маршрутизацию.
# 📌 Создайте класс User с полями id, name, email и password.
# 📌 Создайте список users для хранения пользователей.
# 📌 Создайте маршрут для добавления нового пользователя (метод POST).
#     Создайте маршрут для обновления информации о пользователе (метод PUT).
#     Создайте маршрут для удаления информации о пользователе (метод DELETE).
# 📌 Реализуйте валидацию данных запроса и ответа.

# Создать веб-страницу для отображения списка пользователей. Приложение
# должно использовать шаблонизатор Jinja для динамического формирования HTML
# страницы.
# 📌 Создайте HTML шаблон для отображения списка пользователей. Шаблон должен
# содержать заголовок страницы, таблицу со списком пользователей и кнопку для
# добавления нового пользователя.
# 📌 Создайте маршрут для отображения списка пользователей (метод GET).
# 📌 Реализуйте вывод списка пользователей через шаблонизатор Jinja.

import logging
from fastapi import FastAPI, Request, requests, Form, Depends, Body
from fastapi.responses import FileResponse, HTMLResponse, JSONResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from models import SessionLocal, User
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session



logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


app = FastAPI()

# app.secret_key = b'5f214cacbd30c2ae4784b520f17912ae0d5d8c16ae98128e3f549546221265e4'

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

def get_database_session():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
@app.get("/users", response_class=HTMLResponse)
def read_users(request: Request, db: Session = Depends(get_database_session)):
    user = db.query(User).all()
    print(user)
    # db.refresh(user)
    return templates.TemplateResponse("users.html", {"request": request, "users": user})

        
@app.post("/users/create", response_class=HTMLResponse)
def create_user(request: Request, db: Session = Depends(get_database_session), username=Form(), email=Form(), password=Form()):
    
        user = User(username, email, password)    
        db.add(user)
        db.commit()
        db.refresh(user)
        
        user = db.query(User).all()
        return templates.TemplateResponse("users.html", {"request":request, "users": user})


@app.get("/users/delete/{user_id}", response_class=HTMLResponse)
def delete_user(request: Request, user_id: int, db: Session = Depends(get_database_session)):
    user = db.query(User).get(user_id)
    print(f"Пользователь = {user}")
    if user==None:  
        return JSONResponse(status_code=404, content={ "message": "Пользователь не найден"})
    db.delete(user)  # удаляем объект
    db.commit()     # сохраняем изменения
    db.refresh(user)
    user = db.query(User).all()
    print(f"Пользователь {user}")
    return templates.TemplateResponse("users.html", {"request":request, "users": user})


@app.get("/users/edit/{user_id}", response_class=HTMLResponse)
def update_user(request: Request, user_id: int, db: Session = Depends(get_database_session)):
    user = db.query(User).get(user_id)
    print(f"Пользователь {user}")
    if user==None:  
        return JSONResponse(status_code=404, content={ "message": "Пользователь не найден"})    
   
    db.commit()
    db.refresh(user)  
    return templates.TemplateResponse("edituser.html", {"request":request, "users": user})


@app.post("/users/update/{user_id}", response_class=HTMLResponse)
def update_user(request: Request, user_id: int, db: Session = Depends(get_database_session), username=Form(), email=Form(), password=Form()):
    user = db.query(User).get(user_id)
    user.username = username
    user.email = email
    user.password = password
    
    # db.update(user)
    db.commit()
    db.refresh(user)      
    user = db.query(User).all()

    
    # print(user)
    return templates.TemplateResponse("users.html", {"request": request, "users": user})    