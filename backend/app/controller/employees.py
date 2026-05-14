import re
from fastapi import HTTPException, status

from app.models.employees import EmployeeCreate, EmployeeUpdate, EmployeeResponse
from app.repository.employees import EmployeeRepository


class EmployeeController:
    def __init__(self, repository: EmployeeRepository):
        self.repository = repository

    def validate_employee_id(self, employee_id: str):
        if employee_id.strip() == "":
            raise HTTPException(status_code=422, detail="Malformed employee ID")

        if not re.fullmatch(r"[A-Za-z0-9]+", employee_id):
            raise HTTPException(status_code=422, detail="Malformed employee ID")

    async def create_employee(self, payload: EmployeeCreate) -> EmployeeResponse:
        employee_id = payload.employeeId

        if not employee_id:
            raise HTTPException(status_code=422, detail="employeeId is required")

        self.validate_employee_id(employee_id)

        existing_employee = await self.repository.find_employee_by_id(employee_id)

        if existing_employee:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Employee with this ID already exists"
            )

        position = payload.position or payload.role or "Employee"

        employee = {
            "employeeId": employee_id,
            "name": payload.name,
            "email": str(payload.email),
            "department": payload.department,
            "position": position,
            "role": position,
            "status": payload.status or "active",
        }

        created = await self.repository.create_employee(employee)
        return EmployeeResponse(**created)

    async def get_all_employees(self, department: str | None = None):
        employees = await self.repository.get_all_employees()

        if department:
            employees = [
                employee for employee in employees
                if employee["department"].lower() == department.lower()
            ]

        return [EmployeeResponse(**employee) for employee in employees]

    async def get_employee_by_id(self, employee_id: str) -> EmployeeResponse:
        self.validate_employee_id(employee_id)

        employee = await self.repository.find_employee_by_id(employee_id)

        if not employee:
            raise HTTPException(status_code=404, detail="Employee not found")

        return EmployeeResponse(**employee)

    async def update_employee(self, employee_id: str, payload: EmployeeUpdate) -> EmployeeResponse:
        self.validate_employee_id(employee_id)

        update_data = payload.model_dump(exclude_unset=True)

        if update_data == {}:
            raise HTTPException(status_code=422, detail="Empty update body")

        update_data.pop("employeeId", None)

        existing_employee = await self.repository.find_employee_by_id(employee_id)

        if not existing_employee:
            raise HTTPException(status_code=404, detail="Employee not found")

        updated = await self.repository.update_employee(employee_id, update_data)
        return EmployeeResponse(**updated)

    async def delete_employee(self, employee_id: str):
        self.validate_employee_id(employee_id)

        deleted = await self.repository.delete_employee(employee_id)

        if not deleted:
            raise HTTPException(status_code=404, detail="Employee not found")

        return None