from typing import Optional
from sqlalchemy import Column, Integer, String, Enum as SAEnum, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from db import Base
from models.Enums import EmployeeRole

class Employee(Base):

    __tablename__ = "employees"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(100), unique=True, index=True, comment="login email", nullable=False)
    hashed_password = Column(String(255), comment="Hashed password for authentication", nullable=True)
    department_id = Column(Integer, ForeignKey("departments.id"), comment="What you blong department")
    shift_group_id = Column(Integer, ForeignKey("shiftgroups.id"), comment="Your department Now", nullable=True)
    #shift는 나중에 등록하기 때문에 null 허용
    name = Column(String(10), comment="Employee's Name", nullable=False)
    rank = Column(String(10), comment="Your Rank in the office", nullable=False)
    role = Column(SAEnum(EmployeeRole), default=EmployeeRole.USER, comment="Manager or User", nullable=False)
    #파이썬 Enum클래스 SAEnum 사용해 EmployeeRole의 값만 받음
    birth_date = Column(DateTime, nullable=False)

    department = relationship("Department", backref="employees")
    shift_group = relationship("ShiftGroup", backref="employees")
    
