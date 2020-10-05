import React, { PureComponent } from "react";
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
} from "recharts";
import "./stacked.css";

export default class LineBarChart extends PureComponent {
  static jsfiddleUrl = "https://jsfiddle.net/alidingling/c1rLyqj1/";

  render() {
    const { title, data, stroke1, stroke2, stroke3 } = this.props;
    return (
      <div>
        <h3 className="barTitle">{title}</h3>

        <LineChart
          width={550}
          height={400}
          data={data}
          margin={{
            top: 50,
            right: 0,
            left: 80,
            bottom: 25,
          }}
        >
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis
            label={{
              value: "Network width",
              position: "bottom",
              offset: 0,
            }}
            dataKey="name"
          />
          <YAxis
            label={{
              value: "Flash Memory (KB)",
              position: "top",
              offset: 20,
            }}
          />
          <Tooltip />
          <Line type="monotone" dataKey="tflite" stroke="#8884d8" />
          <Line type="monotone" dataKey="flash" stroke="#32a852" />
        </LineChart>
      </div>
    );
  }
}
