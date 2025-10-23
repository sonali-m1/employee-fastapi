from fastapi  import APIRouter
from database.models import Department
from services import department_service

router = APIRouter(tags=["Departments"])

# create
@router.post("/departments")
def create_new_department(new_dept:Department):
    return department_service.create_department(new_dept)

# read
@router.get("/departments")
def get_all_departments():
    return department_service.get_all_departments()

@router.get("/departments/{dept_id}")
def get_department(dept_id):
    return department_service.get_department(dept_id)

# update
@router.put("/departments/{dept_id}/inc")
def increment_headcount(dept_id):
    return department_service.increment_headcount(dept_id)

@router.put("/departments/{dept_id}/dec")
def decrement_headcount(dept_id):
    return department_service.decrement_headcount(dept_id)

# delete
@router.delete("/departments/{dept_id}")
def delete_department(dept_id):
    return department_service.delete_department(dept_id)