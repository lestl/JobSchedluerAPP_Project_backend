from sqlalchemy import Column, Integer, String, Enum as SAEnum, DateTime, Foreign_Key
from sqlalchemy.orm import relationship
from app.db.base import Base
from Enums import EmployeeRole

class Employee(Base):

    __tablename__ = "employees"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(100), unique=True, index=True, description="login email", nullable=False)
    hashed_password = Column(String(255), nullable=False)
    department_id = Column(Integer, Foreign_Key("department.id"), description="What you blong dpartment")
    shift_group_id = Column(Integer, Foreign_Key("shiftgroup.id"), description="Your department Now", nullable=True)
    #shift는 나중에 등록하기 때문에 null 허용
    name = Column(String, description="Employee's Name", nullable=False)
    rank = Column(String, description="Your Rank in the office", nullable=False)
    role = Column(SAEnum(EmployeeRole), default=EmployeeRole.USER, description="Manager or User", nullable=False)
    #파이썬 Enum클래스 SAEnum 사용해 EmployeeRole의 값만 받음
    birth_data = Column(DateTime, nullable=False)

    department = relationship("Department", backref="departments")
    shift_group = relationship("Shift_Group", backref="shift_groups")