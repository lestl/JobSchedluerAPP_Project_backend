from sqlalchemy import Column, Integer, Enum as SAEnum, DateTime, Date, Text, ForeignKey 
from sqlalchemy.orm import relationship
from app.db import Base
from app.models.Enums import Leave_RequestRole

class LeaveRequest(Base):
    __tablename__ = "leaverequests"

    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, ForeignKey("employees.id"), comment="A Employee Who requested")
    apply_date = Column(DateTime, comment="A Datetime When requested", nullable=False)
    target_date = Column(Date, comment="A Date Whe using a leave", nullable=False)
    reason = Column(Text, default="개인 사유", comment="The reason for using leave")
    status = Column(SAEnum(Leave_RequestRole), default=Leave_RequestRole.PENDING, comment="Request Status")

    employee = relationship("Employee", backref="employees")