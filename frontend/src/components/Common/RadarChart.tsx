import React from "react";
import { Radar } from "react-chartjs-2";
import {
  Chart as ChartJS,
  RadialLinearScale,
  PointElement,
  LineElement,
  Filler,
  Tooltip,
  Legend,
} from "chart.js";
import { UsersService } from "../../client";
import { useQuery } from "@tanstack/react-query";

// Register Chart.js components
ChartJS.register(RadialLinearScale, PointElement, LineElement, Filler, Tooltip, Legend);

function getSkills() {
    return {
      queryFn: () =>
        UsersService.readUserMe1(),
      queryKey: ["skills"],
    }
  }

const RadarChart: React.FC = () => {
    const {
        data: skills,
      } = useQuery({
        ...getSkills(),
      })

  const labels = skills?.skills.map((skill) => skill.name);
  const dataPoints = skills?.skills.map((skill) => skill.level);
  const data = {
    labels: labels,
    datasets: [
      {
        label: "Skill Levels",
        data: dataPoints,
        fill: true,
        backgroundColor: "rgba(255,99,132,0.2)",
        borderColor: "rgba(255,99,132,1)",
        pointBorderColor: "#fff",
        pointBackgroundColor: "rgba(255,99,132,1)",
      },
    ],
  };

  const options = {
    responsive: true,
    plugins: {
      legend: {
        display: false, // Hide the legend
      },
    },
    scales: {
      r: {
        ticks: {
          font: {
            size: 18,
          },
          max: 100,
        },
        grid: {
          lineWidth: 2,
          color: "lightgreen",
        },
        pointLabels: {
          font: {
            size: 18,
            weight: "bold" as "bold",
          },
        },
      },
    },
  };

  return (
    <div style={{ width: "100%", height: "400px" }}>
      <Radar data={data} options={options} />
    </div>
  );
};

export default RadarChart;
