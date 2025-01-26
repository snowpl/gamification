# class LevelsService:
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