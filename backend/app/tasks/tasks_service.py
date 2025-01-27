from datetime import datetime
from typing import List, Optional
from uuid import UUID, uuid4
from dataclasses import asdict
from functools import singledispatch
from typing import Optional, List
from app.tasks.task_repository import TaskRepository
from app.models import EmployeeTask, TaskEvent, TaskStatus
from app.tasks.task_models import ApproveTaskCommand, AssignTaskCommand, CancelTaskCommand, Command, EmployeeTaskDomain, RejectTaskCommand, SubmitTaskCommand, TaskAssignedEvent, TaskCancelledEvent, TaskCompletedEvent, TaskEventDomain, TaskRejectedEvent, TaskSubmittedEvent

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
        requires_approval=task.requires_approval,
        reason=task.reason
    )

@apply_event.register
def _(event: TaskCompletedEvent, task: EmployeeTask | None) -> EmployeeTask:
    return EmployeeTask(
        id=task.id,
        title=task.title,
        description=task.description,
        version=task.version,
        task_id=event.task_id,
        assigned_to_id=task.assigned_to_id,
        status=TaskStatus.COMPLETED,
        created_at=task.created_at,
        completed_at=datetime.now(),
        approved_by_id=event.approved_by_id,
        submitted_at=task.submitted_at,
        reason=task.reason
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
        submitted_at=datetime.now(),
        reason=task.reason
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
    if task.status == TaskStatus.WAITING_APPROVAL or task.status == TaskStatus.ASSIGNED:
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
            task_id=task.task_id,
            approved_by_id=task.assigned_to_id
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
            task_id=task.task_id,
            approved_by_id=command.approved_by_id
        )
    return None

@handle_command.register
def _(command: RejectTaskCommand, task: EmployeeTask | None) -> TaskRejectedEvent:
    if task.status == TaskStatus.WAITING_APPROVAL:
        return TaskRejectedEvent(
            aggregate_id=task.id,
            timestamp=datetime.now(),
            version=task.version,
            reason=command.reason,
            approved_by_id=command.approved_by_id
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

class TaskService:
    def __init__(self, repository: TaskRepository):
        self.repository = repository

    def get_employee_task(self, id: UUID) -> List[EmployeeTask]:
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
        print('saved task:')
        print(updated_task)
        self.repository.save_event(event)
        print('saved event:')
        print(event)
        return event
