import React from "react";
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
} from "recharts";
import data from "../data.json";

export default function Statistics() {
  return (
    <div>
      <div className="box">
        <label>GET</label>
        <LineChart
          width={600}
          height={300}
          data={data}
          margin={{
            top: 5,
            right: 30,
            left: 20,
            bottom: 5,
          }}
        >
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis stroke="white" />
          <YAxis stroke="white" />
          <Tooltip />
          <Legend />
          <Line
            type="monotone"
            dataKey="PostgreSQL"
            stroke="#8884d8"
            activeDot={{ r: 8 }}
          />
          <Line type="monotone" dataKey="MongoDB" stroke="#82ca9d" />
          <Line type="monotone" dataKey="Redis" stroke="red" />
        </LineChart>
      </div>
      <div className="box">
        <label>POST</label>

        <LineChart
          width={600}
          height={300}
          data={data}
          margin={{
            top: 5,
            right: 30,
            left: 20,
            bottom: 5,
          }}
        >
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="name" stroke="white" />
          <YAxis stroke="white" />
          <Tooltip />
          <Legend />
          <Line
            type="monotone"
            dataKey="PostgreSQL"
            stroke="#8884d8"
            activeDot={{ r: 8 }}
          />
          <Line type="monotone" dataKey="MongoDB" stroke="#82ca9d" />
          <Line type="monotone" dataKey="Redis" stroke="red" />
        </LineChart>
      </div>
      <div className="box">
        <label>DELETE</label>
        <LineChart
          width={600}
          height={300}
          data={data}
          margin={{
            top: 5,
            right: 30,
            left: 20,
            bottom: 5,
          }}
        >
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="name" stroke="white" />
          <YAxis stroke="white" />
          <Tooltip />
          <Legend />
          <Line
            type="monotone"
            dataKey="PostgreSQL"
            stroke="#8884d8"
            activeDot={{ r: 8 }}
          />
          <Line type="monotone" dataKey="MongoDB" stroke="#82ca9d" />
          <Line type="monotone" dataKey="Redis" stroke="red" />
        </LineChart>
      </div>
    </div>
  );
}
