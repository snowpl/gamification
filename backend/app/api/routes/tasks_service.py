from datetime import datetime
from enum import Enum
from typing import Dict, List, Any, Optional
from uuid import UUID, uuid4
from dataclasses import asdict, dataclass
from functools import singledispatch
from fastapi import APIRouter
from sqlalchemy.orm import Session
from sqlalchemy import select, insert
from typing import Optional, List
from sqlmodel import func, select
from app.models import AvailableTask, AvailableTasksPublic, EmployeeTask, TaskEvent, TaskStatus

#region Domain Events
@dataclass
class TaskEventDomain:
    aggregate_id: UUID
    timestamp: datetime
    version: int

@dataclass
class TaskAssignedEvent(TaskEventDomain):
    assigned_to_id: UUID
    task_id: UUID

@dataclass
class TaskCompletedEvent(TaskEventDomain):
    assigned_to_id: UUID
    task_id: UUID

@dataclass
class TaskSubmittedEvent(TaskEventDomain):
    pass

@dataclass
class TaskRejectedEvent(TaskEventDomain):
    reason: str

@dataclass
class TaskCancelledEvent(TaskEventDomain):
    reason: str
#endregion

#region Commands
@dataclass
class Command:
    aggregate_id: UUID

@dataclass
class AssignTaskCommand:
    assigned_to_id: UUID
    task_id: UUID
    title: str
    description: str
    requires_approval: bool

@dataclass
class SubmitTaskCommand(Command):
    pass

@dataclass
class ApproveTaskCommand(Command):
    approved_by_id: UUID

@dataclass
class RejectTaskCommand(Command):
    reason: str

@dataclass
class CancelTaskCommand(Command):
    reason: str
#endregion

# Domain Model
@dataclass
class EmployeeTaskDomain:
    id: UUID
    title: str
    description: str
    task_id: UUID
    assigned_to_id: UUID
    completed_at: datetime | None
    created_at: datetime
    reason: str
    version: int = 1
    status: TaskStatus = TaskStatus.ASSIGNED
    requires_approval: bool = False
    approved_by_id: UUID | None
    submitted_at: datetime | None

    @classmethod
    def create(cls, command: AssignTaskCommand) -> tuple['EmployeeTaskDomain', TaskAssignedEvent]:
        id = uuid4()
        event = TaskAssignedEvent(
            aggregate_id=id,
            task_id = command.task_id,
            assigned_to_id=command.assigned_to_id,
            timestamp=datetime.now(),
            version=1
        )
        task = cls(id=id, 
                   task_id=command.task_id, 
                   created_at=event.timestamp, 
                   title=command.title, 
                   description=command.description,
                   assigned_to_id=command.assigned_to_id,
                   completed_at=None,
                   reason="",
                   requires_approval=command.requires_approval,
                   approved_by_id=None,
                   submitted_at=None,
        )
        return task, event

#region Event Handler

# Event Handler using Single Dispatch
@singledispatch
def apply_event(event: TaskEventDomain, task: EmployeeTask | None) -> EmployeeTask:
    raise ValueError(f"Unknown event type: {type(event)}")

@apply_event.register
def _(event: TaskAssignedEvent, task: EmployeeTask | None) -> EmployeeTask:
    return EmployeeTask(
        id=task.id,
        title=task.title,
        version=event.version,
        task_id=event.task_id,
        assigned_to_id=event.assigned_to_id,
        status=TaskStatus.ASSIGNED,
        created_at=event.timestamp,
        requires_approval=task.requires_approval
    )

@apply_event.register
def _(event: TaskCompletedEvent, task: EmployeeTask | None) -> EmployeeTask:
    return EmployeeTask(
        id=task.id,
        title=task.title,
        description=task.description,
        version=task.version,
        task_id=task.task_id,
        assigned_to_id=task.assigned_to_id,
        status=TaskStatus.COMPLETED,
        created_at=task.created_at,
        completed_at=datetime.now()
    )

@apply_event.register
def _(event: TaskCancelledEvent, task: EmployeeTask | None) -> EmployeeTask:
    return EmployeeTask(
        id=task.id,
        title=task.title,
        description=task.description,
        version=task.version,
        task_id=task.task_id,
        assigned_to_id=task.assigned_to_id,
        status=TaskStatus.CANCELED,
        created_at=task.created_at,
        completed_at=datetime.now(),
        reason=event.reason
    )

@apply_event.register
def _(event: TaskSubmittedEvent, task: EmployeeTask | None) -> EmployeeTask:
    return EmployeeTask(
        id=task.id,
        title=task.title,
        description=task.description,
        version=task.version,
        task_id=task.task_id,
        assigned_to_id=task.assigned_to_id,
        status=TaskStatus.WAITING_APPROVAL,
        created_at=task.created_at,
        completed_at=task.created_at,
        submitted_at=datetime.now()
    )

@apply_event.register
def _(event: TaskRejectedEvent, task: EmployeeTask | None) -> EmployeeTask:
    return EmployeeTask(
        id=task.id,
        title=task.title,
        description=task.description,
        version=task.version,
        task_id=task.task_id,
        assigned_to_id=task.assigned_to_id,
        status=TaskStatus.REJECTED,
        created_at=task.created_at,
        completed_at=datetime.now(),
        reason=event.reason
    )
#endregion

#region Command Handler using Single Dispatch
@singledispatch
def handle_command(command: Command, task: EmployeeTask | None) -> Optional[TaskEventDomain]:
    raise ValueError(f"Unknown command type: {type(command)}")

#This should be handled by def create in employee_task
@handle_command.register
def _(command: AssignTaskCommand, task: EmployeeTask | None) -> TaskAssignedEvent:
    id = uuid4()
    return TaskAssignedEvent(
            aggregate_id=id,
            task_id = command.task_id,
            assigned_to_id=command.assigned_to_id,
            timestamp=datetime.now(),
            version=1
    )

@handle_command.register
def _(command: SubmitTaskCommand, task: EmployeeTask | None) -> TaskCompletedEvent | TaskSubmittedEvent:
    if task.status == TaskStatus.WAITING_APPROVAL | task.status == TaskStatus.ASSIGNED:
        if task.requires_approval:
            return TaskSubmittedEvent(
            aggregate_id=task.id,
            timestamp=datetime.now(),
            version=task.version
            )
        return TaskCompletedEvent(
            aggregate_id=task.id,
            timestamp=datetime.now(),
            version=task.version,
            assigned_to_id=task.assigned_to_id,
            task_id=task.task_id
        )
    return None

@handle_command.register
def _(command: ApproveTaskCommand, task: EmployeeTask | None) -> TaskCompletedEvent:
    if task.status == TaskStatus.WAITING_APPROVAL:
        return TaskCompletedEvent(
            aggregate_id=task.id,
            timestamp=datetime.now(),
            version=task.version,
            assigned_to_id=task.assigned_to_id,
            task_id=task.task_id
        )
    return None

@handle_command.register
def _(command: RejectTaskCommand, task: EmployeeTask | None) -> TaskRejectedEvent:
    if task.status == TaskStatus.WAITING_APPROVAL:
        return TaskRejectedEvent(
            aggregate_id=task.id,
            timestamp=datetime.now(),
            version=task.version,
            reason=command.reason
        )
    return None

@handle_command.register
def _(command: CancelTaskCommand, task: EmployeeTask) -> TaskCancelledEvent:
    return TaskCancelledEvent(
        aggregate_id=task.id,
        timestamp=datetime.now(),
        version=task.version,
        reason=command.reason
    )
#endregion

#region Repository Interface
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

        # Handle specific event types for additional fields
        if isinstance(event, TaskAssignedEvent):
            event_data.update({"assigned_to_id": event.assigned_to_id, "task_id": event.task_id, "event_type":"TaskAssignedEvent"})
        elif isinstance(event, TaskSubmittedEvent):
            event_data.update({"event_type":"TaskSubmittedEvent"})
        elif isinstance(event, TaskCompletedEvent):
            event_data.update({"assigned_to_id": event.assigned_to_id, "task_id": event.task_id, "event_type":"TaskCompletedEvent"})
        elif isinstance(event, TaskCancelledEvent):
            event_data.update({"reason": event.reason, "event_type":"TaskCancelledEvent"})
        elif isinstance(event, TaskRejectedEvent):
            event_data.update({"reason": event.reason, "event_type":"TaskRejectedEvent"})
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

#endregion

class TaskService:
    def __init__(self, repository: TaskRepository):
        self.repository = repository

    def get_employee_taks(self, id: UUID) -> List[EmployeeTask]:
        return self.repository.get_user_tasks(id)

    def get_aggregates(self, id: UUID) -> List[TaskEvent]:
        return self.repository.get_events(id)

    def create_task(self, command: AssignTaskCommand) -> UUID:
        task, event = EmployeeTaskDomain.create(command)
        self.repository.save(EmployeeTask(**asdict(task)))
        self.repository.save_event(event)
        return task.id

    def handle_command(self, command: Command) -> TaskEvent:
        # Retrieve the task by ID
        task = self.repository.get_by_id(command.aggregate_id)
        
        # If the task doesn't exist, raise an error
        if task is None:
            raise ValueError(f"Task {command.aggregate_id} not found")

        # Generate the appropriate event using the command handler
        event = handle_command(command, task)

        # If no event is generated (e.g., task already completed), do nothing
        if event is None:
            return

        # Apply the event to update the task's state
        updated_task = apply_event(event, task)

        # Save the updated task and the event to the repository
        self.repository.save(updated_task)
        self.repository.save_event(event)
        return event

