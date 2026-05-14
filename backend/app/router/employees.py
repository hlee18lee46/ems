from fastapi import APIRouter, Depends, Response, status

from app.controller.employees import EmployeeController
from app.dependencies import get_employee_controller
from app.models.employees import EmployeeCreate, EmployeeUpdate, EmployeeResponse

router = APIRouter()


@router.post("/employees", status_code=status.HTTP_201_CREATED, response_model=EmployeeResponse)
async def create_employee(
    payload: EmployeeCreate,
    controller: EmployeeController = Depends(get_employee_controller)
):
    return await controller.create_employee(payload)


@router.get("/employees")
async def get_all_employees(
    department: str | None = None,
    controller: EmployeeController = Depends(get_employee_controller)
):
    return await controller.get_all_employees(department)


@router.get("/employees/{employee_id}", response_model=EmployeeResponse)
async def get_employee_by_id(
    employee_id: str,
    controller: EmployeeController = Depends(get_employee_controller)
):
    return await controller.get_employee_by_id(employee_id)


@router.put("/employees/{employee_id}", response_model=EmployeeResponse)
async def update_employee(
    employee_id: str,
    payload: EmployeeUpdate,
    controller: EmployeeController = Depends(get_employee_controller)
):
    return await controller.update_employee(employee_id, payload)


@router.delete("/employees/{employee_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_employee(
    employee_id: str,
    controller: EmployeeController = Depends(get_employee_controller)
):
    await controller.delete_employee(employee_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)