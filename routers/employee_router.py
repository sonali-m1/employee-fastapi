from fastapi  import APIRouter, HTTPException
from bson.objectid import ObjectId
from configurations import employee_coll
from database.schemas import all_employees, individual_data
from database.models import Employee
from datetime import datetime
from services import employee_service

router = APIRouter()

@router.get("/employees")
def get_all_employees():
    return employee_service.get_all_employees()

@router.post("/employees")
def create_new_employee(new_employee:Employee): 
    return employee_service.create_new_employee(new_employee)

@router.put("/employees/{emp_id}")
def update_employee_department(emp_id:str, updated_emp:Employee):
    return employee_service.update_employee_department(emp_id, updated_emp)

@router.delete("/employees/{emp_id}")
def delete_employee(emp_id:str):
    return employee_service.delete_employee(emp_id)
   