import {makeStyles} from '@mui/styles';

export default makeStyles( theme  => ({
    paper: {
        padding: theme.spacing(2),
        textAlign: 'center',
        color: theme.palette.text.secondary,
        border: "1px black",
        marginTop: 8,
        marginBottom: 8
    },
    root: {
        padding: theme.spacing(2),
        margin: theme.spacing(2),
    },
}));