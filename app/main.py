# 라이브러리 임포트
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

# DB 모델 임포트
from db.session import get_db
from models import Employee, Department, ShiftGroup, DailySchedule, LeaveRequest, Notification, Comment

app = FastAPI(
    title="Job Scheduler AOO API",
    description="API for scheduling and managing jobs",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Welcome to Job Scheduler API"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "code" : 200}

@app.get("/api/v1/employees") # (Admin 권한이 있는) 사용자가 모든 직원 조회 가능 및 부서별 직원 조회 가능
async def get_employees(department_id : int | None = None, db: Session = Depends(get_db)):
        # department_id를 받고 db 세션 통해 접속 후 사용자 정보 조회
        
        
        employees = db.query(Employee).all() #모든 직원 조회
        employees = [employee for employee in employees if employee.department_id == department_id]
        #부서 아이디와 일치하는 직원들만 필터링
        
        if employees is None or len(employees) == 0:
            return {"error": "No employees found for the given department", "code": 404}
          
        return employees, 200 #최종 직원 리스트 반환 즉 부서 내에 직원들만 반환
  
@app.get("/api/v1/employees/{employee_id}") # 특정 직원 조회 (로그인한 유저 본인 정보 조회)
async def get_employee(employee_id: int, db: Session = Depends(get_db)):
    # employee_id를 받고 db 세션 통해 접속 후 특정 사용자 정보 조회
    
    employees = db.query(Employee).filter(Employee.id == employee_id).all()
    # 특정 employee_id와 일치하는 직원 검색
    
    employee = next((employee for employee in employees if employee.id == employee_id), None)
    # 일치하는 직원이 없으면 None 반환
    
    if employee is None:
        return {"error": "Employee not found", "code": 404}
    return employee, 200

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
