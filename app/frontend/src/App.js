import React, { useState } from 'react';
import axios from 'axios';



const App = () => {
  // Define the endpoint for the JSON data
  const endpoint = 'http://127.0.0.1:5000/read/model.json';



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
        <button onClick={fetchData}>Fetch Data</button>

        {/* If the data is available, display it in a dashboard */}
        {data && (
            <Dashboard data={data} />
        )}
      </div>
  );
};



const Dashboard = ({ data }) => (
    <div>
      {/* Display the data from the JSON endpoint in the dashboard */}
      <h1>{data[0].id}</h1>
      <p>{data[0].text}</p>
    </div>
);



export default App;