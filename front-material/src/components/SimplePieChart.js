import { PieChart, Pie, Cell } from 'recharts';
import React from "react";

const data = [{name: 'Group A', value: 400}, {name: 'Group B', value: 300},
  {name: 'Group C', value: 300}];
const COLORS = ['#0088FE', '#00C49F', '#FFBB28'];

const TEXT = ["Logistics", "Product Loss", "Maintenance"];

const RADIAN = Math.PI / 180;
const renderCustomizedLabel = ({ cx, cy, midAngle, innerRadius, outerRadius, percent, index }) => {
  const radius = innerRadius + (outerRadius - innerRadius) * 0.5;
  const x  = cx + radius * Math.cos(-midAngle * RADIAN);
  const y = cy  + radius * Math.sin(-midAngle * RADIAN);

  return (
    <text style={{fontWeight: "bold", fontSize: "16px"}} x={x - 40} y={y} fill="white" dominantBaseline="central">
      {TEXT[index]}
    </text>
  );
};

export default class SimplePieChart extends React.Component {
  render() {
    return (
      <PieChart width={600} height={300} onMouseEnter={this.onPieEnter}>
        <Pie
          data={data}
          cx={300}
          labelLine={false}
          label={renderCustomizedLabel}
          outerRadius={140}
          fill="#8884d8"
        >
          {
            data.map((entry, index) => <Cell fill={COLORS[index % COLORS.length]}/>)
          }
        </Pie>
      </PieChart>
    )
  }
}
