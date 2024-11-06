from typing import List

from fastapi import APIRouter, Depends, HTTPException, status

from auth import get_current_user_role
from models import Department, ErrorResponse

router = APIRouter(
    prefix="/departments",
    tags=["Departments"],
    responses={404: {"model": ErrorResponse}},
)

# Simulated in-memory database
departments_db = {}
department_id_counter = 1


@router.post("/", response_model=Department, status_code=status.HTTP_201_CREATED)
def create_department(
    department: Department, role: str = Depends(get_current_user_role)
):
    """
    Create a new department. Only 'admin' role can create departments.
    """
    if role != "admin":
        raise HTTPException(status_code=403, detail="Insufficient permissions")
    global department_id_counter
    department.id = department_id_counter
    departments_db[department.id] = department
    department_id_counter += 1
    return department


@router.get("/", response_model=List[Department])
def list_departments(role: str = Depends(get_current_user_role)):
    """
    List all departments. Accessible by all authenticated users.
    """
    return list(departments_db.values())


@router.get("/{department_id}", response_model=Department)
def get_department(department_id: int, role: str = Depends(get_current_user_role)):
    """
    Get a department by ID.
    """
    department = departments_db.get(department_id)
    if not department:
        raise HTTPException(status_code=404, detail="Department not found")
    return department


@router.put("/{department_id}", response_model=Department)
def update_department(
    department_id: int,
    department: Department,
    role: str = Depends(get_current_user_role),
):
    """
    Update a department. Only 'admin' role can update departments.
    """
    if role != "admin":
        raise HTTPException(status_code=403, detail="Insufficient permissions")
    if department_id not in departments_db:
        raise HTTPException(status_code=404, detail="Department not found")
    department.id = department_id
    departments_db[department_id] = department
    return department


@router.delete("/{department_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_department(department_id: int, role: str = Depends(get_current_user_role)):
    """
    Delete a department. Only 'admin' role can delete departments.
    """
    if role != "admin":
        raise HTTPException(status_code=403, detail="Insufficient permissions")
    if department_id in departments_db:
        del departments_db[department_id]
    else:
        raise HTTPException(status_code=404, detail="Department not found")
    return
