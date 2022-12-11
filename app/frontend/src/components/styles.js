import {makeStyles} from '@mui/styles';
import styled, { css } from "styled-components";

export default makeStyles( theme  => ({
    paper: {
        padding: theme.spacing(2),
        textAlign: 'center',
        color: theme.palette.text.secondary,
        border: "1px black",
        marginTop: 8,
        marginBottom: 8,
        marginLeft: 16
    },

    root: {
        padding: theme.spacing(2),
        margin: theme.spacing(2),
    },

    tweet_list: {
        maxHeight: 400,
        overflow: 'auto',
        width: 400,
        marginLeft: 8,
        marginRight: 8,
        marginBottom: 8,
        marginTop: 8
    }
}));

export const Container = styled.div`
    margin: 0px auto;
    max-width: 500px;
    height: 500px;
    display: flex;
    flex-direction: column;
    justify-content: flex-end;
`;

export const MainContainer = styled.div`
    display: flex;
    justify-content: space-between;
    width: 100%;
    height: 100%;
`;

export const BarChartContainer = styled.div`
    display: flex;
    flex-direction: column;
    justify-content: flex-end;
    align-items: center;
`;

export const Chart = css`
    margin-top: 10px;
    width: 56px;
    &:hover {
      opacity: 0.8;
    }
    @media (max-width: 420px) {
      width: 34px;
    }
`;

export const Number = styled.span`
    font-size: 1.5rem;
    text-align: center;
    color: ${(props) => props.color};
`;

export const MakeBar = styled.div`
    height: ${(props) => props.height}%;
    background-image: linear-gradient(
    to bottom,
    ${(props) => props.colors[0]},
    ${(props) => props.colors[1]}
    );
    ${Chart};
`;

export const BlackLine = styled.div`
    width: 100%;
    height: 5px;
    background-color: black;
`;
