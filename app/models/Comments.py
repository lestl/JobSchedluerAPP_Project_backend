from sqlalchemy import Column, Integer, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from app.db.base import Base

class Comment(Base):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True, index=True)
    write_date_time = Column(DateTime, nullable=False, description="Writed time")
    employee_id = Column(Integer, ForeignKey("employees.id"), description="A employee who writen")
    notification_id = Column(Integer, ForeignKey("notifications.id"), description="Specific notification")
    contens = Column(Text, nullable=False, description="comments contents")

    employee = relationship("Employee", backref="employees")
    notification = relationship("Notification", backref="notifications")