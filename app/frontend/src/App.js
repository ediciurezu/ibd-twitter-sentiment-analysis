import React, { useState } from 'react';
import axios from 'axios';
import TweetsDashboard from "./dashboard";

const App = () => {
  // Define the endpoint for the JSON data
  const endpoint = 'http://127.0.0.1:5000/statistics';

  // Use React state to store the data from the endpoint
  const [data, setData] = useState(null);



  // Define a function to fetch the data from the endpoint
  const fetchData = () => {
    axios.get(endpoint)
        .then(response => setData(response.data))
        .catch(error => console.error(error));
  };

  return (
      <div>
        {/* Display a button to fetch the data */}
        <button onClick={fetchData}>Refresh</button>

        {/* If the data is available, display it in a dashboard */}
        {data && (
            <TweetsDashboard data={data} />
        )}
      </div>
  );
};

export default App;