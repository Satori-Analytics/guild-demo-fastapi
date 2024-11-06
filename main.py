import jwt
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from auth import ALGORITHM, SECRET_KEY
from routers import departments, employees, roles

app = FastAPI(
    title="Employee Directory API",
    description="API for managing employees, departments, and roles within an organization.",
    version="1.0.0",
)

app.include_router(employees.router)
app.include_router(departments.router)
app.include_router(roles.router)

# Simulated user database
users_db = {
    "admin": {"username": "admin", "password": "admin", "role": "admin"},
    "hr": {"username": "hr", "password": "hr", "role": "hr"},
    "employee": {"username": "employee", "password": "employee", "role": "employee"},
}


@app.post("/token", tags=["Authentication"])
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    """
    Simulated login endpoint to obtain a JWT token.
    """
    user = users_db.get(form_data.username)
    if not user or user["password"] != form_data.password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect username or password",
        )
    token = jwt.encode({"role": user["role"]}, SECRET_KEY, algorithm=ALGORITHM)
    return {"access_token": token, "token_type": "bearer"}
