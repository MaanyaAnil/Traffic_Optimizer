import React, { useState, useEffect } from 'react';
import axios from 'axios';

const Dashboard = () => {
  const [status, setStatus] = useState(null);
  const [error, setError] = useState(null);

  // Fetch the current status from the backend
  const fetchStatus = async () => {
    try {
      const response = await axios.get('http://localhost:5000/status');
      setStatus(response.data);
    } catch (err) {
      setError("Error fetching status. Please try again.");
    }
  };

  // Fetch status when the component mounts
  useEffect(() => {
    fetchStatus();
    const interval = setInterval(fetchStatus, 5000); // Refresh every 5 seconds
    return () => clearInterval(interval); // Clean up the interval on component unmount
  }, []);

  return (
    <div className="dashboard">
      <h1>Traffic Flow Optimizer Dashboard</h1>
      
      {error && <div className="error">{error}</div>}
      
      {status ? (
        <div className="status">
          <h2>Current System Status</h2>
          <p><strong>Emergency Mode:</strong> {status.emergency_mode ? 'Active' : 'Inactive'}</p>
          <p><strong>Emergency Direction:</strong> {status.emergency_direction || 'None'}</p>

          <h3>Optimized Signal Timings:</h3>
          <ul>
            <li><strong>North:</strong> {status.optimized_timings?.north} seconds</li>
            <li><strong>South:</strong> {status.optimized_timings?.south} seconds</li>
            <li><strong>East:</strong> {status.optimized_timings?.east} seconds</li>
            <li><strong>West:</strong> {status.optimized_timings?.west} seconds</li>
          </ul>
        </div>
      ) : (
        <p>Loading status...</p>
      )}
    </div>
  );
};

export default Dashboard;
