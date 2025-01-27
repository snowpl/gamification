from typing import List, Any
from uuid import UUID
from fastapi import APIRouter
from sqlalchemy import select, insert, func
from typing import List
from app.tasks.tasks_service import ApproveTaskCommand, AssignTaskCommand, CancelTaskCommand, Command, RejectTaskCommand, SubmitTaskCommand, TaskEventDomain
from app.tasks.task_models import TaskCompletedEvent
from sqlmodel import func, select
from app.api.deps import CurrentUser, SessionDep, TaskServiceDep, LevelsServiceDep
from app.models import AvailableTask, AvailableTaskPublic, AvailableTasksPublic, Department, EmployeeTask, TaskEvent

router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.get("/", response_model=AvailableTasksPublic)
def read_tasks(
    session: SessionDep, current_user: CurrentUser, skip: int = 0, limit: int = 100, only_active: bool = True
) -> Any:
    """
    Retrieve available tasks.
    """
    # if current_user.is_superuser:
    count_statement = (
            select(func.count())
            .select_from(AvailableTask)
            .where(AvailableTask.is_active == only_active)
        )
    count = session.exec(count_statement).one()
    statement = (select(
                AvailableTask, 
                Department.name.label("department_name"), 
                Department.id.label("department_id")
            )
            .join(Department, Department.id == AvailableTask.department_id)
            .where(AvailableTask.is_active == only_active)
            .offset(skip)
            .limit(limit)
        )
    result = session.exec(statement).all()
    
    tasks = [
        AvailableTaskPublic(
            id=row.id,
            title=row.title,
            description=row.description,
            requires_approval=row.requires_approval,
            department_id=department_id,
            department_name=department_name,
            is_active=row.is_active,
            department_xp= row.department_xp,
            skill_xp = row.skill_xp,
            company_xp = row.company_xp,
            person_xp = row.person_xp
        )
        for row, department_name, department_id in result
    ]
    # else:
    #     count_statement = (
    #         select(func.count())
    #         .select_from(AvailableTask)
    #         .where(AvailableTask.company_id == current_user.company_id & AvailableTask.is_active == only_active)
    #     )
    #     count = session.exec(count_statement).one()
    #     statement = (
    #         select(AvailableTask)
    #         .where(AvailableTask.company_id == current_user.company_id & AvailableTask.is_active == only_active)
    #         .offset(skip)
    #         .limit(limit)
    #     )
    #     tasks = session.exec(statement).all()

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
def submit_task(taskSerivce: TaskServiceDep, 
                levelService: LevelsServiceDep,
                taskSubmitCommand: SubmitTaskCommand) -> Any:
    """
    Submit task.
    """
    tasks = taskSerivce.handle_command(taskSubmitCommand)
    print(tasks)
    if type(tasks) is TaskCompletedEvent:
        levelService.task_completed(tasks.task_id, tasks.assigned_to_id)
    return tasks

@router.patch("/approve-task", response_model=TaskEventDomain)
def approve_task(taskSerivce: TaskServiceDep, current_user: CurrentUser, taskCommand: Command) -> Any:
    """
    Approve task.
    """
    tasks = taskSerivce.handle_command(ApproveTaskCommand(taskCommand.aggregate_id, current_user.id))
    return tasks

@router.patch("/reject-task", response_model=TaskEventDomain)
def reject_task(taskSerivce: TaskServiceDep, taskCommand: RejectTaskCommand) -> Any:
    """
    Reject task.
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
