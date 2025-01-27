from uuid import UUID, uuid4
from sqlmodel import SQLModel, Field

#Shared properties
class SkillBase(SQLModel):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    name: str = Field(min_length=1, max_length=255)
    description: str | None = Field(default=None, max_length=500)

#Skill properties to recieve on creation
class GlobalSkillCreate(SkillBase):
    department_id: UUID

class SkillPublic(SQLModel):
    name: str
    xp: int = 0
    level: int = 0
    missing_xp: int = 0

class EmployeeSkillCreate(SQLModel):
    xp: int = 0
    level: int = 0
    user_id: UUID
    skill_id: UUID