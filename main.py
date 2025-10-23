from fastapi import FastAPI, HTTPException, APIRouter
from pydantic import BaseModel
from configurations import employee_coll, dept_coll
from database.schemas import all_employees
from database.models import Employee, Department
from datetime import datetime
from routers.employee_router import router as employee_router
from routers.department_router import router as department_router

# create app
app = FastAPI()

# specify root page
@app.get("/")
def root_page():
    return "Employee Management System"


app.include_router(employee_router)
app.include_router(department_router)



