from typing import Optional
import uuid
from pydantic import EmailStr
from sqlmodel import Field, Relationship, SQLModel
from sqlalchemy.orm import RelationshipProperty

# Shared properties
class UserBase(SQLModel):
    email: EmailStr = Field(unique=True, index=True, max_length=255)
    is_active: bool = True
    is_superuser: bool = False
    full_name: str | None = Field(default=None, max_length=255)
    current_xp: int = 0

# Properties to receive via API on creation
class UserCreate(UserBase):
    password: str = Field(min_length=8, max_length=40)
    company_id: uuid.UUID
    department_id: uuid.UUID

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
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    hashed_password: str
    items: list["Item"] = Relationship(back_populates="owner", cascade_delete=True)
    company: "Company" = Relationship(back_populates="employees")
    department: "Department" = Relationship(back_populates="employees")
    company_id: uuid.UUID = Field(
        foreign_key="company.id", nullable=False, ondelete="CASCADE"
    )
    department_id: uuid.UUID = Field(foreign_key="department.id")
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

# Properties to return via API, id is always required
class UserPublic(UserBase):
    id: uuid.UUID


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
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    title: str = Field(max_length=255)
    owner_id: uuid.UUID = Field(
        foreign_key="user.id", nullable=False, ondelete="CASCADE"
    )
    owner: User | None = Relationship(back_populates="items")


# Properties to return via API, id is always required
class ItemPublic(ItemBase):
    id: uuid.UUID
    owner_id: uuid.UUID


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
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
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
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    name: str = Field(min_length=1, max_length=255)
    description: str | None = Field(default=None, max_length=500)
    current_xp: int = 0

#Database model
class Skill(SkillBase, table=True):
    user_id: Optional[uuid.UUID] = Field(
        foreign_key="user.id", nullable=True, ondelete="CASCADE"
    )
    user: Optional["User"] = Relationship(back_populates="user_skills")
    department_id: uuid.UUID = Field(
        foreign_key="department.id", nullable=False, ondelete="CASCADE"
    )
    department: "Department" = Relationship(back_populates="department_skills")
    employee_tasks: list["EmployeeTask"] = Relationship(back_populates="skill", cascade_delete=True)

#Skill properties to recieve on creation
class SkillCreate(SkillBase):
    department_id: uuid.UUID
    user_id: Optional[uuid.UUID] = None  # Make user_id optional

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
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    name: str = Field(min_length=1, max_length=255)
    current_xp: int = 0
    level: int = 0

#Database model
class Department(DepartmentBase, table=True):
    company_id: uuid.UUID = Field(
        foreign_key="company.id", nullable=False, ondelete="CASCADE"
    )
    company: "Company" = Relationship(back_populates="departments")
    employees: list["User"] = Relationship(back_populates="department", cascade_delete=True)
    tasks: list["EmployeeTask"] = Relationship(back_populates="department", cascade_delete=True)
    department_skills: list["Skill"] = Relationship(back_populates="department", cascade_delete=True)

#Properties to receive on department creation
class DepartmentCreate(DepartmentBase):
    company_id: uuid.UUID

# # Shared properties
class EmployeeTaskBase(SQLModel):
    title: str = Field(min_length=1, max_length=255)
    description: str | None = Field(default=None, max_length=255)
    requires_approval: bool = False
    approved: bool = False
    department_xp: int = 0
    skill_xp: int = 0
    company_xp: int = 0
    person_xp: int = 0

# Database model, database table inferred from class name
class EmployeeTask(EmployeeTaskBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    title: str = Field(max_length=255)
    assigned_to_id: Optional[uuid.UUID] = Field(
        foreign_key="user.id", nullable=True, ondelete="CASCADE"
    )
    assigned_to: Optional["User"] = Relationship(
        sa_relationship=RelationshipProperty(
            "User",
            back_populates="employee_tasks",
            foreign_keys='[EmployeeTask.assigned_to_id]')
    )
    approved_by_id: Optional[uuid.UUID] = Field(
        foreign_key="user.id", nullable=True, ondelete="CASCADE"
    )
    approved_by: Optional["User"] = Relationship(
        sa_relationship=RelationshipProperty(
            "User",
            back_populates="approved_tasks",
            foreign_keys='[EmployeeTask.approved_by_id]')
    )
    department_id: uuid.UUID = Field(
        foreign_key="department.id", nullable=False, ondelete="CASCADE"
    )
    department: "Department" = Relationship(back_populates="tasks")
    skill_id: uuid.UUID = Field(
        foreign_key="skill.id", nullable=False, ondelete="CASCADE"
    )
    skill: "Skill" = Relationship(back_populates="employee_tasks")

# Properties to receive on item creation
class TaskCreate(EmployeeTaskBase):
    pass

#Properties to recieve on task submit
class TaskSubmit(EmployeeTaskBase):
    subbmited_by: uuid.UUID = Field(
        foreign_key="user.id", nullable=False, ondelete="CASCADE"
    )

#Properties to recieve on task approve
class TaskApprove(EmployeeTaskBase):
    pass

# Properties to receive on item update
class TaskUpdate(EmployeeTaskBase):
    title: str | None = Field(default=None, min_length=1, max_length=255)  # type: ignore

# Properties to return via API, id is always required
class TaskPublic(EmployeeTaskBase):
    id: uuid.UUID
    owner_id: uuid.UUID

class TasksPublic(SQLModel):
    data: list[TaskPublic]
    count: int