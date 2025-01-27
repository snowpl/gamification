from uuid import UUID
from typing import Any

from app.api.users.skills_models import GlobalSkillCreate
from app.api.users.users_models import UserCreate, UserUpdate
from sqlmodel import Session, select

from app.core.security import get_password_hash, verify_password
from app.models import AvailableTask, AvailableTaskCreate, Company, CompanyCreate, Department, DepartmentCreate, EmployeeLevel, GlobalSkill, Item, ItemCreate, User


def create_user(*, session: Session, user_create: UserCreate) -> User:
    # Create the User object
    db_user = User(
        hashed_password=get_password_hash(user_create.password),
        email=user_create.email,
        is_superuser=user_create.is_superuser,
        company_id=user_create.company_id,
        department_id=user_create.department_id,
        full_name=user_create.full_name
    )
    session.add(db_user)
    
    # Create the EmployeeLevel object linked to the User
    employee_level = EmployeeLevel(
        employee_id=db_user.id,
        level=0,
        xp=0,
        xp_multiplier=1.0,
    )
    session.add(employee_level)
    session.flush()  # Ensure the `employee_level.id` is generated

    # Link the `employee_level_id` in the User object
    db_user.employee_level_id = employee_level.id
    session.add(db_user)  # Update the User object

    # Commit the transaction
    session.commit()
    session.refresh(db_user)
    return db_user

def update_user(*, session: Session, db_user: User, user_in: UserUpdate) -> Any:
    user_data = user_in.model_dump(exclude_unset=True)
    extra_data = {}
    if "password" in user_data:
        password = user_data["password"]
        hashed_password = get_password_hash(password)
        extra_data["hashed_password"] = hashed_password
    db_user.sqlmodel_update(user_data, update=extra_data)
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user


def get_user_by_email(*, session: Session, email: str) -> User | None:
    statement = select(User).where(User.email == email)
    session_user = session.exec(statement).first()
    return session_user


def authenticate(*, session: Session, email: str, password: str) -> User | None:
    db_user = get_user_by_email(session=session, email=email)
    if not db_user:
        return None
    if not verify_password(password, db_user.hashed_password):
        return None
    return db_user


def create_item(*, session: Session, item_in: ItemCreate, owner_id: UUID) -> Item:
    db_item = Item.model_validate(item_in, update={"owner_id": owner_id})
    session.add(db_item)
    session.commit()
    session.refresh(db_item)
    return db_item

def create_company(*, session: Session, company_in: CompanyCreate) -> Company:
    db_company = Company.model_validate(company_in)
    session.add(db_company)
    session.commit()
    session.refresh(db_company)
    return db_company

def create_department(*, session: Session, department_in: DepartmentCreate) -> Department:
    db_department = Department.model_validate(department_in)
    session.add(db_department)
    session.commit()
    session.refresh(db_department)
    return db_department

def create_global_skill(*, session: Session, skill_in: GlobalSkillCreate) -> GlobalSkill:
    db_skill = GlobalSkill.model_validate(skill_in)
    session.add(db_skill)
    session.commit()
    session.refresh(db_skill)
    return db_skill

def create_available_task(*, session: Session, task_in: AvailableTaskCreate) -> AvailableTask:
    db_task = AvailableTask.model_validate(task_in)
    session.add(db_task)
    session.commit()
    session.refresh(db_task)
    return db_task

def create_default_level(*, session: Session, employee_id: UUID) -> EmployeeLevel:
    model_in = EmployeeLevel(
            employee_id=employee_id,
            level=0,
            xp=0,
            xp_multiplier=1.0,
    )
    db_level = EmployeeLevel.model_validate(model_in)
    session.add(db_level)
    session.commit()
    session.refresh(db_level)
    return db_level

def create_employee_level(*, session: Session, level_in: EmployeeLevel) -> EmployeeLevel:
    db_level = EmployeeLevel.model_validate(level_in)
    session.add(db_level)
    session.commit()
    session.refresh(db_level)
    return db_level