import { useState } from "react"

import { Button, Flex, Icon, Select, VStack } from "@chakra-ui/react"
import { FaPlus } from "react-icons/fa"
import { AssignTaskCommand, AvailableTaskPublic, AvailableTasksPublic, TasksAssignTaskData, TasksService } from "../../client"
import { useMutation } from "@tanstack/react-query"
import useCustomToast from "../../hooks/useCustomToast"
import useAuth from "../../hooks/useAuth"

interface DropdownProps {
  taskList: AvailableTasksPublic | undefined
}
const showToast = useCustomToast()

const groupTasksByDepartment = (
  tasks: Array<AvailableTaskPublic>
): Record<string, Array<AvailableTaskPublic>> => {
  return tasks.reduce((acc, task) => {
    const departmentId = task.department_name || "Other"; // Default to "Other" if no department_id
    if (!acc[departmentId]) {
      acc[departmentId] = [];
    }
    acc[departmentId].push(task);
    return acc;
  }, {} as Record<string, Array<AvailableTaskPublic>>);
};

const Dropdown = ({ taskList }: DropdownProps) => {
  const { user: currentUser } = useAuth();
  const groupedTasks = taskList ? groupTasksByDepartment(taskList.data) : {};
  const [selectedTask, setSelectedTask] = useState<AvailableTaskPublic | null>(null);
  
  const assignTask = useMutation({
    mutationFn: (data: TasksAssignTaskData) =>
      TasksService.assignTask(data),
      onSuccess: () => {
        showToast("Success", "Task assigned successfully", "success");
      },
      onError: (error: any) => {
        showToast("Error", error.message, "error");
      },
    }
  );

  const handleAssignTask = () => {
    if (!selectedTask || !currentUser) {
      showToast("Issue arised" ,"Please select a task and ensure you are logged in.", "error");
      return;
    }

    const reqBody: AssignTaskCommand = {
      assigned_to_id: currentUser.id,
      task_id: selectedTask.id,
      title: selectedTask.title,
      description: selectedTask.description || "",
      requires_approval: selectedTask.requires_approval || false,
    }
    const taskData: TasksAssignTaskData = {
      requestBody: reqBody
      }

    assignTask.mutate(taskData);
  };
  
  return (
    <>
      <Flex py={8} gap={4}>
        {/* Grouped dropdowns */}
        <VStack align="start" spacing={4}>
          {Object.entries(groupedTasks).map(([department, tasks]) => (
            <Flex key={department} flexDir="column" w="100%">
              <label>{`Department ${department}`}</label>
              <Select placeholder="Select Task" fontSize="sm"
              onChange={(e) => {
                const taskId = e.target.value;
                const task = tasks.find((t) => t.id === taskId);
                setSelectedTask(task || null);
              }}>
                {tasks.map((task) => (
                  <option key={task.id} value={task.id}>
                    {task.title} - {department}
                  </option>
                ))}
              </Select>
            </Flex>
          ))}
        </VStack>
        {/* TODO: Complete search functionality */}
        {/* <InputGroup w={{ base: '100%', md: 'auto' }}>
                    <InputLeftElement pointerEvents='none'>
                        <Icon as={FaSearch} color='ui.dim' />
                    </InputLeftElement>
                    <Input type='text' placeholder='Search' fontSize={{ base: 'sm', md: 'inherit' }} borderRadius='8px' />
                </InputGroup> */}
        <Button
          variant="primary"
          gap={1}
          fontSize={{ base: "sm", md: "inherit" }}
          onClick={handleAssignTask}
        >
          <Icon as={FaPlus} /> Assign Task
        </Button>
      </Flex>
    </>
  )
}

export default Dropdown
