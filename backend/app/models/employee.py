from typing import Optional
from pydantic import BaseModel, EmailStr, Field, ConfigDict


class EmployeeCreate(BaseModel):
    employee_id: Optional[str] = None
    employeeId: Optional[str] = None

    name: str = Field(..., min_length=2)
    email: EmailStr
    department: str

    role: Optional[str] = None
    position: Optional[str] = None

    status: str = "active"


class EmployeeUpdate(BaseModel):
    model_config = ConfigDict(extra="ignore")

    name: Optional[str] = Field(default=None, min_length=2)
    email: Optional[EmailStr] = None
    department: Optional[str] = None

    role: Optional[str] = None
    position: Optional[str] = None

    status: Optional[str] = None


class EmployeeResponse(BaseModel):
    employee_id: str
    name: str
    email: EmailStr
    department: str

    role: Optional[str] = None
    position: Optional[str] = None

    status: str = "active"

    created_at: Optional[str] = None
    updated_at: Optional[str] = None