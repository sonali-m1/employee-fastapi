from fastapi import FastAPI, HTTPException, APIRouter
from pydantic import BaseModel
from configurations import collection
from database.schemas import all_employees
from database.models import Employee
from bson.objectid import ObjectId
from datetime import datetime
# create app
app = FastAPI()
router = APIRouter()

# specify root page
@router.get("/")
def get_all_employees():
    data = collection.find({"is_deleted":False}) # empty find() returns everything, this param makes sure only non-deleted emps are returned (soft delete feature)
    return all_employees(data) # from schemas.py to return all employees and the data we want to see

@router.post("/employees")
def create_new_employee(new_employee:Employee): # TODO 
    try:
        response = collection.insert_one(dict(new_employee))
        print(response)
        return {"status_code":200, "id":str(response.inserted_id)}
    except Exception as e:
        raise HTTPException(status_code=500, detail = f"Error is : {e}")

@router.put("/employees/{emp_id}")
def update_employee_department(emp_id:str, updated_emp:Employee):
    try:
        # first check if employee to update (emp_id) exists
        id = ObjectId(emp_id) # parse it into object id and fetch employee with the id, if it exists itll return the emp otherwise false
        exists = collection.find_one({"_id":id, "is_deleted":False}) # make sure emp exists and is not deleted - use "_id" since that is the given object id that we are trying to get
        if not exists:
            raise HTTPException(status_code=404, detail = f"Employee does not exist")
        updated_emp.updated_at = datetime.now().timestamp() # if exists, update its update time and then insert in collection
        response = collection.update_one({"_id":id}, {"$set":dict(updated_emp)}) # use mongodb's update_one and $set to modify values of the fields of emp
        return {"status_code":200, "message":"Employee updated successfully!"} 
    except Exception as e:
        pass

@router.delete("/employees/{emp_id}")
def delete_employee(emp_id:str):
    try:
        # first check if employee to delete (emp_id) exists
        id = ObjectId(emp_id) # parse it into object id and fetch employee with the id, if it exists itll return the emp otherwise false
        exists = collection.find_one({"_id":id, "is_deleted":False}) # make sure emp exists and is not deleted - use "_id" since that is the given object id that we are trying to get
        if not exists:
            return HTTPException(status_code=404, detail = f"Employee does not exist")
        # response = collection.delete_one({"_id":id}) # hard-delete
        response = collection.update_one({"_id":id}, {"$set":dict({"is_deleted":True})}) # use mongodb's update_one and $set to modify is_delete values. 
        return {"status_code":200, "message":"Employee deleted successfully!"}
    except Exception as e:
        pass

app.include_router(router)



