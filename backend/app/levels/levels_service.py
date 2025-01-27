from uuid import UUID
from app.levels.levels_repository import LevelsRepository
from app.levels.levels_requirements import level_xp_requirements, skill_xp_requirements
from app.api.users.skills_models import EmployeeSkillCreate, GlobalSkillCreate

class LevelsService:
    def __init__(self, repository: LevelsRepository):
        self.repository = repository

    def task_completed(self, task_id: UUID, employee_id: UUID):
        task = self.repository.get_task(task_id)
        employee_level = self.repository.get_level(employee_id)
        print(task.skill_id)
        print(employee_id)
        employee_skill = self.repository.get_employee_skill(task.skill_id, employee_id)
        print(employee_skill)
        #Grant XP to employee
        employee_level.xp += int(task.person_xp * employee_level.xp_multiplier)
        xp_missing = level_xp_requirements[employee_level.level+1] - employee_level.xp

        if xp_missing <= 0:
            employee_level.level += 1
            employee_level.xp = 0
            #Check employee multiplier (if employee level is higher then company level)

        if not employee_skill:
            skill = self.repository.get_global_skill(task.skill_id)
            # Create the skill for the user first time completing task in a domain
            print('got global skill')
            print(skill)
            skill_create = EmployeeSkillCreate(
                skill_id = skill.id,
                user_id=employee_id,
                xp=0,
                level=0
            )
            employee_skill = self.repository.create_employee_skill(skill_create)

        # Grant XP to the skill
        employee_skill.xp += task.skill_xp

        # Check if the skill levels up
        skill_xp_missing = skill_xp_requirements[employee_skill.level + 1] - employee_skill.xp
        if skill_xp_missing <= 0:
            employee_skill.level += 1
            employee_skill.xp = 0

        # Save changes to the database
        self.repository.save(employee_level)
        self.repository.saveSkill(employee_skill)
        print('level service finished')
#     def __init__(self, repository: TaskRepository):
#         self.repository = repository

#     def get_employee_task(self, id: UUID) -> List[EmployeeTask]:
#         return self.repository.get_user_tasks(id)

#     def get_aggregates(self, id: UUID) -> List[TaskEvent]:
#         return self.repository.get_events(id)

#     def create_task(self, command: AssignTaskCommand) -> UUID:
#         task, event = EmployeeTaskDomain.create(command)
#         self.repository.save(EmployeeTask(**asdict(task)))
#         self.repository.save_event(event)
#         return task.id

#     def handle_command(self, command: Command) -> TaskEvent:
#         # Retrieve the task by ID
#         task = self.repository.get_by_id(command.aggregate_id)
        
#         # If the task doesn't exist, raise an error
#         if task is None:
#             raise ValueError(f"Task {command.aggregate_id} not found")

#         # Generate the appropriate event using the command handler
#         event = handle_command(command, task)
#         # If no event is generated (e.g., task already completed), do nothing
#         if event is None:
#             return

#         # Apply the event to update the task's state
#         updated_task = apply_event(event, task)

#         # Save the updated task and the event to the repository
#         self.repository.save(updated_task)
#         self.repository.save_event(event)
#         return event