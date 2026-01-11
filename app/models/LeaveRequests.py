from sqlalchemy import Column, Integer, Enum as SAEnum, DateTime, Date, Text, ForeignKey 
from sqlalchemy.orm import relationship
from app.db.base import Base
from Enums import Leave_RequestRole

class Leave_Request(Base):
    __tablename__ = "leaverequests"

    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, ForeignKey("Employee.id"), description="A Employee Who requested")
    apply_date = Column(DateTime, description="A Datetime When requested", nullable=False)
    target_date = Column(Date, description="A Date Whe using a leave", nullable=False)
    reason = Column(Text, default="개인 사유", description="The reason for using leave")
    status = Column(SAEnum(Leave_RequestRole), default=Leave_RequestRole.PENDING, description="Request Status")

    employee = relationship("Employee", backref="employees")