import React from 'react';
import { Grid, Paper, Typography } from '@material-ui/core';
import useStyles from "./styles";


const TweetsDashboard = ({data}) => {
    const classes = useStyles();

    return (
        <div className={classes.root}>
            <Grid container spacing={3}>
                <Grid item xs={12}>
                    <Paper className={classes.paper} elevation={4}>
                        <Typography variant="h5">Twitter sentiment data analysis - Dashboard</Typography>
                    </Paper>
                </Grid>
                <Grid item xs={12}>
                    <Paper className={classes.paper} elevation={4}>
                        <Typography variant="h6">Statistics</Typography>
                        <Typography>Total tweets: {data.statistics.total}</Typography>
                        <Paper className={classes.paper} elevation={4}>
                            <Typography variant="h6">Positive Tweets</Typography>
                            <Typography>Positive Tweets:{data.statistics.positive}</Typography>
                            <Typography>{data.positive_tweets}</Typography>
                        </Paper>
                        <Paper className={classes.paper} elevation={4}>
                            <Typography variant="h6">Negative Tweets</Typography>
                            <Typography>Negative Tweets:{data.statistics.negative}</Typography>
                            <Typography>{data.negative_tweets}</Typography>
                            <Typography>Order 3</Typography>
                        </Paper>
                    </Paper>
                </Grid>
                <Grid item xs={6}>
                    <Paper className={classes.paper} elevation={4}>
                        <Typography variant="h6">Realtime Graph</Typography>
                        <Typography>Order 1</Typography>
                        <Typography>Order 2</Typography>
                        <Typography>Order 3</Typography>
                    </Paper>
                </Grid>
                <Grid item xs={6}>
                    <Paper className={classes.paper} elevation={4}>
                        <Typography variant="h6">Realtime Graph</Typography>
                        <Typography>Order 1</Typography>
                        <Typography>Order 2</Typography>
                        <Typography>Order 3</Typography>
                    </Paper>
                </Grid>
            </Grid>
        </div>
    );
};


export default TweetsDashboard;