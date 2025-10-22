from fastapi import FastAPI, HTTPException, APIRouter
from pydantic import BaseModel
from configurations import employee_coll
from database.schemas import all_employees
from database.models import Employee
from datetime import datetime
from routers.employee_router import router as employee_router
# create app
app = FastAPI()
router = APIRouter()

# specify root page
@app.get("/")
def root_page():
    return "Employee Management System"


app.include_router(employee_router)



