from unittest.mock import patch
from fastapi import HTTPException

# create
@patch("services.employee_service.create_new_employee")
def test_create_employee_success(mock_create, client):
    emp = {
        "first_name":"John",
        "last_name":"Doe",
        "dept_id" : "abc123",
        "daily_salary": 200.0
    }

    mock_create.return_value = {
        "status_code": 200,
        "message": "Employee successfully created!",
        "emp_id": "emp123",
    }

    res = client.post("/employees", json=emp)

    assert res.status_code in (200, 201)
    assert "successfully" in res.json()["message"].lower()


@patch("services.employee_service.create_new_employee")
def test_create_employee_400_dept_missing(mock_create, client):
    emp = {
        "first_name": "John",
        "last_name": "Doe",
        "dept_id": "missing",
        "daily_salary": 200.0,
    }

    mock_create.side_effect = HTTPException(status_code=400, detail="Department not found")

    res = client.post("/employees", json=emp)

    assert res.status_code == 400
    assert res.json()["detail"] == "Department not found"

# read
@patch("services.employee_service.get_employee")
def test_get_employee_200(mock_get, client):
    mock_get.return_value = {
        "_id": "emp123",
        "first_name": "John",
        "last_name": "Doe",
        "dept_id": "abc123",
        "daily_salary": 200.0,
        "is_deleted": False,
    }

    res = client.get("/employees/emp123")

    assert res.status_code == 200
    assert res.json()["first_name"] == "John"


@patch("services.employee_service.get_employee")
def test_get_employee_404(mock_get, client):
    mock_get.side_effect = HTTPException(status_code=404, detail="Employee not found")

    res = client.get("/employees/none")

    assert res.status_code == 404
    assert res.json()["detail"] == "Employee not found"

# update
@patch("services.employee_service.update_employee_department")
def test_update_employee_200(mock_update, client):
    payload = {
        "first_name": "John",
        "last_name": "Doe",
        "dept_id": "abc123",
        "daily_salary": 210.0,
    }

    mock_update.return_value = {
        "status_code": 200,
        "message": "Employee updated successfully!",
    }

    res = client.put("/employees/emp123", json=payload)

    assert res.status_code in (200, 204)
    if res.status_code == 200:
        assert "updated" in res.json()["message"].lower()


@patch("services.employee_service.update_employee_department")
def test_update_employee_404(mock_update, client):
    mock_update.side_effect = HTTPException(status_code=404, detail="Employee does not exist")

    res = client.put("/employees/none", json={"first_name": "John", "last_name": "Doe", "dept_id": "abc123", "daily_salary": 200.0})

    assert res.status_code == 404


#  delete
@patch("services.employee_service.delete_employee")
def test_delete_employee_200(mock_delete, client):
    mock_delete.return_value = {
        "status_code": 200,
        "message": "Employee deleted successfully!",
    }

    res = client.delete("/employees/emp123")

    assert res.status_code in (200, 204)
    if res.status_code == 200:
        assert "deleted" in res.json()["message"].lower()


@patch("services.employee_service.delete_employee")
def test_delete_employee_404(mock_delete, client):
    mock_delete.side_effect = HTTPException(status_code=404, detail="Employee does not exist")

    res = client.delete("/employees/none")

    assert res.status_code == 404