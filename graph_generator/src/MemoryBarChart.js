import React, { PureComponent } from "react";
import "./App.css";
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
} from "recharts";

export default class MemoryBarChart extends PureComponent {
  static jsfiddleUrl = "https://jsfiddle.net/alidingling/90v76x08/";

  render() {
    const { title, data, heavyFillColor, lightFillColor } = this.props;
    return (
      <div>
        <h3 className="barTitle">{title}</h3>
        <BarChart
          width={600}
          height={300}
          data={data}
          barSize={70}
          margin={{
            top: 20,
            right: 100,
            left: 50,
            bottom: 5,
          }}
        >
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis
            label={{ value: "Memory type", position: "right", offset: 0 }}
            dataKey="name"
          />
          <YAxis label={{ value: "kB", position: "left", offset: 0 }} />
          <Tooltip />
          <Legend margin={{ left: "500" }} />
          {/*
        <Bar dataKey="used" stackId="a" fill="#199c52" />
        <Bar dataKey="free" stackId="a" fill="#82ca9d" />
         */}
          <Bar dataKey="used" stackId="a" fill={heavyFillColor} />
          <Bar dataKey="free" stackId="a" fill={lightFillColor} />
        </BarChart>
      </div>
    );
  }
}
