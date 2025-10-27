from fastapi  import APIRouter, Query
from database.models import Attendance
from services import attendance_service
from datetime import date
from typing import Optional

router = APIRouter(tags=["Attendance"])

# create
@router.post("/attendance")
def create_attendance(attendance:Attendance):
    return attendance_service.create_attendance(attendance)

# read
@router.get("/attendance")
def get_attendance(emp_id:str, start_date:str, end_date:Optional[str] = Query(default=None)):
    return attendance_service.get_attendance(emp_id, start_date, end_date)