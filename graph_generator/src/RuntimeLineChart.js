import React, { PureComponent } from "react";
import "./App.css";
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
} from "recharts";

export default class RuntimeLineChart extends PureComponent {
  static jsfiddleUrl = "https://jsfiddle.net/alidingling/xqjtetw0/";

  render() {
    const { title, data, stroke1, stroke2, stroke3 } = this.props;
    return (
      <div>
        <h3 className="barTitle">{title}</h3>

        <LineChart
          width={600}
          height={300}
          data={data}
          margin={{
            top: 30,
            right: 100,
            left: 50,
            bottom: 5,
          }}
        >
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis
            label={{ value: "Iteration", position: "right" }}
            dataKey="name"
          />
          <YAxis label={{ value: "Runtime (ms)", position: "top" }} />
          <Tooltip />
          <Legend />
          <Line
            type="monotone"
            dataKey="ble"
            dot={false}
            stroke={stroke1}
            strokeWidth={2}
            // activeDot={{ r: 8 }}
          />
          <Line
            type="monotone"
            dataKey="scan"
            dot={false}
            stroke={stroke2}
            strokeWidth={2}
            // stroke="#82ca9d"
          />
          <Line
            type="monotone"
            dataKey="total"
            dot={false}
            stroke={stroke3}
            strokeWidth={2}
            // stroke="#82ca9d"
          />
        </LineChart>
      </div>
    );
  }
}
