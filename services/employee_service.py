from fastapi  import HTTPException
from fastapi.encoders import jsonable_encoder
from bson.objectid import ObjectId
from configurations import employee_coll, dept_coll
from database.schemas import all_employees, individual_data
from database.models import Employee
from services.department_service import increment_headcount, decrement_headcount
from datetime import datetime, timezone

# CREATE
def create_new_employee(new_employee:Employee): # TODO 
    try:
        dept_id = ObjectId(new_employee.dept_id) # get department id from employee creation doc
        department = dept_coll.find_one({"_id":dept_id, "is_deleted":False}) # check that the department exists before trying to insert employee
        if not department:
            raise HTTPException(status_code=400, detail="Department not found")
        
        response = employee_coll.insert_one(jsonable_encoder(new_employee))
        increment_headcount(new_employee.dept_id)
        print(response)
        return {"status_code":200, "message":f"Employee {new_employee.first_name} {new_employee.last_name} successfully created!", "emp_id": str(response.inserted_id)}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail = f"Error is : {e}")
    
# READ
def get_all_employees():
    data = employee_coll.find({"is_deleted":False}) # empty find() returns everything, this param makes sure only non-deleted emps are returned (soft delete feature)
    return all_employees(data) # from schemas.py to return all employees and the data we want to see

def get_employee(emp_id):
    try:
        id = ObjectId(emp_id)
        employee_data = employee_coll.find_one({"_id":id, "is_deleted":False})
        return individual_data(employee_data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching employee: {str(e)}")

# UPDATE
def update_employee_department(emp_id:str, updated_emp:Employee):
    try:
        update_data = updated_emp.model_dump(exclude_unset=True)
        # first check if employee to update (emp_id) exists
        id = ObjectId(emp_id) # parse it into object id and fetch employee with the id, if it exists itll return the emp otherwise false
        exists = employee_coll.find_one({"_id":id, "is_deleted":False}) # make sure emp exists and is not deleted - use "_id" since that is the given object id that we are trying to get
        if not exists:
            raise HTTPException(status_code=404, detail = f"Employee does not exist")
        
        existing_emp = Employee(**exists)
        updated = existing_emp.model_copy(
            update={
                **update_data,
                "updated_at": datetime.now(timezone.utc)
            }
        )

        employee_coll.update_one({
            {"_id": id},
            {"$set": updated.model_dump()}
        })

        return {"status_code":200, "message":"Employee updated successfully!"} 
    except Exception as e:
        pass

# DELETE
def delete_employee(emp_id:str):
    try:
        # first check if employee to delete (emp_id) exists
        id = ObjectId(emp_id) # parse it into object id and fetch employee with the id, if it exists itll return the emp otherwise false
        exists = employee_coll.find_one({"_id":id, "is_deleted":False}) # make sure emp exists and is not deleted - use "_id" since that is the given object id that we are trying to get
        if not exists:
            raise HTTPException(status_code=404, detail = f"Employee does not exist")
        dept_id = exists.get("dept_id") # get the existing employee to delete's department id to decrement headcount
        if dept_id:
            decrement_headcount(dept_id)
        response = employee_coll.update_one({"_id":id}, {"$set":jsonable_encoder({"is_deleted":True})}) # use mongodb's update_one and $set to modify is_delete values. 
        print(response)
        return {"status_code":200, "message":"Employee deleted successfully!"}
    except Exception as e:
        print("Error in deleting employee: ", e)
        raise HTTPException(status_code=500, detail=f"Error deleting employee: {str(e)}")