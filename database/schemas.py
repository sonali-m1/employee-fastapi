from configurations import employee_coll, dept_coll
from bson.objectid import ObjectId
# employee
def individual_data(employee):
    dept_id = employee.get("dept_id")
    dept_name = None
    if dept_id:
        department = dept_coll.find_one({"_id": ObjectId(dept_id), "is_deleted":False})
        if department:
            dept_name = department.get("dept_name")
    return {
        "id": str(employee["_id"]),
        "first_name": employee["first_name"],
        "last_name": employee["last_name"],
        "dept_id": employee["dept_id"],
        "dept_name": dept_name
    }

def all_employees(employees):
    return [individual_data(employee) for employee in employees]

# department
def individual_department(department):
    return {
        "id": str(department["_id"]),
        "dept_name": department["dept_name"],
        "headcount": department["headcount"]
    }
def all_departments(departments):
    return [individual_department(department) for department in departments]

# TODO attendance
def individual_attendance(attendance):
    emp_id = attendance.get("emp_id")
    if emp_id:
        employee = employee_coll.find_one({"_id":ObjectId(emp_id), "is_deleted":False})
        if employee:
            name = f"{employee.get("first_name")} {employee.get("last_name")}"

    return {
        "id": str(attendance["_id"]),
        "emp_id": str(attendance["emp_id"]),
        "name": name,
        "date": attendance["date"],
        "status": attendance["status"]
    }

def all_attendance(attendance_records):
    return [individual_attendance(attendance) for attendance in attendance_records]