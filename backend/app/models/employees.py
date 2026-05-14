import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, Field, ConfigDict


class EmployeeCreate(BaseModel):
    employeeId: Optional[str] = Field(default=None, min_length=1)
    name: str = Field(..., min_length=2)
    email: EmailStr
    department: str
    position: Optional[str] = "Employee"
    role: Optional[str] = None
    status: str = "active"


class EmployeeUpdate(BaseModel):
    model_config = ConfigDict(extra="ignore")

    employeeId: Optional[str] = Field(default=None, min_length=1)
    name: Optional[str] = Field(default=None, min_length=2)
    email: Optional[EmailStr] = None
    department: Optional[str] = None
    position: Optional[str] = None
    role: Optional[str] = None
    status: Optional[str] = None
    updatedAt: Optional[datetime.datetime] = None


class EmployeeResponse(BaseModel):
    id: str
    employeeId: str
    name: str
    email: EmailStr
    department: str
    position: str
    role: Optional[str] = None
    status: str
    createdAt: datetime.datetime
    updatedAt: Optional[datetime.datetime] = None