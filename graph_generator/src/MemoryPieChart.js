import React, { PureComponent } from "react";
import "./App.css";
import { PieChart, Pie, Sector, Cell } from "recharts";

const RADIAN = Math.PI / 180;
const renderCustomizedLabel = ({
  cx,
  cy,
  midAngle,
  innerRadius,
  outerRadius,
  percent,
  index
}) => {
  const radius = innerRadius + (outerRadius - innerRadius) * 0.5;
  const x = cx + radius * Math.cos(-midAngle * RADIAN);
  const y = cy + radius * Math.sin(-midAngle * RADIAN);

  return (
    <text
      x={x}
      y={y}
      fill="white"
      textAnchor={x > cx ? "start" : "end"}
      dominantBaseline="central"
    >
      {`${(percent * 100).toFixed(0)}%`}
    </text>
  );
};

export default class MemoryPieChart extends PureComponent {
  static jsfiddleUrl = "https://jsfiddle.net/alidingling/90v76x08/";

  render() {
    const { title, data, colors } = this.props;
    console.log("received data", data);
    return (
      <div>
        <h3 className="barTitle">{title}</h3>
        <div className="pieCharts">
          <PieChart width={500} height={400}>
            <Pie
              data={data}
              cx={250}
              cy={200}
              labelLine={false}
              label={e => e.name}
              outerRadius={140}
              dataKey="value"
              nameKey="name"
            >
              {data.map((entry, index) => (
                <Cell
                  key={`cell-${index}`}
                  fill={colors[index % colors.length]}
                />
              ))}
            </Pie>
            <Pie
              data={data}
              cx={250}
              cy={200}
              labelLine={false}
              label={renderCustomizedLabel}
              outerRadius={140}
              fill="#8884d8"
              dataKey="value"
            >
              {data.map((entry, index) => (
                <Cell
                  key={`cell-${index}`}
                  fill={colors[index % colors.length]}
                />
              ))}
            </Pie>
          </PieChart>
        </div>
      </div>
    );
  }
}
