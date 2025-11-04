from unittest.mock import patch, MagicMock
from fastapi import HTTPException
from database.models import Employee
from services import employee_service

def sample_employee_model() -> Employee:
    return Employee(
        first_name="John",
        last_name="Doe",
        dept_id="123456789",
        daily_salary=200.0,
    )

@patch("services.employee_service.increment_headcount")
@patch("services.employee_service.employee_coll.insert_one")
@patch("services.employee_service.dept_coll.find_one")
@patch("services.employee_service.ObjectId")
def test_create_new_employee_success(mock_obj, mock_dept_find, mock_insert, mock_inc):
    emp = sample_employee_model()

    mock_obj.return_value = "mocked_object_id"
    # department exists
    mock_dept_find.return_value = {"_id": "mocked_object_id", "dept_name": "Engineering"}
    # insert_one returns an object with inserted_id
    mock_insert.return_value = MagicMock(inserted_id="emp123")

    res = employee_service.create_new_employee(emp)

    assert res["status_code"] == 200
    assert "successfully created" in res["message"].lower()
    mock_insert.assert_called_once()
    mock_inc.assert_called_once_with(emp.dept_id)


@patch("services.employee_service.increment_headcount")
@patch("services.employee_service.dept_coll.find_one")
@patch("services.employee_service.ObjectId")
def test_create_new_employee_dept_not_found(mock_obj, mock_dept_find, mock_inc):
    emp = sample_employee_model()

    mock_obj.return_value = "mocked_object_id"
    mock_dept_find.return_value = None  # department missing

    try:
        employee_service.create_new_employee(emp)
        assert False, "Should have raised HTTPException"
    except HTTPException as e:
        assert e.status_code == 400
        assert "Department not found" in e.detail
    mock_inc.assert_not_called()


@patch("services.employee_service.employee_coll.find")
@patch("services.employee_service.all_employees")
def test_get_all_employees(mock_all_emps, mock_find):
    mock_find.return_value = [{"_id": "1"}, {"_id": "2"}]
    mock_all_emps.return_value = [{"id": "1"}, {"id": "2"}]

    res = employee_service.get_all_employees()

    assert res == [{"id": "1"}, {"id": "2"}]
    mock_find.assert_called_once_with({"is_deleted": False})
    mock_all_emps.assert_called_once()


@patch("services.employee_service.employee_coll.find_one")
@patch("services.employee_service.individual_data")
@patch("services.employee_service.ObjectId")
def test_get_employee_success(mock_obj, mock_individual, mock_find_one):
    mock_obj.return_value = "emp_obj_id"
    mock_find_one.return_value = {"_id": "emp_obj_id", "first_name": "John"}
    mock_individual.return_value = {"id": "emp_obj_id", "first_name": "John"}

    res = employee_service.get_employee("123456789")

    assert res["first_name"] == "John"
    mock_find_one.assert_called_once()

@patch("services.employee_service.employee_coll.find_one")
@patch("services.employee_service.ObjectId")
def test_get_employee_error(mock_obj, mock_find_one):
    mock_obj.return_value = "emp_obj_id"
    
    mock_find_one.side_effect = Exception("DB down")

    try:
        employee_service.get_employee("123456789")
        assert False, "Should have raised HTTPException"
    except HTTPException as e:
        assert e.status_code == 500
        assert "Error fetching employee" in e.detail

@patch("services.employee_service.employee_coll.update_one")
@patch("services.employee_service.employee_coll.find_one")
@patch("services.employee_service.ObjectId")
def test_update_employee_success(mock_obj, mock_find_one, mock_update_one):
    # existing employee in DB
    mock_obj.return_value = "emp_obj_id"
    mock_find_one.return_value = {
        "_id": "emp_obj_id",
        "first_name": "John",
        "last_name": "Doe",
        "dept_id": "123456789",
        "daily_salary": 200.0,
        "created_at": None,
        "updated_at": None,
        "is_deleted": False,
    }

    # we only update first_name
    updated_emp = Employee(
        first_name="Johnny",
        last_name="Doe",
        dept_id="123456789",
        daily_salary=200.0,
    )

    res = employee_service.update_employee_department("123456789", updated_emp)

    assert res["status_code"] == 200
    assert "updated" in res["message"].lower()
    mock_update_one.assert_called_once()


@patch("services.employee_service.employee_coll.find_one")
@patch("services.employee_service.ObjectId")
def test_update_employee_not_found(mock_obj, mock_find_one):
    mock_obj.return_value = "emp_obj_id"
    mock_find_one.return_value = None  # employee not in DB

    updated_emp = Employee(
        first_name="Johnny",
        last_name="Doe",
        dept_id="123456789",
        daily_salary=200.0,
    )

    try:
        employee_service.update_employee_department("123456789", updated_emp)
        assert False, "Should have raised HTTPException"
    except HTTPException as e:
        assert e.status_code == 404
        assert "Employee does not exist" in e.detail

# delete
@patch("services.employee_service.employee_coll.update_one")
@patch("services.employee_service.decrement_headcount")
@patch("services.employee_service.employee_coll.find_one")
@patch("services.employee_service.ObjectId")
def test_delete_employee_success(mock_obj, mock_find_one, mock_dec, mock_update):
    mock_obj.return_value = "emp_obj_id"
    mock_find_one.return_value = {
        "_id": "emp_obj_id",
        "dept_id": "123456789",
        "is_deleted": False,
    }

    res = employee_service.delete_employee("123456789")

    assert res["status_code"] == 200
    assert "deleted" in res["message"].lower()
    mock_dec.assert_called_once_with("123456789")
    mock_update.assert_called_once()

@patch("services.employee_service.employee_coll.find_one")
@patch("services.employee_service.ObjectId")
def test_delete_employee_not_found(mock_obj, mock_find_one):
    mock_obj.return_value = "emp_obj_id"
    mock_find_one.return_value = None

    try:
        employee_service.delete_employee("123456789")
        assert False, "Should have raised HTTPException"
    except HTTPException as e:
        assert e.status_code == 404
        assert "Employee does not exist" in e.detail