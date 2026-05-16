from app.core.database import get_database
from app.repository.users import UserRepository
from app.controllers.auth import AuthController


def get_user_repository():
    db = get_database()
    return UserRepository(db)


def get_auth_controller():
    user_repository = get_user_repository()
    return AuthController(user_repository)