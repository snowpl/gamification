from functools import singledispatch
from typing import List, Optional
from uuid import UUID
from requests import Session
from sqlalchemy import select, insert
from app.models import EmployeeTask, TaskEvent
from app.tasks.task_models import TaskAssignedEvent, TaskCancelledEvent, TaskCompletedEvent, TaskRejectedEvent, TaskSubmittedEvent


#region Repository Interface
@singledispatch
def update_event_data(event, event_data):
    raise ValueError(f"Unhandled event type: {type(event)}")

@update_event_data.register
def _(event: TaskAssignedEvent, event_data: dict):
    event_data.update({
        "assigned_to_id": event.assigned_to_id,
        "task_id": event.task_id,
        "event_type": "TaskAssignedEvent"
    })

# Handle specific event types for additional fields
@update_event_data.register
def _(event: TaskSubmittedEvent, event_data: dict):
    event_data.update({
        "event_type": "TaskSubmittedEvent"
    })

@update_event_data.register
def _(event: TaskCompletedEvent, event_data: dict):
    event_data.update({
        "assigned_to_id": event.assigned_to_id,
        "task_id": event.task_id,
        "event_type": "TaskCompletedEvent",
        "approved_by_id": event.approved_by_id
    })

@update_event_data.register
def _(event: TaskCancelledEvent, event_data: dict):
    event_data.update({
        "reason": event.reason,
        "event_type": "TaskCancelledEvent"
    })

@update_event_data.register
def _(event: TaskRejectedEvent, event_data: dict):
     event_data.update({
        "reason": event.reason,
        "event_type": "TaskRejectedEvent",
        "approved_by_id": event.approved_by_id
    })


class TaskRepository:
    def save(self, task: EmployeeTask) -> None:
        raise NotImplementedError

    def save_event(self, event: TaskEvent) -> None:
        raise NotImplementedError

    def get_by_id(self, task_id: UUID) -> Optional[EmployeeTask]:
        raise NotImplementedError

    def get_events(self, task_id: UUID) -> List[TaskEvent]:
        raise NotImplementedError

class PostgresTaskRepository(TaskRepository):
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def save(self, task: EmployeeTask) -> None:
        existing_task = self.get_by_id(task.id)
        if existing_task:
            # Update the task
            self.db_session.merge(task)
        else:
            # Add a new task
            self.db_session.add(task)
        self.db_session.commit()

    def save_event(self, event: TaskEvent) -> None:
        # Convert the event to a dict representation if needed
        event_data = {
            "aggregate_id": event.aggregate_id,
            "timestamp": event.timestamp,
            "version": event.version
        }

        # Call the handler
        update_event_data(event, event_data)
        self.db_session.execute(insert(TaskEvent).values(event_data))
        self.db_session.commit()
        
    def get_by_id(self, id: UUID) -> Optional[EmployeeTask]:
        query = select(EmployeeTask).where(EmployeeTask.id==id)
        result = self.db_session.execute(query).scalar_one_or_none()
        return result

    def get_events(self, id: UUID) -> List[TaskEvent]:
        query = select(TaskEvent).filter_by(aggregate_id=id).order_by(TaskEvent.timestamp)
        result = self.db_session.execute(query).scalars().all()
        return result
    
    def get_user_tasks(self, id: UUID) -> List[EmployeeTask]:
        query = select(EmployeeTask).where(EmployeeTask.assigned_to_id==id)
        result = self.db_session.execute(query).scalars().all()
        return result
