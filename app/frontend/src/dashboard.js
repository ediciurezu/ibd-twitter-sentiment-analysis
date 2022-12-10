import React from 'react';
import { makeStyles } from '@material-ui/core/styles';
import { Grid, Paper, Typography } from '@material-ui/core';

const useStyles = makeStyles(theme => ({
    root: {
        padding: theme.spacing(2),
        margin: theme.spacing(2),
    },
    paper: {
        padding: theme.spacing(2),
        textAlign: 'center',
        color: theme.palette.text.secondary,
    },
}));


const TweetsDashboard = ({data}) => {
    const classes = useStyles();

    return (
        <div className={classes.root}>
            <Grid container spacing={3}>
                <Grid item xs={12}>
                    <Paper className={classes.paper}>
                        <Typography variant="h5">Twitter sentiment data analysis - Dashboard</Typography>
                    </Paper>
                </Grid>
                <Grid item xs={6}>
                    <Paper className={classes.paper}>
                        <Typography variant="h6">Statistics</Typography>
                        <Typography>Total tweets: {data.statistics.total}</Typography>
                        <Typography>Positive Tweets:{data.statistics.positive}</Typography>
                        <Typography>Negative Tweets:{data.statistics.negative}</Typography>
                        <Typography>Positive:{data.positive_tweets}</Typography>
                        <Typography>Negative:{data.negative_tweets}</Typography>
                    </Paper>
                </Grid>
                <Grid item xs={6}>
                    <Paper className={classes.paper}>
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