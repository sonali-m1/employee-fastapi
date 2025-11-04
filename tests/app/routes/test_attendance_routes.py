from unittest.mock import patch
from fastapi import HTTPException

# create
@patch("services.attendance_service.create_attendance")
def test_create_attendance_200(mock_create, client):
    att = {
        "emp_id" : "emp123",
        "date": "2024-11-03",
        "status": "Present"
    }

    mock_create.return_value = {
        "status_code" : 200,
        "message" : "Attendance record created successfully",
        "att_id": "att1"
    }

    res = client.post("/attendance", json=att)
    assert res.status_code in (200, 201)
    assert "successfully" in res.json()["message"].lower()

@patch("services.attendance_service.create_attendance")
def test_create_employee_400_dept_missing(mock_create, client):
    att = {
        "emp_id" : "none",
        "date": "2024-11-03",
        "status": "Present"
    }

    mock_create.side_effect = HTTPException(status_code=400, detail="Employee not found")

    res = client.post("/attendance", json=att)

    assert res.status_code == 400
    assert res.json()["detail"] == "Employee not found"


# TODO read
@patch("services.attendance_service.get_attendance")
def test_get_attendance_200(mock_get, client):
    mock_get.return_value = [
        {"emp_id": "emp123", "date": "2024-11-03", "status": "Present"},
        {"emp_id": "emp123", "date": "2024-11-04", "status": "Remote"},
    ]

    res = client.get(
        "/attendance",
        params={"emp_id": "emp123","start_date": "2024-11-03"},
    )

    assert res.status_code == 200
    body = res.json()
    assert isinstance(body, list)
    assert body[0]["emp_id"] == "emp123"


@patch("services.attendance_service.get_attendance")
def test_get_attendance_error(mock_get, client):
# your service wraps errors as 500
    mock_get.side_effect = HTTPException(
        status_code=500, detail="Error reading attendance: oops"
    )

    res = client.get("/attendance", params={
        "emp_id": "emp123", "start_date": "2024-11-03"},
    )

    assert res.status_code == 500
    assert "Error reading attendance" in res.json()["detail"]



# update
@patch("services.attendance_service.update_attendance")
def test_update_attendance_200(mock_update, client):
   
    mock_update.return_value = {
    "status_code": 200,
    "message": "Attendance updated successfully!",
    }
    res = client.put("/attendance/emp123/2024-11-03",
                     json={"emp_id":"emp123",
                           "date":"2025-11-03",
                           "status":"Present"})

    assert res.status_code in (200, 204)
    if res.status_code == 200:
        assert "updated" in res.json()["message"].lower()


@patch("services.attendance_service.update_attendance")
def test_update_attendance_404(mock_update, client):
    att = {
        "emp_id" : "emp123",
        "date": "2024-11-03",
        "status": "Present"
    }
    mock_update.side_effect = HTTPException(
        status_code=404, detail="Attendance record not found"
    )

    res = client.put(
        "/attendance/emp321/2024-11-03",
        json={"emp_id":"emp123",
              "date":"2024-11-03",
              "status":"Remote"},
    )

    assert res.status_code == 404
    assert res.json()["detail"] == "Attendance record not found"

# delete
@patch("services.attendance_service.delete_attendance")
def test_delete_attendance_200(mock_delete, client):
    mock_delete.return_value = {
        "message": "Attendance deleted successfully!"
    }

    res = client.delete("/attendance/emp123/2024-11-03")

    assert res.status_code in (200, 204)
    if res.status_code == 200:
        assert res.json()["message"] == "Attendance deleted successfully!"


@patch("services.attendance_service.delete_attendance")
def test_delete_attendance_404(mock_delete, client):
    mock_delete.side_effect = HTTPException(
        status_code=404,
        detail="Attendance record not found",
    )

    res = client.delete("/attendance/emp123/2024-11-03")

    assert res.status_code == 404
    assert res.json()["detail"] == "Attendance record not found"