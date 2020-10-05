import React, { PureComponent } from "react";
import {
  AreaChart,
  Area,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
} from "recharts";
import "./stacked.css";

export default class MyStackedBarChart extends PureComponent {
  static jsfiddleUrl = "https://jsfiddle.net/alidingling/c1rLyqj1/";

  render() {
    const { title, data, stroke1, stroke2, stroke3 } = this.props;
    return (
      <div className="stackedContainer">
        <div>
          <h3 className="barTitle">{title}</h3>

          <AreaChart
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
                value: "Sense Cycle Memory (%)",
                position: "bottom",
                offset: 0,
              }}
              dataKey="name"
            />
            <YAxis
              label={{
                value: "Neural Netowork Memory (%)",
                position: "top",
                offset: 20,
              }}
            />
            <Tooltip />
            <Area
              type="monotone"
              dataKey="sense"
              stackId="1"
              stroke="#8884d8"
              fill="#8884d8"
              label="Hello"
            />
            <Area
              type="monotone"
              dataKey="nn"
              stackId="2"
              stroke="#82ca9d"
              fill="#82ca9d"
            />
          </AreaChart>
        </div>
        <div className="legends">
          <div className="innerCont">
            <ul className="colorBoxes">
              <li style={{ backgroundColor: "#b7b6e4" }}>&nbsp;</li>
              <li style={{ backgroundColor: "#bedec6" }}>&nbsp;</li>
            </ul>
            <ul className="labels">
              <li>Neural Network</li>
              <li>Sense Cycle</li>
            </ul>
          </div>
        </div>
      </div>
    );
  }
}
