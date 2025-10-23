from pydantic import BaseModel
from datetime import datetime, timezone, date
from typing import Optional

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
    date:date
    status:str
    check_in:Optional[datetime] = None
    check_out:Optional[datetime] = None



