

def individual_data(employee):
    return {
        "id": str(employee["_id"]),
        "first_name": employee["first_name"],
        "last_name": employee["last_name"],
        "department": employee["department"]
    }

def all_employees(employees):
    return [individual_data(employee) for employee in employees]