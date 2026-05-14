import datetime


class EmployeeRepository:
    def __init__(self):
        self.employees = []

    def now(self):
        return datetime.datetime.now(datetime.timezone.utc)

    async def create_employee(self, employee: dict):
        employee["id"] = employee["employeeId"]
        employee["createdAt"] = self.now()
        employee["updatedAt"] = None

        self.employees.append(employee)

        return employee

    async def get_all_employees(self):
        return self.employees

    async def find_employee_by_id(self, employee_id: str):
        for employee in self.employees:
            if employee["employeeId"] == employee_id or employee.get("id") == employee_id:
                return employee

        return None

    async def update_employee(self, employee_id: str, update_data: dict):
        employee = await self.find_employee_by_id(employee_id)

        if not employee:
            return None

        update_data.pop("employeeId", None)
        update_data.pop("id", None)

        for key, value in update_data.items():
            if key == "role":
                employee["position"] = value
                employee["role"] = value
            elif key == "position":
                employee["position"] = value
                employee["role"] = value
            else:
                employee[key] = value

        employee["id"] = employee["employeeId"]
        employee["updatedAt"] = self.now()

        return employee

    async def delete_employee(self, employee_id: str):
        employee = await self.find_employee_by_id(employee_id)

        if not employee:
            return False

        self.employees.remove(employee)

        return True