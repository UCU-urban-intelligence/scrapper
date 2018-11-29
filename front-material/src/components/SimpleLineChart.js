import React from 'react';
import ResponsiveContainer from 'recharts/lib/component/ResponsiveContainer';
import LineChart from 'recharts/lib/chart/LineChart';
import Line from 'recharts/lib/cartesian/Line';
import XAxis from 'recharts/lib/cartesian/XAxis';
import YAxis from 'recharts/lib/cartesian/YAxis';
import CartesianGrid from 'recharts/lib/cartesian/CartesianGrid';
import Tooltip from 'recharts/lib/component/Tooltip';
import Legend from 'recharts/lib/component/Legend';

const data = [
  { name: 'Mon', Tomato: 2200, Carrot: 3400, Basil: 4000 },
  { name: 'Tue', Tomato: 1280, Carrot: 2398, Basil: 5000 },
  { name: 'Wed', Tomato: 5000, Carrot: 4300, Basil: 2499 },
  { name: 'Thu', Tomato: 4780, Carrot: 2908, Basil: 4566 },
  { name: 'Fri', Tomato: 5890, Carrot: 4800, Basil: 3500 },
  { name: 'Sat', Tomato: 4390, Carrot: 3800, Basil: 4000 },
  { name: 'Sun', Tomato: 4490, Carrot: 4300, Basil: 4000 },
];

function SimpleLineChart() {
  return (
    // 99% per https://github.com/recharts/recharts/issues/172
    <ResponsiveContainer width="99%" height={250}>
      <LineChart data={data}>
        <XAxis dataKey="name" />
        <YAxis />
        <CartesianGrid vertical={false} strokeDasharray="3 3" />
        <Tooltip />
        <Legend />
        <Line type="monotone" dataKey="Tomato" stroke="#82ca9d" />
        <Line type="monotone" dataKey="Carrot" stroke="#8884d8" activeDot={{ r: 8 }} />
        <Line type="monotone" dataKey="Basil" stroke="#83c9bc" />
      </LineChart>
    </ResponsiveContainer>
  );
}

export default SimpleLineChart;
