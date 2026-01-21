from sqlalchemy import Column, Integer, String, Date, Text, ForeignKey
from sqlalchemy.orm import relationship
from app.db import Base

class Notification(Base):
    __tablename__ = "notifications"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date, nullable=False, comment="A date of When created")
    detail = Column(Text, nullable=False, comment="The Notification's detail")
    title = Column(String(100), nullable=False, comment="Notification's title")
    employee_id = Column(Integer, ForeignKey("employees.id"), comment="The employee who writed (Only Manager)")

    employee = relationship("Employee", backref="employees")