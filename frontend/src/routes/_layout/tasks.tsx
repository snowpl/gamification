import {
    Container,
    Heading,
    SkeletonText,
    Table,
    TableContainer,
    Tbody,
    Td,
    Th,
    Thead,
    Tr,
  } from "@chakra-ui/react"
  import { useQuery, useQueryClient } from "@tanstack/react-query"
  import { createFileRoute, useNavigate } from "@tanstack/react-router"
  import { useEffect } from "react"
  import { z } from "zod"
  
  import { TasksService } from "../../client"
  import Dropdown from "../../components/Tasks/Dropdown"
  import { PaginationFooter } from "../../components/Common/PaginationFooter.tsx"
  import useAuth from "../../hooks/useAuth"

  const tasksSearchSchema = z.object({
    page: z.number().catch(1),
  })
  
  export const Route = createFileRoute("/_layout/tasks")({
    component: Tasks,
    validateSearch: (search) => tasksSearchSchema.parse(search),
  })
  
  const PER_PAGE = 8
  
  function getTasksQueryOptions({ page }: { page: number }) {
  const { user: currentUser } = useAuth()
    return {
      queryFn: () =>
        TasksService.getEmployeeTasks({ id: currentUser!.id }),
      queryKey: ["tasks", { page }],
    }
  }

  function getAvailableTasks() {
      return {
        queryFn: () =>
          TasksService.readTasks({ onlyActive: true }),
        queryKey: ["availableTasks"],
      }
    }
  
  function TasksTable() {
    const queryClient = useQueryClient()
    const { page } = Route.useSearch()
    const navigate = useNavigate({ from: Route.fullPath })
    const setPage = (page: number) =>
      navigate({ search: (prev: {[key: string]: string}) => ({ ...prev, page }) })
  
    const {
      data: tasks,
      isPending,
      isPlaceholderData,
    } = useQuery({
      ...getTasksQueryOptions({ page }),
      placeholderData: (prevData) => prevData,
    })
  
    const hasNextPage = !isPlaceholderData && tasks?.length === PER_PAGE
    const hasPreviousPage = page > 1
  
    useEffect(() => {
      if (hasNextPage) {
        queryClient.prefetchQuery(getTasksQueryOptions({ page: page + 1 }))
      }
    }, [page, queryClient, hasNextPage])
  
    return (
      <>
        <TableContainer>
          <Table size={{ base: "sm", md: "md" }}>
            <Thead>
              <Tr>
                <Th>Title</Th>
                <Th>Description</Th>
                <Th>Status</Th>
                <Th>Requires Approval</Th>
                <Th>Actions</Th>
              </Tr>
            </Thead>
            {isPending ? (
              <Tbody>
                <Tr>
                  {new Array(4).fill(null).map((_, index) => (
                    <Td key={index}>
                      <SkeletonText noOfLines={1} paddingBlock="16px" />
                    </Td>
                  ))}
                </Tr>
              </Tbody>
            ) : (
              <Tbody>
                {tasks?.map((task) => (
                  <Tr key={task.id} opacity={isPlaceholderData ? 0.5 : 1}>
                    <Td>{task.title}</Td>
                    <Td
                      color={!task.description ? "ui.dim" : "inherit"}
                      isTruncated
                      maxWidth="150px"
                    >
                      {task.description || "N/A"}
                    </Td>
                    <Td isTruncated maxWidth="150px">
                      {task.status}
                    </Td>
                    <Td isTruncated maxWidth="150px">
                      {task.requires_approval}
                    </Td>
                    <Td>
                      {/* <ActionsMenu type={"Task"} value={task} /> */}
                    </Td>
                  </Tr>
                ))}
              </Tbody>
            )}
          </Table>
        </TableContainer>
        <PaginationFooter
          page={page}
          onChangePage={setPage}
          hasNextPage={hasNextPage}
          hasPreviousPage={hasPreviousPage}
        />
      </>
    )
  }
  
  function Tasks() {
    const {
        data: avialbleTasks,
      } = useQuery({
        ...getAvailableTasks(),
      })

    return (
      <Container maxW="full">
        <Heading size="lg" textAlign={{ base: "center", md: "left" }} pt={12}>
          Task Management
        </Heading>
  
        <Dropdown taskList={avialbleTasks} />
        <TasksTable />
      </Container>
    )
  }
  