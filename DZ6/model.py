from fastapi import FastAPI
from pydantic import BaseModel, Field

app = FastAPI()
class User(BaseModel):
    username: str = Field(title="Username", max_length=50)
    sername: str = Field(title="Sername", max_length=50)    
    email: email = Field(title="Email", max_length=50)
    password: str = Field(title="Description", max_length=50)

class Goods(BaseModel):
    goods_name: str = Field(title="Goods_name", max_length=50)
    description: str = Field(title="Description", max_length=150) 
    price: float = Field(title="Price", gt=0, le=100000)

class Orders(BaseModel):
    order_date: str = Field(title="Order_date", max_length=10)
    order_status: str = Field(title="Order_status", max_length=128) 

    
@app.post("/users/")
def create_user(users: User):
    return {"users": users}

@app.post("/goods/")
def create_good(goods: Goods):
    return {"goods": goods}

@app.post("/orders/")
def create_order(orders: Orders):
    return {"orders": orders}