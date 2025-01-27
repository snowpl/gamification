import { useEffect, useState } from "react";
import { Box, Circle, Flex, Text } from "@chakra-ui/react";

const MIN = 0;

export default function XPProgressBar({ value = 0, currentMissingValue = 100, currentLevel = 0,  onComplete = () => {} }) {
  const [percent, setPercent] = useState(value);
  const maxValue = currentMissingValue+value;
  
  useEffect(() => {
    setPercent(Math.min(Math.max(value, MIN), maxValue));

    if (value >= maxValue) {
      onComplete();
    }
  }, [value, maxValue, onComplete]);

  return(
      <Flex
        align="center"
        justify="space-between"
        position="relative"
        width="100%"
        maxWidth="600px"
        mx="auto"
      >
        {/* Progress Bar */}
        <Box
          position="relative"
          flex="1"
          height="24px"
          backgroundColor="white"
          borderRadius="15px 0 0 15px"
          overflow="hidden"
          borderColor="gray.400"
          borderWidth="1px"
        >
          {/* XP Text */}
          <Text
            position="absolute"
            width="100%"
            display="flex"
            justifyContent="center"
            alignItems="center"
            zIndex="99"
            fontWeight="bold"
            // color={percent > 50 ? "gray.500" : "black"}
            color="black"
          >
            XP:{value}/{maxValue}
          </Text>
  
          {/* Progress Fill */}
          <Box
             backgroundColor="#00c251"
             height="100%"
             textAlign="center"
             transform={`scaleX(${percent / maxValue})`}
             transformOrigin="left"
             transition="transform 0.3s ease"
          />
        </Box>
  
        {/* Next Level Circle */}
        <Circle
          size="50px"
          bg="white"
          borderWidth="4px"
          borderColor="gray.400"
          fontWeight="bold"
          color="gray.500"
          marginLeft="-6px"
          zIndex="100"
        >
          {currentLevel + 1}
        </Circle>
      </Flex>
    );
}
