from sqlalchemy import Column, Integer, String
from app.db import Base

class Department(Base):
    __tablename__ = "departments" # __tablename__  you can use it when you set the table name

    id = Column(Integer, primary_key=True, index=True) # index 사용해서 조회 성능을 높이나 쓰기 성능과 용량을 희생한다. index 사용해서 무언갈 찾겠다 싶으면 넣는거다 (Where에서 자주 씀, Order by, Join)
    name = Column(String(30), min_length=1, max_length=20, unique=True, nullable=False)