from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import  Column, Integer, String

from sqlalchemy.orm import sessionmaker 
from fastapi import FastAPI
 
# строка подключения
SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"
 
# создаем движок SqlAlchemy
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

Base = declarative_base()
 
class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True)
    username = Column(String(80), unique=True, nullable=False) 
    email = Column(String(120), unique=True, nullable=False)
    password = Column(String(128), nullable=False)
    
    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password

SessionLocal = sessionmaker(autoflush=False, bind=engine)

 
if __name__ == "__main__":
     
    db = SessionLocal()
    # создаем таблицы
    
    Base.metadata.create_all(bind=engine)
    
    persons = [User("John","i@mail.ru","123"),User("Bony","g@mail.ru","321"), User("Claid","c@mail.ru","231")]

    
    for user in persons:
        db.add(user)
        print(f"Добавлен пользователь user = {user}")

    db.commit()
    print(f"База сохранена")

    db.refresh(user)
    print(f"База обновлена")


