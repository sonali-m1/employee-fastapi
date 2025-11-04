# tests/app/services/test_department_service.py

from unittest.mock import patch, MagicMock
from fastapi import HTTPException
from database.models import Department
from services import department_service


def sample_department_model() -> Department:
    return Department(
        dept_name="Engineering",
        headcount=0,
    )


# ------------------ CREATE ------------------ #
@patch("services.department_service.dept_coll.insert_one")
def test_create_department_success(mock_insert):
    mock_insert.return_value = MagicMock(inserted_id="dept123")

    dept = sample_department_model()
    res = department_service.create_department(dept)

    assert res["status_code"] in (200, 201)
    assert "successfully created" in res["message"].lower()
    mock_insert.assert_called_once()


@patch("services.department_service.dept_coll.insert_one")
def test_create_department_db_error(mock_insert):
    mock_insert.side_effect = Exception("db down")

    dept = sample_department_model()
    try:
        department_service.create_department(dept)
        assert False, "Should have raised HTTPException"
    except HTTPException as e:
        assert e.status_code == 500
        assert "error" in e.detail.lower()


# get
@patch("services.department_service.dept_coll.find")
@patch("services.department_service.all_departments")
def test_get_all_departments_success(mock_all, mock_find):
    mock_find.return_value = [{"_id": "1", "dept_name": "Eng", "is_deleted": False}]
    mock_all.return_value = [{"id": "1", "dept_name": "Eng"}]

    res = department_service.get_all_departments()

    assert res == [{"id": "1", "dept_name": "Eng"}]
    mock_find.assert_called_once_with({"is_deleted": False})
    mock_all.assert_called_once()


@patch("services.department_service.dept_coll.find")
def test_get_all_departments_error(mock_find):
    mock_find.side_effect = Exception("db down")

    try:
        department_service.get_all_departments()
        assert False, "Should have raised HTTPException"
    except HTTPException as e:
        assert e.status_code == 500
        assert "error fetching departments" in e.detail.lower()

@patch("services.department_service.individual_department")
@patch("services.department_service.dept_coll.find_one")
@patch("services.department_service.ObjectId")
def test_get_department_success(mock_obj, mock_find_one, mock_individual):
    mock_obj.return_value = "dept_obj_id"
    mock_find_one.return_value = {
        "_id": "dept_obj_id",
        "dept_name": "Engineering",
        "is_deleted": False,
    }
    mock_individual.return_value = {"id": "dept_obj_id", "dept_name": "Engineering"}

    res = department_service.get_department("123456789")

    assert res["dept_name"] == "Engineering"
    mock_find_one.assert_called_once()


@patch("services.department_service.dept_coll.find_one")
@patch("services.department_service.ObjectId")
def test_get_department_error(mock_obj, mock_find_one):
    mock_obj.return_value = "dept_obj_id"
    mock_find_one.side_effect = Exception("db down")

    try:
        department_service.get_department("123456789")
        assert False, "Should have raised HTTPException"
    except HTTPException as e:
        assert e.status_code == 500
        assert "error fetching department" in e.detail.lower()


# update
@patch("services.department_service.dept_coll.update_one")
@patch("services.department_service.dept_coll.find_one")
@patch("services.department_service.ObjectId")
def test_increment_headcount_success(mock_obj, mock_find_one, mock_update):
    mock_obj.return_value = "dept_obj_id"
    mock_find_one.return_value = {
        "_id": "dept_obj_id",
        "dept_name": "Eng",
        "is_deleted": False,
    }

    res = department_service.increment_headcount("123456789")

    assert res["status_code"] == 200
    assert "updated successfully" in res["message"].lower()
    mock_update.assert_called_once()


@patch("services.department_service.dept_coll.find_one")
@patch("services.department_service.ObjectId")
def test_increment_headcount_not_found(mock_obj, mock_find_one):
    mock_obj.return_value = "dept_obj_id"
    mock_find_one.return_value = None  # dept does not exist

    try:
        department_service.increment_headcount("123456789")
        assert False, "Should have raised HTTPException"
    except HTTPException as e:
        assert e.status_code == 404
        assert "department does not exist" in e.detail.lower()


@patch("services.department_service.dept_coll.update_one")
@patch("services.department_service.dept_coll.find_one")
@patch("services.department_service.ObjectId")
def test_increment_headcount_db_error(mock_obj, mock_find_one, mock_update):
    mock_obj.return_value = "dept_obj_id"
    mock_find_one.return_value = {
        "_id": "dept_obj_id",
        "dept_name": "Eng",
        "is_deleted": False,
    }
    mock_update.side_effect = Exception("db down")

    try:
        department_service.increment_headcount("123456789")
        assert False, "Should have raised HTTPException"
    except HTTPException as e:
        assert e.status_code == 500
        assert "error fetching departments" in e.detail.lower()


@patch("services.department_service.dept_coll.update_one")
@patch("services.department_service.dept_coll.find_one")
@patch("services.department_service.ObjectId")
def test_decrement_headcount_success(mock_obj, mock_find_one, mock_update):
    mock_obj.return_value = "dept_obj_id"
    mock_find_one.return_value = {
        "_id": "dept_obj_id",
        "dept_name": "Eng",
        "is_deleted": False,
    }

    res = department_service.decrement_headcount("123456789")

    assert res["status_code"] == 200
    assert "updated successfully" in res["message"].lower()
    mock_update.assert_called_once()


@patch("services.department_service.dept_coll.find_one")
@patch("services.department_service.ObjectId")
def test_decrement_headcount_not_found(mock_obj, mock_find_one):
    mock_obj.return_value = "dept_obj_id"
    mock_find_one.return_value = None

    try:
        department_service.decrement_headcount("123456789")
        assert False, "Should have raised HTTPException"
    except HTTPException as e:
        assert e.status_code == 404
        assert "department does not exist" in e.detail.lower()


@patch("services.department_service.dept_coll.update_one")
@patch("services.department_service.dept_coll.find_one")
@patch("services.department_service.ObjectId")
def test_decrement_headcount_db_error(mock_obj, mock_find_one, mock_update):
    mock_obj.return_value = "dept_obj_id"
    mock_find_one.return_value = {
        "_id": "dept_obj_id",
        "dept_name": "Eng",
        "is_deleted": False,
    }
    mock_update.side_effect = Exception("db down")

    try:
        department_service.decrement_headcount("123456789")
        assert False, "Should have raised HTTPException"
    except HTTPException as e:
        assert e.status_code == 500
        assert "error fetching departments" in e.detail.lower()


# delete
@patch("services.department_service.dept_coll.update_one")
@patch("services.department_service.dept_coll.find_one")
@patch("services.department_service.ObjectId")
def test_delete_department_success(mock_obj, mock_find_one, mock_update):
    mock_obj.return_value = "dept_obj_id"
    mock_find_one.return_value = {
        "_id": "dept_obj_id",
        "dept_name": "Eng",
        "is_deleted": False,
    }

    res = department_service.delete_department("123456789")

    # your current service *returns* a dict, not a Response
    assert res["status_code"] == 200
    assert "deleted successfully" in res["message"].lower()
    mock_update.assert_called_once()


@patch("services.department_service.dept_coll.find_one")
@patch("services.department_service.ObjectId")
def test_delete_department_not_found(mock_obj, mock_find_one):
    mock_obj.return_value = "dept_obj_id"
    mock_find_one.return_value = None

    # your current delete_department RETURNS an HTTPException instead of raising it
    res = department_service.delete_department("123456789")
    assert isinstance(res, HTTPException)
    assert res.status_code == 404
    assert "department does not exist" in res.detail.lower()
