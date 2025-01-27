from collections.abc import Generator
from typing import Annotated

from sqlalchemy import select

from app.tasks.tasks_service import TaskService
from app.tasks.task_repository import PostgresTaskRepository
from app.levels.levels_repository import PostgresLevelsRepository
from app.levels.levels_service import LevelsService
import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jwt.exceptions import InvalidTokenError
from pydantic import ValidationError
from sqlmodel import Session

from app.core import security
from app.core.config import settings
from app.core.db import engine
from app.models import EmployeeLevel, TokenPayload, User, UserWithExperience
from app.levels.levels_requirements import level_xp_requirements

reusable_oauth2 = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_STR}/login/access-token"
)


def get_db() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session

SessionDep = Annotated[Session, Depends(get_db)]
TokenDep = Annotated[str, Depends(reusable_oauth2)]

def get_task_service(db: SessionDep) -> TaskService:
    return TaskService(PostgresTaskRepository(db))
TaskServiceDep = Annotated[TaskService, Depends(get_task_service)]

def get_level_service(db: SessionDep) -> LevelsService:
    return LevelsService(PostgresLevelsRepository(db))
LevelsServiceDep = Annotated[LevelsService, Depends(get_level_service)]

def get_current_user(session: SessionDep, token: TokenDep) -> User:
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[security.ALGORITHM]
        )
        token_data = TokenPayload(**payload)
    except (InvalidTokenError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        )
    user = session.get(User, token_data.sub)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if not user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return user


CurrentUser = Annotated[User, Depends(get_current_user)]


def get_current_active_superuser(current_user: CurrentUser) -> User:
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=403, detail="The user doesn't have enough privileges"
        )
    return current_user


def get_current_user_with_level(session: SessionDep, token: TokenDep) -> UserWithExperience:
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[security.ALGORITHM]
        )
        token_data = TokenPayload(**payload)
    except (InvalidTokenError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        )
    
    # Fetch user with employee level information
    user_statement = (select(
                User, 
                EmployeeLevel.level.label("level"), 
                EmployeeLevel.xp.label("xp")
            )
        .join(EmployeeLevel, User.id == EmployeeLevel.employee_id)
        .filter(User.id == token_data.sub)
    )

    user_with_levels = session.exec(user_statement).one()

    if not user_with_levels:
        raise HTTPException(status_code=404, detail="User not found")

    # Calculate XP missing for the next level
    xp_missing = level_xp_requirements[user_with_levels.level+1] - user_with_levels.xp

    return UserWithExperience(
        email=user_with_levels.User.email,
        is_active=user_with_levels.User.is_active,
        is_superuser=user_with_levels.User.is_superuser,
        full_name=user_with_levels.User.full_name,
        id = user_with_levels.User.id,
        current_xp = user_with_levels.xp,
        level = user_with_levels.level,
        missing_xp = xp_missing
    )


CurrentUserWithLevel = Annotated[dict, Depends(get_current_user_with_level)]