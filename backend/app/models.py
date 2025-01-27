from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4
from pydantic import EmailStr
from sqlmodel import Field, Relationship, SQLModel
from sqlalchemy.orm import RelationshipProperty
from sqlalchemy import Column, Enum

# Shared properties
class UserBase(SQLModel):
    email: EmailStr = Field(unique=True, index=True, max_length=255)
    is_active: bool = True
    is_superuser: bool = False
    full_name: str | None = Field(default=None, max_length=255)

# Properties to receive via API on creation
class UserCreate(UserBase):
    password: str = Field(min_length=8, max_length=40)
    company_id: UUID
    department_id: UUID

class UserRegister(SQLModel):
    email: EmailStr = Field(max_length=255)
    password: str = Field(min_length=8, max_length=40)
    full_name: str | None = Field(default=None, max_length=255)

# Properties to receive via API on update, all are optional
class UserUpdate(UserBase):
    email: EmailStr | None = Field(default=None, max_length=255)  # type: ignore
    password: str | None = Field(default=None, min_length=8, max_length=40)


class UserUpdateMe(SQLModel):
    full_name: str | None = Field(default=None, max_length=255)
    email: EmailStr | None = Field(default=None, max_length=255)


class UpdatePassword(SQLModel):
    current_password: str = Field(min_length=8, max_length=40)
    new_password: str = Field(min_length=8, max_length=40)

# Database model, database table inferred from class name
class User(UserBase, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    hashed_password: str
    items: list["Item"] = Relationship(back_populates="owner", cascade_delete=True)
    company: "Company" = Relationship(back_populates="employees")
    department: "Department" = Relationship(back_populates="employees")
    company_id: UUID = Field(
        foreign_key="company.id", nullable=False, ondelete="CASCADE"
    )
    department_id: UUID = Field(foreign_key="department.id")
    employee_tasks: list["EmployeeTask"] = Relationship(
        sa_relationship=RelationshipProperty(
            "EmployeeTask",
            back_populates="assigned_to",
            foreign_keys='[EmployeeTask.assigned_to_id]')
    )
    approved_tasks: list["EmployeeTask"] = Relationship(
        sa_relationship=RelationshipProperty(
            "EmployeeTask",
            back_populates="approved_by",
            foreign_keys='[EmployeeTask.approved_by_id]')
    )
    user_skills: list["Skill"] = Relationship(back_populates="user")
    employee_level_id: Optional[UUID] = Field(
        foreign_key="employee_levels.id", nullable=True, ondelete="CASCADE"
    )
    employee_level: "EmployeeLevel" = Relationship(
        sa_relationship=RelationshipProperty(
            "EmployeeLevel",
            back_populates="employee",
            foreign_keys='[EmployeeLevel.employee_id]'
            )
    )

# Properties to return via API, id is always required
class UserPublic(UserBase):
    id: UUID

class UserWithExperience(UserPublic):
    current_xp: int
    level: int
    missing_xp: int

class UsersPublic(SQLModel):
    data: list[UserPublic]
    count: int


# Shared properties
class ItemBase(SQLModel):
    title: str = Field(min_length=1, max_length=255)
    description: str | None = Field(default=None, max_length=255)


# Properties to receive on item creation
class ItemCreate(ItemBase):
    pass


# Properties to receive on item update
class ItemUpdate(ItemBase):
    title: str | None = Field(default=None, min_length=1, max_length=255)  # type: ignore


# Database model, database table inferred from class name
class Item(ItemBase, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    title: str = Field(max_length=255)
    owner_id: UUID = Field(
        foreign_key="user.id", nullable=False, ondelete="CASCADE"
    )
    owner: User | None = Relationship(back_populates="items")


# Properties to return via API, id is always required
class ItemPublic(ItemBase):
    id: UUID
    owner_id: UUID


class ItemsPublic(SQLModel):
    data: list[ItemPublic]
    count: int


# Generic message
class Message(SQLModel):
    message: str


# JSON payload containing access token
class Token(SQLModel):
    access_token: str
    token_type: str = "bearer"


# Contents of JWT token
class TokenPayload(SQLModel):
    sub: str | None = None


class NewPassword(SQLModel):
    token: str
    new_password: str = Field(min_length=8, max_length=40)

#Shared properties
class CompanyBase(SQLModel):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    name: str
    current_xp: int = 0
    level: int = 0

#Database model
class Company(CompanyBase, table=True):
    is_active: bool = True 
    employees: list["User"] = Relationship(back_populates="company", cascade_delete=True)
    departments: list["Department"] = Relationship(back_populates="company", cascade_delete=True)

class CompanyRead(CompanyBase):
    pass

class CompanyCreate(CompanyBase):
    pass

#Shared properties
class SkillBase(SQLModel):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    name: str = Field(min_length=1, max_length=255)
    description: str | None = Field(default=None, max_length=500)
    current_xp: int = 0

#Database model
class Skill(SkillBase, table=True):
    user_id: Optional[UUID] = Field(
        foreign_key="user.id", nullable=True, ondelete="CASCADE"
    )
    user: Optional["User"] = Relationship(back_populates="user_skills")
    department_id: UUID = Field(
        foreign_key="department.id", nullable=False, ondelete="CASCADE"
    )
    department: "Department" = Relationship(back_populates="department_skills")
    employee_tasks: list["AvailableTask"] = Relationship(back_populates="skill", cascade_delete=True)

#Skill properties to recieve on creation
class SkillCreate(SkillBase):
    department_id: UUID
    user_id: Optional[UUID] = None  # Make user_id optional

# #Shared properties
# class LevelBase(SQLModel):
#     level: int = 0
#     required_xp: int = 0

# #Database model
# class Level(LevelBase, table=True):
#     reward: str | None = Field(default=None, max_length=255)
#     type: str | None = Field(default=None, max_length=255)

# # Shared properties
class DepartmentBase(SQLModel):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    name: str = Field(min_length=1, max_length=255)
    current_xp: int = 0
    level: int = 0

#Database model
class Department(DepartmentBase, table=True):
    company_id: UUID = Field(
        foreign_key="company.id", nullable=False, ondelete="CASCADE"
    )
    company: "Company" = Relationship(back_populates="departments")
    employees: list["User"] = Relationship(back_populates="department", cascade_delete=True)
    tasks: list["AvailableTask"] = Relationship(back_populates="department", cascade_delete=True)
    department_skills: list["Skill"] = Relationship(back_populates="department", cascade_delete=True)

#Properties to receive on department creation
class DepartmentCreate(DepartmentBase):
    company_id: UUID

# # Shared properties
class AvailableTaskBase(SQLModel):
    title: str = Field(min_length=1, max_length=255)
    description: str| None = Field(default=None, max_length=500)
    requires_approval: bool = False
    approved: bool = False
    department_xp: int = 0
    skill_xp: int = 0
    company_xp: int = 0
    person_xp: int = 0
    is_active: bool = True

class AvailableTask(AvailableTaskBase, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    department_id: UUID = Field(
        foreign_key="department.id", nullable=False, ondelete="CASCADE"
    )
    department: "Department" = Relationship(back_populates="tasks")
    skill_id: UUID = Field(
        foreign_key="skill.id", nullable=False, ondelete="CASCADE"
    )
    skill: "Skill" = Relationship(back_populates="employee_tasks")
    company_id: UUID = Field(
        foreign_key="company.id", nullable=False, ondelete="CASCADE"
    )

# Properties to return via API, id is always required
class AvailableTaskPublic(AvailableTaskBase):
    id: UUID
    department_id: UUID
    department_name: str
    #skill_id: UUID
    #company_id: UUID

class AvailableTasksPublic(SQLModel):
    data: list[AvailableTaskPublic]
    count: int

class TaskStatus(Enum):
    ASSIGNED = "Assigned"
    #IN_PROGRESS = "In Progress"
    WAITING_APPROVAL = "Waiting Approval"
    REJECTED = "Rejected"
    COMPLETED = "Completed"
    CANCELED = "Canceled"

class EmployeeTaskBase(SQLModel):
    task_id: UUID | None
    status: str
    created_at: datetime = Field(default_factory=datetime.now, nullable=False),
    title: str| None = Field(default=None, max_length=500)
    description: str| None = Field(default=None, max_length=500)
    version: int = 1
    completed_at: datetime | None
    reason: str | None = Field(default=None, max_length=500),
    requires_approval: bool = False
    submitted_at: datetime | None

# Database model, database table inferred from class name
class EmployeeTask(EmployeeTaskBase, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    assigned_to_id: UUID = Field(
        foreign_key="user.id", nullable=False, ondelete="CASCADE"
    )
    assigned_to: "User" = Relationship(
        sa_relationship=RelationshipProperty(
            "User",
            back_populates="employee_tasks",
            foreign_keys='[EmployeeTask.assigned_to_id]')
    )
    approved_by_id: Optional[UUID] = Field(
        foreign_key="user.id", nullable=True, ondelete="CASCADE"
    )
    approved_by: Optional["User"] = Relationship(
        sa_relationship=RelationshipProperty(
            "User",
            back_populates="approved_tasks",
            foreign_keys='[EmployeeTask.approved_by_id]')
    )
    # company_id: UUID = Field(
    #     foreign_key="company.id", nullable=False, ondelete="CASCADE"
    # )

class TaskEvent(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    aggregate_id: UUID
    timestamp: datetime
    version: int
    event_type: str = Field(max_length=100)
    assigned_to_id: UUID| None
    task_id: UUID| None
    reason: str| None = Field(default=None, max_length=500)
    approved_by_id: UUID | None

# Properties to receive on item creation
class AvailableTaskCreate(AvailableTaskBase):
    department_id: UUID
    skill_id: UUID
    company_id: UUID

#Properties to recieve on task submit
class TaskSubmit(EmployeeTaskBase):
    subbmited_by: UUID = Field(
        foreign_key="user.id", nullable=False, ondelete="CASCADE"
    )

#Properties to recieve on task approve
class TaskApprove(EmployeeTaskBase):
    pass

# Properties to receive on item update
class TaskUpdate(EmployeeTaskBase):
    title: str | None = Field(default=None, min_length=1, max_length=255)  # type: ignore

class EmployeeLevel(SQLModel, table=True):
    __tablename__ = "employee_levels"

    id: UUID = Field(default_factory=uuid4, primary_key=True, nullable=False)
    employee_id: Optional[UUID] = Field(
        foreign_key="user.id", nullable=True, unique=True, ondelete="CASCADE"
    )
    employee: "User" = Relationship(
        sa_relationship=RelationshipProperty(
            "User",
            back_populates="employee_level",
            foreign_keys='[EmployeeLevel.employee_id]')
    )
    level: int = Field(nullable=False, default=0, description="Current level of the employee.")
    #This would be for tracking history of leveling up
    level_start_date: datetime = Field(default_factory=datetime.now, nullable=False)
    level_end_date: Optional[datetime] = Field(default=None)
    xp: int = Field(default=0, nullable=False, description="Current XP points of the employee.")
    xp_multiplier: float = Field(default=1.0, description="XP multiplier based on company-level constraints.")
    created_at: datetime = Field(default_factory=datetime.now, nullable=False)
    updated_at: Optional[datetime] = Field(default=None, description="Last updated timestamp.")
    #Add this later, think if this is the right place
    #revenue_generated: Optional[float] = Field(default=0.0, description="Revenue generated by the employee.")
    #perks_granted: Optional[JSON] = Field(default=None, description="JSON data storing perks granted for this level.")
    #months_of_active_contract: int = Field(default=0, description="Number of months the employee has been active in the company.")
    