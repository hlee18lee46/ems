from fastapi import APIRouter, Depends, status
from app.models.users import ActivityLogEntry, UserCreate, UserResponse, UserInDB
from app.repository.users import UserRepository
from app.auth.utils import hash_password, verify_password
from app.dependencies.users import get_user_repository
from datetime import datetime


class AuthController:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    async def register_user(self, payload: UserCreate) -> UserResponse:
        hashed_password = hash_password(payload.password)

        user_in_db = UserInDB(
            email=payload.email,
            hashed_password=hashed_password
        )

        activity_log_entry = ActivityLogEntry(
            action="register",
            timestamp=datetime.utcnow()
        )

        user_in_db.activity_log.append(activity_log_entry)

        user_id = await self.user_repository.create_user(user_in_db)

        return UserResponse(id=user_id, email=payload.email)