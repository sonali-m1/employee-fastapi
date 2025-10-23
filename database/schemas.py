
# employee
def individual_data(employee):
    return {
        "id": str(employee["_id"]),
        "first_name": employee["first_name"],
        "last_name": employee["last_name"],
        "dept_id": employee["dept_id"]
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
