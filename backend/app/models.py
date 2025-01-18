import uuid

from pydantic import EmailStr
from sqlmodel import Field, Relationship, SQLModel


# Shared properties
class UserBase(SQLModel):
    email: EmailStr = Field(unique=True, index=True, max_length=255)
    is_active: bool = True
    is_superuser: bool = False
    full_name: str | None = Field(default=None, max_length=255)
    company_id: uuid.UUID = Field(foreign_key="company.id")
    #department_id: uuid.UUID = Field(foreign_key="department.id")
    company: "Company" = Relationship(back_populates="employees")
    #department: "Department" = Relationship(back_populates="employees")

# Properties to receive via API on creation
class UserCreate(UserBase):
    password: str = Field(min_length=8, max_length=40)


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
    employees: list["User"] = Relationship(back_populates="company", cascade_delete=True)
    #departments: list["Department"] = Relationship(back_populates="company", cascade_delete=True)

#Database model
class Company(CompanyBase, table=True):
    is_active: bool = True 

# #Shared properties
# class SkillBase(SQLModel):
#     id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
#     name: str = Field(min_length=1, max_length=255)
#     description: str | None = Field(default=None, max_length=500)
#     current_xp: int = 0
#     department_id: uuid.UUID = Field(
#         foreign_key="department.id", nullable=False, ondelete="CASCADE"
#     )
#     department: "Department" = Relationship(back_populates="skills")

# #Database model
# class Skill(SkillBase, table=True):
#     pass

# #Shared properties
# class LevelBase(SQLModel):
#     level: int = 0
#     required_xp: int = 0

# #Database model
# class Level(LevelBase, table=True):
#     reward: str | None = Field(default=None, max_length=255)
#     type: str | None = Field(default=None, max_length=255)

# # Shared properties
# class DepartmentBase(SQLModel):
#     id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
#     name: str = Field(min_length=1, max_length=255)
#     current_xp: int = 0
#     level: int = 0
#     company_id: uuid.UUID = Field(
#         foreign_key="company.id", nullable=False, ondelete="CASCADE"
#     )
#     skills: list["Skill"] = Relationship(back_populates="department", cascade_delete=True)
#     tasks: list["Task"] = Relationship(back_populates="department", cascade_delete=True)
#     #company: "Company" = Relationship(back_populates="company", cascade_delete=True)
#     #employees: list["User"] = Relationship(back_populates="department", cascade_delete=True)

# # Properties to receive a department
# class DepartmentReceive(DepartmentBase):
#     current_level: int = 0
#     required_xp: int = 0
#     pass

# #Database model
# class Department(DepartmentBase, table=True):
#     pass

# # Shared properties
# class TaskBase(SQLModel):
#     title: str = Field(min_length=1, max_length=255)
#     description: str | None = Field(default=None, max_length=255)
#     requires_approval: bool = False
#     approved: bool = False
#     approved_by: uuid.UUID = Field(
#         foreign_key="user.id", nullable=False, ondelete="CASCADE"
#     )
#     department_id: uuid.UUID = Field(
#         foreign_key="department.id", nullable=False, ondelete="CASCADE"
#     )
#     skill_id: uuid.UUID = Field(
#         foreign_key="skill.id", nullable=False, ondelete="CASCADE"
#     )
#     department_xp: int = 0
#     skill_xp: int = 0
#     company_xp: int = 0
#     person_xp: int = 0
#     department: "Department" = Relationship(back_populates="tasks")

# # Database model, database table inferred from class name
# class Task(TaskBase, table=True):
#     id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
#     title: str = Field(max_length=255)
#     owner_id: uuid.UUID = Field(
#         foreign_key="user.id", nullable=False, ondelete="CASCADE"
#     )
#     owner: User | None = Relationship(back_populates="tasks")

# #Database model
# class Task(TaskBase, table=True):
#     pass

# # Properties to receive on item creation
# class TaskCreate(TaskBase):
#     pass

# #Properties to recieve on task submit
# class TaskSubmit(TaskBase):
#     subbmited_by: uuid.UUID = Field(
#         foreign_key="user.id", nullable=False, ondelete="CASCADE"
#     )
#     pass

# #Properties to recieve on task approve
# class TaskApprove(TaskBase):
#     pass

# # Properties to receive on item update
# class TaskUpdate(TaskBase):
#     title: str | None = Field(default=None, min_length=1, max_length=255)  # type: ignore

# # Properties to return via API, id is always required
# class TaskPublic(TaskBase):
#     id: uuid.UUID
#     owner_id: uuid.UUID

# class TasksPublic(SQLModel):
#     data: list[TaskPublic]
#     count: int