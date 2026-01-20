from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.db import Base

class ShiftGroup(Base):
    __tablename__ = "shiftgroups"

    id = Column(Integer, primary_key=True, index=True)
    department_id = Column(Integer, ForeignKey("department.id"), description="Relationship on 1:N with department" )
    name = Column(String, min_length = 1, max_length = 10, nullable=False, description="The A group, B group...")
    color = Column(String, default="#FFFFFF", description="Color Code. Display the UI/Calender's with a color EX)#ffffff") #null일 경우 기본 색상 지정

    employee = relationship("Employee", backref="employees")
    #backref = 이걸 설정함으로  만든 employees 객체를 통해 통해 바로 Employees 테이블의 속성을 사용할 수 있다.
    #Join 쿼리 안짜도 . 만으로 다른 테이블 모든 속성을 가져올 수 있다.
    #backref는 그저 문일 뿐이다 이걸 설정하면 Employee 객체에 employees 라는 속성이 하나 더 생기는 것과 같다 (명시해도 된다.)
    #나중에 db.backref이름.으로 바로 employess의 객체에 접근하면 된다.