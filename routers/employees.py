from typing import List

from fastapi import APIRouter, Depends, HTTPException, status

from auth import get_current_user_role
from models import Employee, ErrorResponse

router = APIRouter(
    prefix="/employees",
    tags=["Employees"],
    responses={404: {"model": ErrorResponse}},
)

# Simulated in-memory database
employees_db = {}
employee_id_counter = 1


@router.post("/", response_model=Employee, status_code=status.HTTP_201_CREATED)
def create_employee(employee: Employee, role: str = Depends(get_current_user_role)):
    """
    Create a new employee. Only 'admin' and 'hr' roles can create employees.
    """
    if role not in ["admin", "hr"]:
        raise HTTPException(status_code=403, detail="Insufficient permissions")
    global employee_id_counter
    employee.id = employee_id_counter
    employees_db[employee.id] = employee
    employee_id_counter += 1
    return employee


@router.get("/", response_model=List[Employee])
def list_employees(role: str = Depends(get_current_user_role)):
    """
    List all employees. Accessible by all authenticated users.
    """
    return list(employees_db.values())


@router.get("/{employee_id}", response_model=Employee)
def get_employee(employee_id: int, role: str = Depends(get_current_user_role)):
    """
    Get an employee by ID.
    """
    employee = employees_db.get(employee_id)
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    return employee


@router.put("/{employee_id}", response_model=Employee)
def update_employee(
    employee_id: int, employee: Employee, role: str = Depends(get_current_user_role)
):
    """
    Update an employee's information. Only 'admin' and 'hr' roles can update employees.
    """
    if role not in ["admin", "hr"]:
        raise HTTPException(status_code=403, detail="Insufficient permissions")
    if employee_id not in employees_db:
        raise HTTPException(status_code=404, detail="Employee not found")
    employee.id = employee_id
    employees_db[employee_id] = employee
    return employee


@router.delete("/{employee_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_employee(employee_id: int, role: str = Depends(get_current_user_role)):
    """
    Delete an employee. Only 'admin' role can delete employees.
    """
    if role != "admin":
        raise HTTPException(status_code=403, detail="Insufficient permissions")
    if employee_id in employees_db:
        del employees_db[employee_id]
    else:
        raise HTTPException(status_code=404, detail="Employee not found")
    return
