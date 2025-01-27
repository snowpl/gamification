from datetime import datetime
from uuid import UUID, uuid4
from dataclasses import dataclass
from app.models import TaskStatus

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
    approved_by_id: UUID

@dataclass
class TaskSubmittedEvent(TaskEventDomain):
    pass

@dataclass
class TaskRejectedEvent(TaskEventDomain):
    reason: str
    approved_by_id: UUID

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
    approved_by_id: UUID

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
    approved_by_id: UUID | None
    submitted_at: datetime | None
    version: int = 1
    status: TaskStatus = TaskStatus.ASSIGNED
    requires_approval: bool = False

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
                   status=TaskStatus.ASSIGNED
        )
        return task, event
