from sqlalchemy import Column, Integer, String, Date, Text, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base import Base

class Notification(Base):
    __tablename__ = "notifications"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date, nullable=False, description="A date of When created")
    detail = Column(Text, nullable=False, description="The Notification's detail")
    title = Column(String, nullable=False, description="Notification's title")
    employee_id = Column(Integer, ForeignKey("employees.id"), description="The employee who writed (Only Manager)")

    employee = relationship("Employee", backref="employees")