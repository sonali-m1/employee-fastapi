from pydantic import BaseModel
from datetime import datetime

class Employee(BaseModel):
    first_name:str
    last_name:str
    department:str = None
    created_at:datetime = datetime.now().timestamp()
    updated_at:datetime = datetime.now().timestamp()
    is_deleted:bool = False

