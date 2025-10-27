from fastapi import HTTPException, Query
from fastapi.encoders import jsonable_encoder
from bson.objectid import ObjectId
from configurations import employee_coll, attendance_coll
from database.schemas import all_attendance, individual_attendance
from database.models import Attendance, AttendanceStatus
from datetime import datetime, date, timezone, time
from typing import Optional, List, Dict

# create attednance record

def create_attendance(attendance:Attendance):
    validate_employee(attendance.emp_id)
    try:
        if not isinstance(attendance.status, AttendanceStatus):
            raise HTTPException(status_code=404, detail = f"Incorrect status input")
        
        response = attendance_coll.insert_one(jsonable_encoder(attendance))
        print(response)
        return {"status_code":200, "message": f"Attendance record successfully inserted!", "att_id":str(response.inserted_id)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {e}")

# read attendance record
def get_attendance(emp_id:str, start_date:str, end_date: Optional[str] = None) -> List[Dict]:
    validate_employee(emp_id)
    query = {"emp_id" : emp_id, "is_deleted":False}
    if end_date:
        query["date"] = {"$gte":start_date, "$lte": end_date}
    else:
        query["date"] = start_date

    try:
        docs = attendance_coll.find(query).sort("date",1)
        return all_attendance(docs)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error reading attendance: {str(e)}")
    

# update
def update_attendance(emp_id:str, date:str, status:str):
    validate_employee(emp_id)
    try:
        query = {"emp_id": emp_id, "date":date, "is_deleted":False}
        update = {"$set" : {"status":status}}
        response = attendance_coll.update_one(query, update)

        if response.matched_count == 0:
            raise HTTPException(status_code=404, detail="Attendance record not found")
        return {"message":"Attendance updated successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error updating attendance: {str(e)}")
    
# delete
def delete_attendance(emp_id:str, date:str):
    validate_employee(emp_id)
    try:
        query = {"emp_id":emp_id, "date":date, "is_deleted":False}
        delete = {"$set" : {"is_deleted":True}}
        response = attendance_coll.update_one(query, delete)

        if response.matched_count == 0:
            raise HTTPException(status_code=404, detail="Attendance record not found")
        
        return {"message": "Attendance deleted successfully!"}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error updating attendance: {str(e)}")

def validate_employee(emp_id:str):
    try:
        emp_oid = ObjectId(emp_id)
        employee = employee_coll.find_one({"_id": emp_oid, "is_deleted":False})
        if not employee:
            raise HTTPException(status_code=404, detail="Employee not found")
    except Exception:
        employee = None