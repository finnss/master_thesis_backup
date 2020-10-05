import React, { PureComponent } from "react";
import "./App.css";
import {
  baseData,
  cycleData,
  adjustedCycleData,
  nnData,
  adjustedNnData,
  totalData,
  freeData,
} from "./memoryData";
import MemoryBarChart from "./MemoryBarChart";
import MemoryPieChart from "./MemoryPieChart";
import { cycleRuntimeData, integratedCycleRuntimeData } from "./runtimeData";
import RuntimeLineChart from "./RuntimeLineChart";
import StackedBarChart from "./StackedBarChart";
import { stackedData } from "./stackedData";
import { lineData } from "./lineData";
import LineBarChart from "./LineBarChart";

export default class Main extends PureComponent {
  static jsfiddleUrl = "https://jsfiddle.net/alidingling/90v76x08/";

  state = {
    toDisplay: "line",
  };

  formatDataForPie = (dataIndex) => {
    const dataNames = ["Overhead", "Cyclic", "Neural network", "Free"];
    return [baseData, adjustedCycleData, adjustedNnData, freeData].map(
      (dataPoint, i) => ({
        name: dataNames[i],
        value: dataPoint[dataIndex].used,
      })
    );
  };

  renderMemoryCharts = () => {
    console.log("rendering memory");
    return (
      <div className="chartsContainer">
        <div className="barCharts">
          <h2 style={{ marginLeft: "30px" }}>Individual data points</h2>
          <MemoryBarChart
            title={"Common memory overhead"}
            data={baseData}
            heavyFillColor="#fcba03"
            lightFillColor="#ffe18f"
          />
          <MemoryBarChart
            title={"Cyclic sensor memory footprint"}
            data={cycleData}
            heavyFillColor="#199c52"
            lightFillColor="#82ca9d"
          />
          <MemoryBarChart
            title={"Neural Network memory consumption"}
            data={nnData}
            heavyFillColor="#65bfe0"
            lightFillColor="#b3e8fc"
          />
        </div>
        <div className="totalChart">
          <h2 style={{ marginLeft: "30px" }}>Total</h2>
          <MemoryBarChart
            title={"Total memory usage at compile time"}
            data={totalData}
            heavyFillColor="#35374a"
            lightFillColor="#adafc4"
          />
          <MemoryPieChart
            title={"Flash memory distribution"}
            data={this.formatDataForPie(0)}
            colors={["#0088FE", "#00C49F", "#FFBB28", "#FF8042"]}
          />
          <MemoryPieChart
            title={"RAM distribution"}
            data={this.formatDataForPie(1)}
            colors={["#0088FE", "#00C49F", "#FFBB28", "#FF8042"]}
          />
        </div>
      </div>
    );
  };

  renderRuntimeCharts = () => {
    console.log("rendering runtime");
    return (
      <div className="chartsContainer">
        <div className="barCharts">
          <h2 style={{ marginLeft: "30px" }}>Sense Cycle Runtime</h2>
          <RuntimeLineChart
            title={"Sense Cycle Runtime"}
            data={cycleRuntimeData}
            stroke1="#8884d8"
            stroke2="#82ca9d"
            stroke3="#eb8634"
          />
          <RuntimeLineChart
            title={"Sense Cycle Runtime (Integrated)"}
            data={integratedCycleRuntimeData}
            stroke1="#8884d8"
            stroke2="#82ca9d"
            stroke3="#eb8634"
          />
        </div>
      </div>
    );
  };

  renderStackedCharts = () => {
    console.log("rendering stack");
    return (
      <div className="chartsContainer">
        <div className="barCharts">
          <h2 style={{ marginLeft: "30px" }}>Stacked Bar charts</h2>
          <StackedBarChart
            title={"Memory Consumption Ratio"}
            data={stackedData}
          />
        </div>
      </div>
    );
  };

  renderLineCharts = () => {
    console.log("rendering line");
    return (
      <div className="chartsContainer">
        <div className="barCharts">
          <h2 style={{ marginLeft: "30px" }}>Line charts</h2>
          <LineBarChart title={"Tflite / Flash Memory"} data={lineData} />
        </div>
      </div>
    );
  };

  render() {
    const options = [
      {
        key: "mem",
        label: "Memory charts",
        renderFun: this.renderMemoryCharts,
      },
      {
        key: "run",
        label: "Runtime charts",
        renderFun: this.renderRuntimeCharts,
      },
      {
        key: "stack",
        label: "Stacked Bar charts",
        renderFun: this.renderStackedCharts,
      },
      {
        key: "line",
        label: "Line charts",
        renderFun: this.renderLineCharts,
      },
    ];

    return (
      <div>
        <h1 style={{ marginLeft: "30px" }}>
          IoT Power Consumption Master Thesis 2020 Graphs
        </h1>
        <div className="dropdown">
          Display:
          <select
            onChange={(e) => this.setState({ toDisplay: e.target.value })}
          >
            {options.map((option) => (
              <option
                selected={this.state.toDisplay === option.key}
                value={option.key}
              >
                {option.label}
              </option>
            ))}
          </select>
        </div>
        <div>
          {options.find((o) => o.key === this.state.toDisplay).renderFun()}
        </div>
      </div>
    );
  }
}
