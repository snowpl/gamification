import datetime
from enum import Enum
from typing import Any, Optional
import uuid
from fastapi import APIRouter
from sqlmodel import func, select
from app.api.deps import CurrentUser, SessionDep
from app.models import AvailableTask, AvailableTasksPublic
from eventsourcing.application import Application
from eventsourcing.domain import Aggregate, event

router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.get("/", response_model=AvailableTasksPublic)
def read_tasks(
    session: SessionDep, current_user: CurrentUser, skip: int = 0, limit: int = 100, only_active: bool = True
) -> Any:
    """
    Retrieve tasks.
    """
    if current_user.is_superuser:
        count_statement = (
            select(func.count())
            .select_from(AvailableTask)
            .where(AvailableTask.is_active == only_active)
        )
        count = session.exec(count_statement).one()
        statement = select(AvailableTask).where(AvailableTask.is_active == only_active).offset(skip).limit(limit)
        tasks = session.exec(statement).all()
    else:
        count_statement = (
            select(func.count())
            .select_from(AvailableTask)
            .where(AvailableTask.company_id == current_user.company_id & AvailableTask.is_active == only_active)
        )
        count = session.exec(count_statement).one()
        statement = (
            select(AvailableTask)
            .where(AvailableTask.company_id == current_user.company_id & AvailableTask.is_active == only_active)
            .offset(skip)
            .limit(limit)
        )
        tasks = session.exec(statement).all()

    return AvailableTasksPublic(data=tasks, count=count)

class TaskStatus(Enum):
    ASSIGNED = "Assigned"
    IN_PROGRESS = "In Progress"
    WAITING_APPROVAL = "Waiting Approval"
    REJECTED = "Rejected"
    COMPLETED = "Completed"
    CANCELED = "Canceled"

class TaskError(Exception):
    pass

class TaskStateError(TaskError):
    pass

class TaskNotFoundError(TaskError):
    pass

class EmployeeTaskService(Application):
    def __init__(self, session: SessionDep):
        self.repository = session

    def get_available_task(self, id: uuid.UUID):
        return self.repository.get(AvailableTask, id)

    def assign_task(self, task_id: uuid.UUID, assigned_to_id: uuid.UUID, company_id: uuid.UUID):
        #This should get available_task
        available_task = self.repository.get(task_id)
        if not available_task:
            raise TaskNotFoundError(f"Available task with ID {task_id} not found.")
        
        #This should get user
        user = self.repository.get(assigned_to_id)
        if not user:
            raise TaskNotFoundError(f"User with ID {assigned_to_id} not found.")
        
        if not available_task.active:
            raise TaskStateError(f"Task {task_id} is not active.")
        
        #This calls the aggregate
        taskAssigned = EmployeeTask.TaskAssigned(task_id, assigned_to_id, company_id)
        user.assign_task(taskAssigned)

        self.save(taskAssigned)
        self.save(user)
        return taskAssigned.id

    def start_task(self, task_id: uuid.UUID):
        task = self.repository.get(task_id)
        if not task:
            raise TaskNotFoundError(f"Task with ID {task_id} not found.")
    
        if task.status != TaskStatus.ASSIGNED:
            raise TaskStateError(f"Task {task_id} cannot be started from status {task.status}.")
    
        task.start_task()
        self.save(task)
        
    def submit_task(self, task_id: uuid.UUID):
        task = self.repository.get(task_id)
        if not task:
            raise TaskNotFoundError(f"Task with ID {task_id} not found.")
        task.submit_task()
        self.save(task)

    def approve_task(self, employee_task_id: uuid.UUID, approved_by_id: uuid.UUID):
        #get user
        userApproving = self.repository.get(approved_by_id)
        if not userApproving.is_superuser:
            raise TaskStateError(f"User can't approve tasks.")
        #get the task
        employee_task = self.repository.get(employee_task_id)
        employee_task.approve(approved_by_id)
        self.save(employee_task)
        #task_completed = self.repository.get(employee_task.task_id)
        #task_completed.complete(employee_task.assigned_to_id)
        #self.save(task_completed)
        #TODO: Assign rewards, XP, Level-Up, etc.
        #function nextLevel(level) - BASED ON D&D
        #return 500 * (level ^ 2) - (500 * level)
        #local exponent = 1.5
        #local baseXP = 1000
        #return math.floor(baseXP * (level ^ exponent))

    def reject_task(self, task_id: uuid.UUID, reason: str, rejected_by_id: uuid.UUID):
        task = self.repository.get(task_id)
        if not task:
            raise TaskNotFoundError(f"Task with ID {task_id} not found.")
        task.reject(rejected_by_id, reason)
        self.save(task)

    def cancel_task(self, task_id: uuid.UUID, reason: str, cancelled_by_id: uuid.UUID):
        task = self.repository.get(task_id)
        if not task:
            raise TaskNotFoundError(f"Task with ID {task_id} not found.")
        if not task.assigned_to_id == cancelled_by_id:
            raise TaskStateError(f"Task {task_id} can't be canceled by user {cancelled_by_id}")
        task.cancel(cancelled_by_id, reason)
        self.save(task)

class EmployeeTask(Aggregate):
    @event("TaskAssigned")
    def __init__(self, task_id: uuid.UUID, assigned_to_id: uuid.UUID, company_id: uuid.UUID):
        self.task_id = task_id
        self.assigned_to_id = assigned_to_id
        self.company_id = company_id
        self.status = TaskStatus.ASSIGNED
        self.created_at = datetime.datetime.now()
        self.started_at = None
        self.submitted_at = None
        self.completed_at = None
        self.requires_approval = False
        self.approved_by_id = None
        self.rejection_reason = None

    @event("TaskStarted")
    def start_task(self) -> None:
        self.status = TaskStatus.IN_PROGRESS
        self.started_at = datetime.datetime.now()

    @event("TaskSubmitted")
    def submit_task(self) -> None:
        self.submitted_at = datetime.datetime.now()
        if(self.requires_approval):
            self.status = TaskStatus.WAITING_APPROVAL
        else:
            self.completed_at = self.submitted_at
            self.status = TaskStatus.COMPLETED

    @event("TaskApproved")
    def approve_task(self, approved_by_id: uuid.UUID) -> None:
        if self.stats == TaskStatus.WAITING_APPROVAL:
            self.completed_at = datetime.datetime.now()
            self.approved_by_id = approved_by_id
            self.status = TaskStatus.COMPLETED
        else:
            raise TaskStateError(f"Task {self.task_id} is in state {self.status} and can't be approved.")

    @event("TaskRejected")
    def reject_task(self, approved_by_id: uuid.UUID, reason: str) -> None:
        if self.status == TaskStatus.WAITING_APPROVAL:
            self.rejection_reason = reason
            self.approved_by_id = approved_by_id
            self.completed_at = datetime.datetime.now()
            self.status = TaskStatus.REJECTED
        else:
            raise TaskStateError(f"Task {self.task_id} is in state {self.status} and can't be rejected.")

    @event("TaskCanceled")
    def cancel_task(self, approved_by_id: uuid.UUID, reason:str) -> None:
        self.rejection_reason = reason
        self.approved_by_id = approved_by_id
        self.completed_at = datetime.datetime.now()
        self.status = TaskStatus.CANCELED
