from enum import Enum

class EmployeeRole(str, Enum):
    #근무표 관리자 = Manager, 일반 = User
    MANAGER = "manager"
    USER = "user"

class Leave_RequestRole(str, Enum):
    #연차 상태
    PENDING = "대기"
    APPROVE = "승인"
    REJECTED = "거절"

class Daily_ScheduleRole(str, Enum):
    #DAY(주간), NIGHT(야간), OFF(비번), LEAVE(연차)
    DAY = "주간"
    NIGHT = "야간"
    OFF = "비번"
    LEAVE = "연차 및 휴가"

class ShiftGroup(str, Enum):
    #근무조 그룹
    GROUP_A = "A조"
    GROUP_B = "B조"
    GROUP_C = "C조"
    
class Department(str, Enum):
    #부서
    HR = "인사부"
    BDP = "BDP운영팀"