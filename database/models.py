from pydantic import BaseModel
from datetime import datetime, timezone, date
from typing import Optional
from enum import Enum

class Employee(BaseModel):
    first_name:str
    last_name:str
    dept_id:str
    created_at:datetime = datetime.now(timezone.utc)
    updated_at:datetime = datetime.now(timezone.utc)
    is_deleted:bool = False

class Department(BaseModel):
    dept_name:str = None
    headcount:int = 0
    created_at:datetime = datetime.now(timezone.utc)
    updated_at:datetime = datetime.now(timezone.utc)
    is_deleted:bool = False

class Attendance(BaseModel):
    emp_id:str
    date:str
    status:AttendanceStatus
    created_at:datetime = datetime.now(timezone.utc)
    updated_at:datetime = datetime.now(timezone.utc)
    is_deleted:bool = False

class AttendanceStatus(str, Enum):
    PRESENT = "Present"
    ABSENT = "Absent"
    LEAVE = "Leave"
    REMOTE = "Remote"



