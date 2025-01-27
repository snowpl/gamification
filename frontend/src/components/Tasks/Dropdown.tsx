import { Button, Flex, Icon, Select, VStack } from "@chakra-ui/react"
import { FaPlus } from "react-icons/fa"
import { AssignTaskCommand, AvailableTaskPublic, AvailableTasksPublic, SubmitTaskCommand, TasksAssignTaskData, TasksService, TasksSubmitTaskData } from "../../client"
import { useState } from "react";
import useAuth from "../../hooks/useAuth";
import { useMutation } from "@tanstack/react-query"
// import useCustomToast from "../../hooks/useCustomToast"
import { useQueryClient } from "@tanstack/react-query"


interface DropdownProps {
  taskList: AvailableTasksPublic | undefined
}
//const showToast = useCustomToast()

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
  const queryClient = useQueryClient()
  const { user: currentUser } = useAuth();
  const groupedTasks = taskList ? groupTasksByDepartment(taskList.data) : {};
  const [selectedDepartment, setSelectedDepartment] = useState<string | null>(null);
  const [selectedTask, setSelectedTask] = useState<AvailableTaskPublic | null>(null);
  let assignedTaskId: string = "";

  const assignTask = useMutation({
    mutationFn: async (data: TasksAssignTaskData) => {
      assignedTaskId = await TasksService.assignTask(data)
    },
      onSuccess: () => {
        console.log("Task assigned successfully");
        queryClient.invalidateQueries({ queryKey: ["currentUser"] })
        //showToast("Success", "Task assigned successfully", "success");
      },
      onError: (error: any) => {
        console.log("Error assigning task", error);
        //showToast("Error", error.message, "error");
      },
    }
  );

  const submitTask = useMutation({
    mutationFn: async (data: TasksSubmitTaskData) =>
      await TasksService.submitTask(data),
      onSuccess: () => {
        console.log("Task completed successfully");
        queryClient.invalidateQueries({ queryKey: ["currentUser"] })
        //showToast("Success", "Task completed successfully", "success");
      },
      onError: (error: any) => {
        console.log("Error completing task", error);
        //showToast("Error", error.message, "error");
      },
    }
  );

  const handleAssignTask = async () => {
    if (!selectedTask || !currentUser) {
      //showToast("Issue arised" ,"Please select a task and ensure you are logged in.", "error");
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

    await assignTask.mutateAsync(taskData);
  };

  const handleAssignAndCompleteTask = async () => {
    await handleAssignTask();
    const reqBody: SubmitTaskCommand = {
      aggregate_id: assignedTaskId
    }
    const taskData: TasksSubmitTaskData = {
      requestBody: reqBody
    }
    await submitTask.mutateAsync(taskData);
  };
  
  return (
    <>
    <Flex py={8} gap={4} flexDir="column">
        <VStack align="start" spacing={4}>
          {/* Department Dropdown */}
          <Flex flexDir="column" w="25%">
            <label>Select Departments</label>
            <Select
              placeholder="Select Department"
              fontSize="sm"
              onChange={(e) => {
                const department = e.target.value;
                setSelectedDepartment(department);
                setSelectedTask(null); // Reset the selected task when department changes
              }}
            >
              {Object.keys(groupedTasks).map((department) => (
                <option key={department} value={department}>
                  {department}
                </option>
              ))}
            </Select>
          </Flex>

          {/* Task Dropdown */}
          {selectedDepartment && (
            <Flex flexDir="column" w="25%">
              <label>Select Task</label>
              <Select
                placeholder="Select Task"
                fontSize="sm"
                onChange={(e) => {
                  const taskId = e.target.value;
                  const task = groupedTasks[selectedDepartment]?.find((t) => t.id === taskId);
                  setSelectedTask(task || null);
                }}
              >
                {groupedTasks[selectedDepartment]?.map((task) => (
                  <option key={task.id} value={task.id}>
                    {task.title}
                  </option>
                ))}
              </Select>
            </Flex>
          )}
        </VStack>
      {/* <Flex py={8} gap={4}>
        <VStack align="start" spacing={4}>
          {Object.entries(groupedTasks).map(([department, tasks]) => (
            <Flex key={department} flexDir="column" w="100%">
              <label>{`${department} Tasks`}</label>
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
        </VStack> */}

        <Button
          variant="primary"
          gap={1}
          fontSize={{ base: "sm", md: "inherit" }}
          onClick={handleAssignTask}
        >
          <Icon as={FaPlus} /> Assign
        </Button>
        <Button
          variant="primary"
          gap={1}
          fontSize={{ base: "sm", md: "inherit" }}
          onClick={handleAssignAndCompleteTask}
        >
          <Icon as={FaPlus} /> Assign And Complete
        </Button>
      </Flex>
    </>
  )
}

export default Dropdown
