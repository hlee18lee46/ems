from app.repository.employees import EmployeeRepository
from app.controller.employees import EmployeeController

employee_repository = EmployeeRepository()
employee_controller = EmployeeController(employee_repository)


def get_employee_controller():
    return employee_controller