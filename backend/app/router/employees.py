from datetime import datetime, timezone
import re

from fastapi import APIRouter, HTTPException, Response, status, Body

router = APIRouter()

employees = []


def now_iso():
    return datetime.now(timezone.utc).isoformat()


def validate_employee_id(employee_id: str):
    if not re.fullmatch(r"EMP\d+", employee_id):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Malformed employee ID"
        )


def get_payload_id(payload: dict):
    return payload.get("employeeId") or payload.get("employee_id") or payload.get("id")


def normalize_employee(payload: dict):
    employee_id = get_payload_id(payload)

    if not employee_id:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="employeeId is required"
        )

    employee_id = str(employee_id)
    validate_employee_id(employee_id)

    position = payload.get("position") or payload.get("role") or "Employee"

    return {
        "id": employee_id,
        "employeeId": employee_id,
        "employee_id": employee_id,
        "name": payload.get("name"),
        "email": payload.get("email"),
        "department": payload.get("department"),
        "position": position,
        "role": position,
        "status": payload.get("status", "Active"),
        "createdAt": now_iso(),
        "updatedAt": None,
    }


@router.post("/employees", status_code=status.HTTP_201_CREATED)
def create_employee(payload: dict = Body(...)):
    employee = normalize_employee(payload)

    for existing_employee in employees:
        if existing_employee["employeeId"] == employee["employeeId"]:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Employee with this ID already exists"
            )

    if not employee["name"] or len(employee["name"]) < 2:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Name too short"
        )

    if not employee["email"] or "@" not in employee["email"]:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Invalid email"
        )

    if not employee["department"]:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Department is required"
        )

    employees.append(employee)

    return employee


@router.get("/employees")
def get_all_employees(department: str | None = None):
    results = employees

    if department:
        results = [
            employee for employee in results
            if employee["department"].lower() == department.lower()
        ]

    return results


@router.get("/employees/{employee_id}")
def get_employee_by_id(employee_id: str):
    validate_employee_id(employee_id)

    for employee in employees:
        if employee["employeeId"] == employee_id:
            return employee

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Employee not found"
    )


@router.put("/employees/{employee_id}")
def update_employee(employee_id: str, payload: dict = Body(...)):
    validate_employee_id(employee_id)

    if payload == {}:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Empty update body"
        )

    payload.pop("employeeId", None)
    payload.pop("employee_id", None)
    payload.pop("id", None)

    for employee in employees:
        if employee["employeeId"] == employee_id:
            if "name" in payload:
                if not payload["name"] or len(payload["name"]) < 2:
                    raise HTTPException(
                        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                        detail="Name too short"
                    )
                employee["name"] = payload["name"]

            if "email" in payload:
                if "@" not in payload["email"]:
                    raise HTTPException(
                        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                        detail="Invalid email"
                    )
                employee["email"] = payload["email"]

            if "department" in payload:
                employee["department"] = payload["department"]

            if "position" in payload:
                employee["position"] = payload["position"]
                employee["role"] = payload["position"]

            if "role" in payload:
                employee["role"] = payload["role"]
                employee["position"] = payload["role"]

            if "status" in payload:
                employee["status"] = payload["status"]

            employee["updatedAt"] = now_iso()

            return employee

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Employee not found"
    )


@router.delete("/employees/{employee_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_employee(employee_id: str):
    validate_employee_id(employee_id)

    for employee in employees:
        if employee["employeeId"] == employee_id:
            employees.remove(employee)
            return Response(status_code=status.HTTP_204_NO_CONTENT)

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Employee not found"
    )