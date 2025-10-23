from fastapi  import APIRouter, HTTPException
from bson.objectid import ObjectId
from configurations import dept_coll
from database.models import Department
from datetime import datetime
from services import department_service

router = APIRouter()

# create
@router.post("/departments")
def create_new_department(new_dept:Department):
    return department_service.create_department(new_dept)

# read
@router.get("/departments")
def get_all_departments():
    return department_service.get_all_departments()

# update

# delete
@router.delete("/departments/{dept_id}")
def delete_department(dept_id):
    return department_service.delete_department(dept_id)