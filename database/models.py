from pydantic import BaseModel
from datetime import datetime

class Employee(BaseModel):
    first_name:str
    last_name:str
    department:Department = None
    created_at:datetime = datetime.now().timestamp()
    updated_at:datetime = datetime.now().timestamp()
    is_deleted:bool = False

class Department(BaseModel):
    dept_name:str = None
    created_at:datetime = datetime.now().timestamp()
    updated_at:datetime = datetime.now().timestamp()
    is_deleted:bool = False
