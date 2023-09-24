# Необходимо создать базу данных для интернет-магазина. База данных должна состоять из трёх таблиц: товары, заказы и пользователи.
# — Таблица «Товары» должна содержать информацию о доступных товарах, их описаниях и ценах.
# — Таблица «Заказы» должна содержать информацию о заказах, сделанных пользователями.
# — Таблица «Пользователи» должна содержать информацию о зарегистрированных пользователях магазина.
# • Таблица пользователей должна содержать следующие поля: id (PRIMARY KEY), имя, фамилия, адрес электронной почты и пароль.
# • Таблица заказов должна содержать следующие поля: id (PRIMARY KEY), id пользователя (FOREIGN KEY), id товара (FOREIGN KEY), дата заказа и статус заказа.
# • Таблица товаров должна содержать следующие поля: id (PRIMARY KEY), название, описание и цена.

# Создайте модели pydantic для получения новых данных и возврата существующих в БД для каждой из трёх таблиц.
# Реализуйте CRUD операции для каждой из таблиц через создание маршрутов, REST API.

import logging
from fastapi import FastAPI, Request, requests, Form, Depends, Body
from fastapi.responses import FileResponse, HTMLResponse, JSONResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from models import SessionLocal, User, Goods, Orders
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session, joinedload
from pydantic import BaseModel, Field



logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


app = FastAPI()

# class User(BaseModel):
#     username: str = Field(title="Username", max_length=50)
#     sername: str = Field(title="Sername", max_length=50)    
#     email: email = Field(title="Email", max_length=50)
#     password: str = Field(title="Description", max_length=50)

# class Goods(BaseModel):
#     goods_name: str = Field(title="Goods_name", max_length=50)
#     description: str = Field(title="Description", max_length=150) 
#     price: float = Field(title="Price", gt=0, le=100000)

# class Orders(BaseModel):
#     order_date: str = Field(title="Order_date", max_length=10)
#     order_status: str = Field(title="Order_status", max_length=128) 


# app.secret_key = b'5f214cacbd30c2ae4784b520f17912ae0d5d8c16ae98128e3f549546221265e4'

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

def get_database_session():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/", response_class=HTMLResponse)
def index(request: Request, db: Session = Depends(get_database_session)):
    return templates.TemplateResponse("base.html", {"request": request})

# ---------------------------------------
# Вывод списков

@app.get("/users", response_class=HTMLResponse)
def read_users(request: Request, db: Session = Depends(get_database_session)):
    user = db.query(User).all()
    print(user)
    # db.refresh(user)
    return templates.TemplateResponse("users.html", {"request": request, "users": user})

@app.get("/goods", response_class=HTMLResponse)
def read_goods(request: Request, db: Session = Depends(get_database_session)):
    goods = db.query(Goods).all()
    return templates.TemplateResponse("goods.html", {"request": request, "goods": goods})
        
@app.get("/orders", response_class=HTMLResponse)
def read_orders(request: Request, db: Session = Depends(get_database_session)):
    orders = db.query(Orders).join(User).join(Goods)
    goods = db.query(Goods).all()
    user = db.query(User).all()
    return templates.TemplateResponse("orders.html", {"request": request, "orders": orders, "users": user, "goods": goods})        
        
# ------------------------------------
# Добавление элементов
        
@app.post("/users/create", response_class=HTMLResponse)
def create_user(request: Request, db: Session = Depends(get_database_session), username=Form(), sername=Form(), email=Form(), password=Form()):
        user = User(username, sername, email, password)    
        db.add(user)
        db.commit()
        # db.refresh(user)
        # user = db.query(User).all()
        return templates.TemplateResponse("base.html", {"request":request, "message": "Пользователь добавлен"})

@app.post("/goods/create", response_class=HTMLResponse)
def create_good(request: Request, db: Session = Depends(get_database_session), goods_name=Form(), description=Form(), price=Form()):
    
        good = Goods(goods_name, description, price)    
        db.add(good)
        db.commit()
        # db.refresh(good)
        
        # goods = db.query(User).all()
        return templates.TemplateResponse("base.html", {"request":request, "message": "Товар добавлен"})         
        # return templates.TemplateResponse("goods.html",{"request":request, "goods": goods})
    # templates.TemplateResponse("goods.html", {"request":request, "goods": goods})

@app.post("/orders/create", response_class=HTMLResponse)
def create_user(request: Request, db: Session = Depends(get_database_session), username=Form(), goods_name=Form(), order_date=Form(), order_status=Form()):
        goods_id = db.query(Goods).filter(Goods.goods_name == goods_name).first()
        user_id = db.query(User).filter(User.username==username).first()     
        print(f"{goods_id},  {user_id}") 
        orders = Orders(user_id.id, goods_id.id, order_date, order_status)    
        db.add(orders)
        db.commit()
        # db.refresh(orders)
        # user = db.query(User).all()
        return templates.TemplateResponse("base.html", {"request":request, "message": "Заказ добавлен"}) 
        # return templates.TemplateResponse("orders.html", {"request":request, "orders": orders})

# -----------------------------
# Удаление данных из таблиц

@app.get("/users/delete/{user_id}", response_class=HTMLResponse)
def delete_user(request: Request, user_id: int, db: Session = Depends(get_database_session)):
    user = db.query(User).get(user_id)
    # print(f"Пользователь = {user}")
    if user==None:  
        return JSONResponse(status_code=404, content={ "message": "Пользователь не найден"})
    db.delete(user)  # удаляем объект
    db.commit()     # сохраняем изменения
    # db.refresh(user)
    # user = db.query(User).all()
    # print(f"Пользователь {user}")
    return templates.TemplateResponse("base.html", {"request":request, "message": "Пользователь удален"})
    # return templates.TemplateResponse("users.html", {"request":request, "users": user})

@app.get("/goods/delete/{goods_id}", response_class=HTMLResponse)
def delete_user(request: Request, goods_id: int, db: Session = Depends(get_database_session)):
    good = db.query(Goods).get(goods_id)
    # print(f"Пользователь = {user}")
    if good==None:  
        return JSONResponse(status_code=404, content={ "message": "Товар не найден"})
    db.delete(good)  # удаляем объект
    db.commit()     # сохраняем изменения
    # db.refresh(good)
    # goods = db.query(Goods).all()
    return templates.TemplateResponse("base.html",  {"request":request, "message": "Товар удален"}) 
    # return templates.TemplateResponse("goods.html", {"request":request, "goods": goods})

@app.get("/orders/delete/{orders_id}", response_class=HTMLResponse)
def delete_user(request: Request, orders_id: int, db: Session = Depends(get_database_session)):
    order = db.query(Orders).get(orders_id)
    # print(f"Пользователь = {user}")
    if order==None:  
        return JSONResponse(status_code=404, content={ "message": "Заказ не найден"})
    db.delete(order)  # удаляем объект
    db.commit()     # сохраняем изменения
    # db.refresh(good)
    # goods = db.query(Goods).all()
    return templates.TemplateResponse("base.html",  {"request":request, "message": "Заказ удален"}) 

# -----------------------------
# Обновление данных в таблицах

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
def update_user(request: Request, user_id: int, db: Session = Depends(get_database_session), username=Form(), sername=Form(), email=Form(), password=Form()):
    user = db.query(User).get(user_id)
    user.username = username
    user.sername = sername
    user.email = email
    user.password = password
    
    # db.update(user)
    db.commit()
    db.refresh(user)      
    # user = db.query(User).all()
    return templates.TemplateResponse("base.html", {"request":request, "message": "Пользователь изменен"})        

# ---

@app.get("/goods/edit/{goods_id}", response_class=HTMLResponse)
def update_goods(request: Request, goods_id: int, db: Session = Depends(get_database_session)):
    good = db.query(Goods).get(goods_id)
    # print(f"Пользователь {user}")
    if good==None:  
        return JSONResponse(status_code=404, content={ "message": "Пользователь не найден"})    
    db.commit()
    db.refresh(good)  
    return templates.TemplateResponse("editgoods.html", {"request":request, "goods": good})

@app.post("/goods/update/{goods_id}", response_class=HTMLResponse)
def update_goods_2(request: Request, goods_id: int, db: Session = Depends(get_database_session), goods_name=Form(), description=Form(), price=Form()):
    good = db.query(Goods).get(goods_id)
    good.goods_name = goods_name
    good.description = description
    good.price = price
    
    # db.update(user)
    db.commit()
    # db.refresh(good)      
    # goods = db.query(Goods).all()
    return templates.TemplateResponse("base.html", {"request":request, "message": "Пользователь изменен"})            
    # return templates.TemplateResponse("goods.html", {"request": request, "goods": goods})    
# ----


@app.get("/orders/edit/{orders_id}", response_class=HTMLResponse)
def update_order(request: Request, orders_id: int, db: Session = Depends(get_database_session)):
    order = db.query(Orders).get(orders_id)
    # print(f"Пользователь {user}")
    if order==None:  
        return JSONResponse(status_code=404, content={ "message": "Заказ не найден"})    
    db.commit()
    # db.refresh(order)  
    goods = db.query(Goods).all()
    user = db.query(User).all()
    return templates.TemplateResponse("editorder.html", {"request": request, "orders": order, "users": user, "goods": goods})            
    # return templates.TemplateResponse("editorder.html", {"request":request, "orders": order})

@app.post("/orders/update/{orders_id}", response_class=HTMLResponse)
def update_order_2(request: Request, orders_id: int, db: Session = Depends(get_database_session), order_date=Form(), order_status=Form(), username=Form(), goods_name=Form()):
    user_id = db.query(User).filter_by(username=username).first()
    goods_id = db.query(Goods).filter_by(goods_name=goods_name).first()    
    order = db.query(Orders).get(orders_id)
    order.order_date = order_date
    order.order_status = order_status
    order.user_id = user_id.id
    order.goods_id = goods_id.id
    
    # db.update(order)
    db.commit()
    # db.refresh(order)      
    # goods = db.query(Goods).all()
    return templates.TemplateResponse("base.html", {"request":request, "message": "Заказ изменен"})            
    # return templates.TemplateResponse("goods.html", {"request": request, "goods": goods})        
