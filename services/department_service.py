from fastapi  import APIRouter, HTTPException
from fastapi.encoders import jsonable_encoder
from bson.objectid import ObjectId
from configurations import dept_coll
from database.schemas import all_departments, individual_department
from database.models import Department
from datetime import datetime, timezone

# create
def create_department(new_dept:Department):
    try:
        response = dept_coll.insert_one(jsonable_encoder(new_dept))
        print(response)
        return {"status_code":200, "message": f"{new_dept.dept_name} Department successfully created!", "dept_id":str(response.inserted_id)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {e}")  

# read
def get_all_departments():
    try:
        data = dept_coll.find({"is_deleted": False})
        return all_departments(data)
    except Exception as e:
        print("Error in get_all_departments:", e)
        raise HTTPException(status_code=500, detail=f"Error fetching departments: {str(e)}")
    
def get_department(dept_id):
    try:
        id = ObjectId(dept_id)
        department = dept_coll.find_one({"_id":id, "is_deleted":False})
        return individual_department(department)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching department: {str(e)}")
    
# update
def increment_headcount(dept_id):
    try:
        id = ObjectId(dept_id)
        exists = dept_coll.find_one({"_id":id, "is_deleted":False}) 
        if not exists:
            raise HTTPException(status_code=404, detail = f"Department does not exist")
        response = dept_coll.update_one({"_id": id}, {"$inc":{"headcount":1}, "$set":{"updated_at": datetime.now(timezone.utc)}})
        return {"status_code":200, "message":"Department headcount updated successfully!"}
    except Exception as e:
        print("Error in increment_department:", e)
        raise HTTPException(status_code=500, detail=f"Error fetching departments: {str(e)}")
    
def decrement_headcount(dept_id):
    try:
        id = ObjectId(dept_id)
        exists = dept_coll.find_one({"_id":id, "is_deleted":False})
        if not exists:
            raise HTTPException(status_code=404, detail = f"Department does not exist")
        response = dept_coll.update_one({"_id": id}, {"$inc":{"headcount":-1}, "$set":{"updated_at": datetime.now(timezone.utc)}})
        return {"status_code":200, "message":"Department headcount updated successfully!"}
    except Exception as e:
        print("Error in increment_department:", e)
        raise HTTPException(status_code=500, detail=f"Error fetching departments: {str(e)}")


# delete
def delete_department(dept_id):
    try:
        # first check if department to delete (dept_id) exists
        id = ObjectId(dept_id) # parse it into object id and fetch employee with the id, if it exists itll return the emp otherwise false
        exists = dept_coll.find_one({"_id":id, "is_deleted":False}) # make sure dep exists and is not deleted - use "_id" since that is the given object id that we are trying to get
        if not exists:
            return HTTPException(status_code=404, detail = f"Department does not exist")
        # response = dept_coll.delete_one({"_id":id}) # hard-delete
        response = dept_coll.update_one({"_id":id}, {"$set":jsonable_encoder({"is_deleted":True})}) # use mongodb's update_one and $set to modify is_delete values. 
        return {"status_code":200, "message":"Department deleted successfully!"}
    except Exception as e:
        pass
    
        



