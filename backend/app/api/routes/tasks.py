from datetime import datetime
from enum import Enum
from typing import Dict, List, Any, Optional
from uuid import UUID, uuid4
from dataclasses import dataclass
from functools import singledispatch
from fastapi import APIRouter
from sqlalchemy.orm import Session
from sqlalchemy import select, insert
from typing import Optional, List
from app.api.routes.tasks_service import ApproveTaskCommand, AssignTaskCommand, CancelTaskCommand, Command, RejectTaskCommand, SubmitTaskCommand, TaskEventDomain
from sqlmodel import func, select
from app.api.deps import CurrentUser, SessionDep, TaskServiceDep
from app.models import AvailableTask, AvailableTasksPublic, EmployeeTask, TaskEvent, TaskStatus

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

@router.post("/assign-task", response_model=UUID)
def assign_task(
     task_in: AssignTaskCommand, taskService: TaskServiceDep
) -> Any:
    """
    Assign task.
    """
    task_id = taskService.create_task(task_in)
    return task_id

@router.patch("/submit-task", response_model=TaskEventDomain)
def submit_task(taskSerivce: TaskServiceDep, taskCommand: SubmitTaskCommand) -> Any:
    """
    Submit task.
    """
    print('submit-task')
    tasks = taskSerivce.handle_command(taskCommand)
    print(tasks)
    return tasks

@router.patch("/approve-task", response_model=TaskEventDomain)
def submit_task(taskSerivce: TaskServiceDep, current_user: CurrentUser, taskCommand: Command) -> Any:
    """
    Submit task.
    """
    tasks = taskSerivce.handle_command(ApproveTaskCommand(taskCommand.aggregate_id, current_user.id))
    return tasks

@router.patch("/reject-task", response_model=TaskEventDomain)
def submit_task(taskSerivce: TaskServiceDep, taskCommand: RejectTaskCommand) -> Any:
    """
    Submit task.
    """
    tasks = taskSerivce.handle_command(taskCommand)
    return tasks

@router.patch("/cancel-task", response_model=TaskEventDomain)
def cancel_task(taskSerivce: TaskServiceDep, taskCommand: CancelTaskCommand) -> Any:
    """
    Cancel task.
    """
    tasks = taskSerivce.handle_command(taskCommand)
    return tasks

@router.get("/employee-tasks/{id}", response_model=List[EmployeeTask])
def get_employee_tasks(taskService: TaskServiceDep, id: UUID) -> Any:
    """
    Get employee tasks.
    """
    tasks = taskService.get_employee_task(id)
    return tasks

@router.get("/events/{id}", response_model=list[TaskEvent])
def get_tasks_event(taskService: TaskServiceDep, id: UUID) -> Any:
    """
    Get events.
    """
    events = taskService.get_aggregates(id)
    return events

#         #TODO: Assign rewards, XP, Level-Up, etc.
#         #function nextLevel(level) - BASED ON D&D
#         #return 500 * (level ^ 2) - (500 * level)
#         #local exponent = 1.5
#         #local baseXP = 1000
#         #return math.floor(baseXP * (level ^ exponent))
