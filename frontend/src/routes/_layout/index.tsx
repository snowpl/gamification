import { Box, Container, Text } from "@chakra-ui/react"
import { createFileRoute } from "@tanstack/react-router"

import useAuth from "../../hooks/useAuth"
import RadarChart from "../../components/Common/RadarChart"

export const Route = createFileRoute("/_layout/")({
  component: Dashboard,
})

function Dashboard() {
  const { user: currentUser } = useAuth()

  return (
    <>
      <Container maxW="full">
        <Box pt={12} m={4}>
          <Text fontSize="2xl">
            Hi, {currentUser?.full_name || currentUser?.email} 👋🏼
          </Text>
          <Text>Welcome back, nice to see you again!</Text>
          <Text>Your current level is {currentUser?.level} and you miss experience {currentUser?.missing_xp} to next level.</Text>
          <Text fontSize="xl">
            Your skills:
          </Text>
          <RadarChart/>
        </Box>
      </Container>
    </>
  )
}
