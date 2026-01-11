from sqlalchemy import Column, Integer, String, Enum as SAEnum, Date, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from app.db.base import Base
from Enums import Daily_ScheduleRole

class   Daily_Schedule(Base):
    __tablename__ = "dailyschedules"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date, description="The Date of When you go work", nullable=False)
    shift_type = Column(SAEnum(Daily_ScheduleRole), nullable=False, description="The work form")
    employee_id = Column(Integer, ForeignKey("employees.id"), description="A employee Who need to work")
    note = Column(String, nullable=True, description="significant things")

    __table_args__ = (
        UniqueConstraint('date', 'employee_id', name='uq_isone_date_in_one_employee') #복합 제약조건 걸어서 date와 employee가 합쳐져 Unique해야함
    )
    employee = relationship("Employee", backref="employees")