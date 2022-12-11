import React from 'react';
import { Grid, Paper, Typography } from '@material-ui/core';
import useStyles from "./styles";
import BarChart from "./BarChart";
import {Box, List, ListItem, ListItemText} from "@mui/material";


const TweetsDashboard = ({data}) => {
    const classes = useStyles();

    return (
        <div className={classes.root}>
            <Grid container spacing={3} justifyContent={"center"}>
                <Grid item xs={12}>
                    <Paper className={classes.paper} elevation={4}>
                        <Typography variant="h5">Twitter sentiment data analysis - Dashboard</Typography>
                    </Paper>
                </Grid>

                <Grid>
                    <Grid container item xs={24} justifyContent={"center"} >
                        <Paper className={classes.paper} elevation={4}>
                            <Typography>Total tweets: {data.statistics.total}</Typography>
                        </Paper>
                    </Grid>

                    <Grid container spacing={24}>
                        <Paper className={classes.paper} elevation={4}>
                            <Typography>Positive Tweets: {data.statistics.positive}</Typography>
                            <Paper className={classes.tweet_list} elevation={4}>
                                <List>
                                    {
                                        data.positive_tweets.map((item, index) => (
                                            <ListItem key={index}>
                                                <ListItemText primary={item}></ListItemText>
                                            </ListItem>
                                        ))
                                    }
                                </List>
                            </Paper>
                        </Paper>

                        <Paper className={classes.paper} elevation={4}>
                            <Typography>Negative Tweets: {data.statistics.negative}</Typography>
                            <Paper className={classes.tweet_list}>
                                <List>
                                    {
                                        data.negative_tweets.map((item, index) => (
                                            <ListItem key={index}>
                                                <ListItemText primary={item}></ListItemText>
                                            </ListItem>
                                        ))
                                    }
                                </List>
                            </Paper>
                        </Paper>
                    </Grid>

                    <Grid item xs={12}>
                        <Box display="flex" style={{alignContent: "center"}}>
                            <BarChart data={data}></BarChart>
                        </Box>
                    </Grid>
                </Grid>
            </Grid>
        </div>
    );
};


export default TweetsDashboard;