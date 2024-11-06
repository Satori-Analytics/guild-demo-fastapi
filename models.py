import uuid
from enum import Enum

from pydantic import BaseModel, EmailStr, Field


class RoleName(str, Enum):
    ADMIN = "admin"
    HR = "hr"
    EMPLOYEE = "employee"


class Role(BaseModel):
    id: int | None = Field(
        default_factory=lambda: str(uuid.uuid4()),
        description="Unique identifier for the role",
        examples=["1", "2", "3"],
    )
    name: RoleName = Field(
        ..., description="Name of the role", examples=["admin", "hr", "employee"]
    )


class Department(BaseModel):
    id: int | None = Field(
        default_factory=lambda: str(uuid.uuid4()),
        description="Unique identifier for the department",
    )
    name: str = Field(
        ..., max_length=50, description="Name of the department", examples=["HR"]
    )


class Employee(BaseModel):
    id: int | None = Field(
        default_factory=lambda: str(uuid.uuid4()),
        description="Unique identifier for the employee",
    )
    first_name: str = Field(
        ..., max_length=30, description="First name of the employee", examples=["John"]
    )
    last_name: str = Field(
        ..., max_length=30, description="Last name of the employee", examples=["Doe"]
    )
    email: EmailStr = Field(
        ..., description="Email address of the employee", examples=["johndoe@email.com"]
    )
    department_id: int = Field(
        ..., description="ID of the department the employee belongs to", examples=["1"]
    )
    role_id: int = Field(..., description="ID of the employee's role", examples=["1"])


class ErrorResponse(BaseModel):
    detail: str = Field(
        ...,
        description="Detailed error message explaining the issue.",
        examples=["Invalid input"],
    )


class UserCredentials(BaseModel):
    username: str
    password: str
