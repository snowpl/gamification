from datetime import datetime
from functools import singledispatch
from typing import List, Optional
from uuid import UUID
from requests import Session
from sqlalchemy import select, insert
from app.models import AvailableTask, EmployeeLevel, Skill
from app.api.users.skills_models import SkillCreate

# #region Repository Interface
# @singledispatch
# def update_event_data(event, event_data):
#     raise ValueError(f"Unhandled event type: {type(event)}")

# @update_event_data.register
# def _(event: TaskAssignedEvent, event_data: dict):
#     event_data.update({
#         "assigned_to_id": event.assigned_to_id,
#         "task_id": event.task_id,
#         "event_type": "TaskAssignedEvent"
#     })

class LevelsRepository:
    def save(self, level: EmployeeLevel) -> None:
        raise NotImplementedError

    def get_task(self, task_id: UUID) -> AvailableTask:
        raise NotImplementedError

    def get_level(self, employee_id: UUID) -> EmployeeLevel:
        raise NotImplementedError
    
    def get_skill(self, skill_id: UUID) -> Skill:
        raise NotImplementedError
    
    def get_employee_skill(self, skill_id: UUID, employee_id: UUID) -> Optional[Skill]:
        raise NotImplementedError

    def create_skill(self, skill_in: SkillCreate) -> Skill:
        raise NotImplementedError
    
    # def get_by_id(self, task_id: UUID) -> Optional[EmployeeTask]:
    #     raise NotImplementedError

    # def get_events(self, task_id: UUID) -> List[TaskEvent]:
    #     raise NotImplementedError

class PostgresLevelsRepository(LevelsRepository):
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def save(self, level: EmployeeLevel) -> None:
        existing_level = self.get_by_id(level.id)
        if existing_level:
            # Update the task
            existing_level.updated_at = datetime.now()
            self.db_session.merge(level)
        else:
            # Add a new task
            self.db_session.add(level)
        self.db_session.commit()

    def get_task(self, task_id: UUID) -> AvailableTask:
        query = select(AvailableTask).where(AvailableTask.id==task_id)
        result = self.db_session.execute(query).scalars().one()
        return result
    
    def get_level(self, employee_id: UUID) -> EmployeeLevel:
        query = select(EmployeeLevel).where(EmployeeLevel.employee_id==employee_id)
        result = self.db_session.execute(query).scalars().one()
        return result
    
    def get_skill(self, skill_id: UUID) -> Skill:
        query = select(Skill).where(Skill.id==skill_id)
        result = self.db_session.execute(query).scalars().one()
        return result

    def get_employee_skill(self, skill_id: UUID, user_id: UUID) -> Optional[Skill]:
        query = select(Skill).where((Skill.id==skill_id) & (Skill.user_id == user_id))
        result = self.db_session.execute(query).scalars().one_or_none()
        return result
    
    def create_skill(self, skill_in: SkillCreate) -> Skill:
        db_skill = Skill.model_validate(skill_in)
        self.db_session.add(db_skill)
        self.db_session.commit()
        return db_skill
    
    # def save_event(self, event: TaskEvent) -> None:
    #     # Convert the event to a dict representation if needed
    #     event_data = {
    #         "aggregate_id": event.aggregate_id,
    #         "timestamp": event.timestamp,
    #         "version": event.version
    #     }

    #     # Call the handler
    #     update_event_data(event, event_data)
    #     self.db_session.execute(insert(TaskEvent).values(event_data))
    #     self.db_session.commit()
        
    def get_by_id(self, id: UUID) -> Optional[EmployeeLevel]:
        query = select(EmployeeLevel).where(EmployeeLevel.id==id)
        result = self.db_session.execute(query).scalar_one_or_none()
        return result

    # def get_events(self, id: UUID) -> List[TaskEvent]:
    #     query = select(TaskEvent).filter_by(aggregate_id=id).order_by(TaskEvent.timestamp)
    #     result = self.db_session.execute(query).scalars().all()
    #     return result
    
    # def get_user_tasks(self, id: UUID) -> List[EmployeeTask]:
    #     query = select(EmployeeTask).where(EmployeeTask.assigned_to_id==id)
    #     result = self.db_session.execute(query).scalars().all()
    #     return result
