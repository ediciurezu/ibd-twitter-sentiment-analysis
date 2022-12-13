import React, { useState, useEffect } from 'react';
import {createTheme, ThemeProvider} from '@mui/material/styles';
import TweetsDashboard from "./components/Dashboard";
import socketio from 'socket.io-client';

const theme = createTheme({
    palette: {
        mode: 'light'
    }
});

const App = () => {
  // Use React state to store the data from the endpoint
  const [data, setData] = useState(null);

  // Initialize a websocket connection to the Flask backend
  const socket = socketio('http://127.0.0.1:5001/');

  socket.on('UPDATE', (updates) => {
    // Update the frontend with the new data from the updates
    setData(updates);
  });

  // Send a request to the Flask backend to get updates every second
  useEffect(() => {
    // Send an HTTP request to the webhook URL every second
    const interval = setInterval(() => {
      socket.emit('GET_UPDATES');
    }, 1000);

    return () => clearInterval(interval);
  });

    return (
      <ThemeProvider theme={theme}>
          <div>
            {/* If the data is available, display it in a dashboard */}
            {data && (
                <TweetsDashboard data={data} />
            )}
          </div>
      </ThemeProvider>
    );
};

export default App;