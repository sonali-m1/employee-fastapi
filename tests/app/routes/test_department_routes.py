from unittest.mock import patch
from fastapi import HTTPException


# create
# TODO write test for no duplicate departments
@patch("services.department_service.create_department")
def test_create_department_201(mock_create, client):
    dept = {"dept_name": "Engineering"}

    mock_create.return_value = {
        "status_code": 200,
        "message": "Engineering Department successfully created!",
        "dept_id": "abc123",
    }

    res = client.post("/departments", json=dept)

    assert res.status_code in (200, 201)

# read
@patch("services.department_service.get_all_departments")
def test_get_all_departments_200(mock_get, client):
    mock_get.return_value = [
        {"_id": "abc123", "dept_name": "Engineering", "headcount": 0, "is_deleted": False},
    ]

    res = client.get("/departments")

    assert res.status_code == 200
    assert isinstance(res.json(), list)


@patch("services.department_service.get_department")
def test_get_department_404(mock_get, client):
    mock_get.side_effect = HTTPException(status_code=404, detail="Department not found")

    res = client.get("/departments/none")

    assert res.status_code == 404

# update
# TODO write tests for trying to decrement headcount 0
# and trying to update nonexistent department
@patch("services.department_service.increment_headcount")
def test_update_inc_department_headcount_200(mock_update, client):
    dept = {
        "dept_name" : "IT",
        "headcount" : 0,
    }
    mock_update.return_value = {
        "status_code":200,
        "message":"Department updated successfully!"
    }

    res = client.put("/departments/abc123/inc", json=dept)
    assert res.status_code in (200,201)
    assert "successfully" in res.json()["message"].lower()

@patch("services.department_service.decrement_headcount")
def test_update_dec_department_headcount_200(mock_update, client):
    dept = {
        "dept_name" : "IT",
        "headcount" : 1,
    }
    mock_update.return_value = {
        "status_code":200,
        "message":"Department updated successfully!"
    }

    res = client.put("/departments/abc123/dec", json=dept)
    assert res.status_code in (200,201)
    assert "successfully" in res.json()["message"].lower()


# delete
@patch("services.department_service.delete_department")
def test_delete_department_200(mock_delete, client):
    mock_delete.return_value = {
        "status_code":200,
        "message": "Department deleted successfully!"
    }
    res = client.delete("/departments/abc123")
    
    assert res.status_code in (200, 204)
    assert "deleted" in res.json()["message"].lower()

@patch("services.department_service.delete_department")
def test_delete_department_404(mock_delete, client):
    mock_delete.side_effect = HTTPException(status_code=404, detail="Department does not exist")
    res = client.delete("/departments/none")
    assert res.status_code == 404