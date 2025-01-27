from typing import Optional
from uuid import UUID, uuid4
from sqlmodel import SQLModel, Field

#Shared properties
class SkillBase(SQLModel):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    name: str = Field(min_length=1, max_length=255)
    description: str | None = Field(default=None, max_length=500)
    xp: int = 0
    level: int = 0

#Skill properties to recieve on creation
class SkillCreate(SkillBase):
    department_id: UUID
    user_id: Optional[UUID] = None  # Make user_id optional

class SkillPublic(SQLModel):
    name: str
    xp: int = 0
    level: int = 0
    missing_xp: int = 0