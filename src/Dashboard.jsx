// src/Dashboard.jsx

import React, { useEffect, useRef, useState } from 'react';
import { Chart, registerables } from 'chart.js';

// Register the components needed for Chart.js
Chart.register(...registerables);

const Dashboard = () => {
  const [data, setData] = useState(null);
  const chartRef = useRef(null);

  useEffect(() => {
    const fetchSimulationData = async () => {
      try {
        const response = await fetch('http://127.0.0.1:5500/simulation-data');
        if (!response.ok) {
          throw new Error('Network response was not ok ' + response.statusText);
        }
        const data = await response.json();
        setData(data);
      } catch (error) {
        console.error('Error fetching data:', error);
      }
    };

    fetchSimulationData();
    const intervalId = setInterval(fetchSimulationData, 5000);

    // Cleanup the interval on component unmount
    return () => clearInterval(intervalId);
  }, []);

  useEffect(() => {
    if (data && chartRef.current) {
      const finalVehicleCounts = data.final_vehicle_counts;

      // Destroy existing chart if any
      if (chartRef.current.chart) {
        chartRef.current.chart.destroy();
      }

      // Create a new chart
      const chart = new Chart(chartRef.current, {
        type: 'bar',
        data: {
          labels: Object.keys(finalVehicleCounts),
          datasets: [
            {
              label: 'Final Vehicle Counts',
              data: Object.values(finalVehicleCounts),
              backgroundColor: 'rgba(54, 162, 235, 0.2)',
              borderColor: 'rgba(54, 162, 235, 1)',
              borderWidth: 1,
            },
          ],
        },
        options: {
          scales: {
            y: {
              beginAtZero: true,
            },
          },
        },
      });

      // Store the chart instance for later destruction
      chartRef.current.chart = chart;
    }
  }, [data]);

  return (
    <div>
      <h1>Traffic Simulation Dashboard</h1>
      <canvas ref={chartRef} width="400" height="200"></canvas>
    </div>
  );
};

export default Dashboard;
