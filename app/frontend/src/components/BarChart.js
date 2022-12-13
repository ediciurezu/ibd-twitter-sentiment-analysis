import React from "react";
import {
    MainContainer,
    Container,
    BarChartContainer,
    Number,
    BlackLine,
    MakeBar
} from "./styles";

const BarChart = ({data}) => {
    const positiveTweets = parseInt(data.statistics.positive.toString())
    const negativeTweets = parseInt(data.statistics.negative.toString())
    const total = parseInt(data.statistics.total.toString())
    const positivePercent = (positiveTweets * 100 / total).toFixed(2)
    const negativePercent = (negativeTweets * 100 / total).toFixed(2)

    return (
        <Container>
            <MainContainer>
                <BarChartContainer key={0}>
                    <Number color={"#e0064e"}>{positivePercent}%</Number>
                    <MakeBar height={positivePercent} colors={["#ff47ab", "#e0064e"]} />
                </BarChartContainer>

                <BarChartContainer key={1} style={{marginLeft: 24}}>
                    <Number color={"#1da890"}>{negativePercent}%</Number>
                    <MakeBar height={negativePercent} colors={["#add9c0", "#1da890"]} />
                </BarChartContainer>
            </MainContainer>
            <BlackLine />
        </Container>
    );
};

export default BarChart;
