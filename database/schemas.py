

def individual_data(employee):
    return {
        "id": str(employee["_id"]),
        "first_name": employee["first_name"],
        "last_name": employee["last_name"],
        "department": employee["department"]
    }

def all_employees(employees):
    return [individual_data(employee) for employee in employees]

def individual_department(department):
    return {
        "id": str(department["_id"]),
        "dept_name": department["dept_name"],
    }
def all_departments(departments):
    return [individual_department(department) for department in departments]