import {BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend} from "recharts";
import React from "react";
import ResponsiveContainer from "recharts/lib/component/ResponsiveContainer";


const data = [
  {name: 'CO2 emission reduction', "CO2 emission reduction": 4000},
  {name: 'Stormwater reduction', "Stormwater reduction": 1398},
  {name: 'Energy savings', "Energy savings": 2290},
];

export default class StackedBarChart extends React.Component {
  render () {
    return (
      <ResponsiveContainer width="99%" height={250}>
        <BarChart data={data} margin={{top: 20, right: 30, left: 20, bottom: 5}}>
          <CartesianGrid strokeDasharray="3 3"/>
          <XAxis dataKey="name"/>
          <YAxis/>
          <Tooltip/>
          <Bar dataKey="CO2 emission reduction" stackId="a" fill="#8884d8" />
          <Bar dataKey="Stormwater reduction" stackId="a" fill="#82ca9d" />
          <Bar dataKey="Energy savings" stackId="a" fill="#28acd9" />
        </BarChart>
      </ResponsiveContainer>
    );
  }
}