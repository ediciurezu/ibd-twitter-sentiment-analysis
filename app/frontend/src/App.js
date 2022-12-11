import React, { useState } from 'react';
import {createTheme, ThemeProvider} from '@mui/material/styles';
import axios from 'axios';
import TweetsDashboard from "./components/Dashboard";
import {Button, Container, CssBaseline} from "@mui/material";
import RefreshIcon from '@mui/icons-material/Refresh';

const theme = createTheme({
    palette: {
        mode: 'light'
    }
});

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
      <ThemeProvider theme={theme}>
          <Container align={"center"} >
              {!data &&
                  <Container style={{marginTop: theme.spacing(50)}}>
                          <Button variant="contained" endIcon={<RefreshIcon />} onClick={fetchData}>
                              Refresh
                          </Button>
                  </Container>
              }

              {data && (
                  <TweetsDashboard data={data} />
              )}

              {data &&
                  <Container>
                      <Button variant="contained" endIcon={<RefreshIcon />} onClick={fetchData}>
                          Refresh
                      </Button>
                  </Container>
              }
          </Container>
          {/*<CssBaseline></CssBaseline>*/}
      </ThemeProvider>
    );
};

export default App;