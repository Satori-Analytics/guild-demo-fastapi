from typing import List

from fastapi import APIRouter, Depends, HTTPException

from auth import get_current_user_role
from models import ErrorResponse, Role

router = APIRouter(
    prefix="/roles",
    tags=["Roles"],
    responses={404: {"model": ErrorResponse}},
)

# Simulated in-memory database
roles_db = {
    1: Role(id=1, name="admin"),
    2: Role(id=2, name="hr"),
    3: Role(id=3, name="employee"),
}
role_id_counter = 4


@router.get("/", response_model=List[Role])
def list_roles(role: str = Depends(get_current_user_role)):
    """
    List all roles. Accessible by all authenticated users.
    """
    return list(roles_db.values())


@router.get("/{role_id}", response_model=Role)
def get_role(role_id: int, role: str = Depends(get_current_user_role)):
    """
    Get a role by ID.
    """
    role_obj = roles_db.get(role_id)
    if not role_obj:
        raise HTTPException(status_code=404, detail="Role not found")
    return role_obj
