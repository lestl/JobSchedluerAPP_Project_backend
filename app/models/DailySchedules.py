from sqlalchemy import Column, Integer, String, Enum as SAEnum, Date, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from app.db import Base
from app.models.Enums import Daily_ScheduleRole

class   DailySchedule(Base):
    __tablename__ = "dailyschedules"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date, comment="The Date of When you go work", nullable=False)
    shift_type = Column(SAEnum(Daily_ScheduleRole), nullable=False, comment="The work form")
    employee_id = Column(Integer, ForeignKey("employees.id"), comment="A employee Who need to work")
    note = Column(String(255), nullable=True, comment="significant things")

    __table_args__ = (
        UniqueConstraint('date', 'employee_id', name='uq_isone_date_in_one_employee'), #복합 제약조건 걸어서 date와 employee가 합쳐져 Unique해야함
    )
    employee = relationship("Employee", backref="employees")