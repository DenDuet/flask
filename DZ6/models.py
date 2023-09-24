from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import  Column, Integer, String, create_engine, ForeignKey, DateTime, Float
from sqlalchemy.orm import sessionmaker 
from fastapi import FastAPI
from sqlalchemy.orm import relationship
 
# строка подключения
SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app_shop.db"
 
# создаем движок SqlAlchemy
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

Base = declarative_base()
 
class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True)
    username = Column(String(80), unique=True, nullable=False) 
    sername = Column(String(80), nullable=False) 
    email = Column(String(120), unique=True, nullable=False)
    password = Column(String(128), nullable=False)
    orders = relationship("Orders", back_populates="users")
    
    def __init__(self, username, sername, email, password):
        self.username = username
        self.sername = sername
        self.email = email
        self.password = password

class Goods(Base):
    __tablename__ = "goods"
    
    id = Column(Integer, primary_key=True)
    goods_name = Column(String(80), unique=True, nullable=False) 
    description = Column(String(200), nullable=False) 
    price = Column(Float, nullable=False)
    orders = relationship("Orders", back_populates="goods")
    
    def __init__(self, goods_name, description, price):
        self.goods_name = goods_name
        self.description = description
        self.price = price


class Orders(Base):
    __tablename__ = "orders"
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id")) 
    goods_id = Column(Integer, ForeignKey("goods.id")) 
    order_date = Column(String(10), nullable=False) 
    order_status = Column(String(128), nullable=False)
    users = relationship("User", back_populates="orders")
    goods = relationship("Goods", back_populates="orders")
    
    def __init__(self, user_id, goods_id, order_date, order_status):
        self.user_id = user_id
        self.goods_id = goods_id
        self.order_date = order_date
        self.order_status = order_status


SessionLocal = sessionmaker(autoflush=False, bind=engine)


 
if __name__ == "__main__":
     
    db = SessionLocal()
    # создаем таблицы

    Base.metadata.create_all(bind=engine)
    
    persons = [User("John","Malkovich","i@mail.ru","123"),User("Bony","Ebonito","g@mail.ru","321"), User("Claid","Gansta","c@mail.ru","231")]
    
    for user in persons:
        db.add(user)
        print(f"Добавлен пользователь user = {user}")

    goods = [Goods("TV", "Телевизор с диагональю 200 дюймов. Показывает офигительно круто. Вау", 200.0), Goods("TV_2", "Телевизор с диагональю 300 дюймов. Показывает офигительно круче первого. Вау-Вау", 300.0), Goods("TV_3", "Телевизор с диагональю 400 дюймов. Показывает круче вареного яйца. Без комментариев", 1000.50), Goods("Тумба TV", "Тумба для телевизора. Для всех моделей.", 500.90)]
    
    for good in goods:
        db.add(good)
        print(f"Добавлен товар goods = {good}")
        
    orders = [Orders(1, 2, "12.05.2020", "ready"),Orders(1, 4, "12.05.2020", "ready"),Orders(2, 1, "12.05.2021", "ок"),Orders(2, 4, "12.06.2021", "ок"),Orders(3, 1, "01.10.2022", "ready")]
    
    for order in orders:
        db.add(order)
        print(f"Добавлен товар goods = {order}")
            
    db.commit()
    print(f"База сохранена")

    db.refresh(user)
    print(f"База обновлена")


