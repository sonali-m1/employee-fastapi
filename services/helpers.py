from datetime import datetime
from bson import ObjectId
from fastapi import HTTPException
from configurations import employee_coll, attendance_coll
from database.schemas import all_employees, individual_data
from database.models import Employee, Attendance, AttendanceStatus

PAYABLE = {AttendanceStatus.PRESENT.value, AttendanceStatus.REMOTE.value}

def validate_employee(emp_id:str):
    try:
        emp_oid = ObjectId(emp_id)
        employee = employee_coll.find_one({"_id": emp_oid, "is_deleted":False})
        if not employee:
            raise HTTPException(status_code=404, detail="Employee not found")
    except Exception:
        employee = None

def dateify(date:str) -> str:
    try:
        datetime.fromisoformat(date)
    except ValueError:
        raise HTTPException(status_code=400, detail="date must be in YYYY-MM-DD format")
    return date

# TODO  finish salary calculaton function
def calculate_salary(emp_id:str, start_date:str, end_date:str):
    start_date = dateify(start_date)
    end_date = dateify(end_date)
    if start_date > end_date:
        raise HTTPException(status_code=400, detail="start_date must be before end_date")
    
    validate_employee(emp_id)
    employee = employee_coll.find_one({"_id":ObjectId(emp_id), "is_deleted":False})
    daily_rate = employee.get("daily_salary",0.0)

    payable_range = {"$gte": start_date, "$lte": end_date}
    query = {"emp_id":emp_id, "is_deleted":False, "date":payable_range, "status": {"$in": list(PAYABLE)}}
    payable_days = attendance_coll.count_documents(query)
    



    