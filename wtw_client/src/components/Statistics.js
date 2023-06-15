import React, { useState, useEffect } from "react";
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  BarChart,
  Bar,
} from "recharts";
import axios from "axios";

export default function Statistics() {
  const [timesPostgreSQL, setTimesPostgreSQL] = useState();
  const [timesMongo, setTimesMongo] = useState();
  const [timesCassandra, setTimesCassandra] = useState();
  const [meanPostgreSQL, setMeanPostgreSQL] = useState();
  const [meanMongo, setMeanMongo] = useState();
  const [meanCassandra, setMeanCassandra] = useState();
  const [requestType, setRequestType] = useState("GET");

  useEffect(() => {
    let urlPostgres = `/postgresql/times/?filter_by=request_type&filter_value=${requestType}`;
    let urlMongo = `/mongodb/times/?filter_by=request_type&filter_value=${requestType}`;
    let urlCassandra = `/cassandra/times/?filter_by=request_type&filter_value=${requestType}`;

    const fetchTimesPostgres = async () => {
      await axios
        .get(urlPostgres)
        .then(function (response) {
          setTimesPostgreSQL(response.data.times);
          setMeanPostgreSQL(response.data.times_mean);
        })
        .catch(function (error) {
          console.log(error);
        });
    };

    const fetchTimesMongo = async () => {
      await axios
        .get(urlMongo)
        .then(function (response) {
          setTimesMongo(response.data.times);
          setMeanMongo(response.data.times_mean);
        })
        .catch(function (error) {
          console.log(error);
        });
    };

    const fetchTimesCassandra = async () => {
      await axios
        .get(urlCassandra)
        .then(function (response) {
          setTimesCassandra(response.data.times);
          setMeanCassandra(response.data.times_mean);
        })
        .catch(function (error) {
          console.log(error);
        });
    };

    fetchTimesPostgres();

    fetchTimesMongo();

    fetchTimesCassandra();
  }, [requestType]);

  const handleRequest = (event) => {
    setRequestType(event.target.value);
  };

  const data = [
    {
      postgres: `${meanPostgreSQL}`,
      mongo: `${meanMongo}`,
      cassandra: `${meanCassandra}`,
    },
  ];

  return (
    <div>
      <div className="sort-dropdown">
        <label htmlFor="sort"></label>
        <select id="sort" value={requestType} onChange={handleRequest}>
          <option value="GET">GET</option>
          <option value="GET_filter">GET FILTER</option>
          <option value="GET_details">GET DETAILS</option>
          <option value="GET_sort">GET SORT</option>
          <option value="GET_combined">GET SORT AND FILTER</option>
          <option value="POST">POST</option>
          <option value="DELETE">DELETE</option>
          <option value="PATCH">PATCH</option>
        </select>
      </div>
      <div className="box">
        <div>
          <LineChart
            width={450}
            height={300}
            data={timesPostgreSQL}
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
              dataKey="time_value"
              name="PostgreSQL"
              stroke="#8884d8"
              activeDot={{ r: 8 }}
            />
          </LineChart>
          Mean time: {meanPostgreSQL}
        </div>
        <div>
          <LineChart
            width={450}
            height={300}
            data={timesMongo}
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
              dataKey="time_value"
              name="MongoDB"
              stroke="#e09620"
              activeDot={{ r: 8 }}
            />
          </LineChart>
          Mean time: {meanMongo}
        </div>
        <div>
          <LineChart
            width={450}
            height={300}
            data={timesCassandra}
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
              dataKey="time_value"
              name="Cassandra"
              stroke="red"
              activeDot={{ r: 8 }}
            />
          </LineChart>
          Mean time: {meanCassandra}
        </div>
      </div>
      <div className="box">
        <BarChart
          width={500}
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
          <XAxis dataKey="Mean" stroke="white" />
          <YAxis stroke="white" />
          <Tooltip />
          <Legend />
          <Bar dataKey="postgres" name="PostgreSQL" fill="#8884d8" />
          <Bar dataKey="mongo" name="MongoDB" fill="#e09620" />
          <Bar dataKey="cassandra" name="Cassandra" fill="red" />
        </BarChart>
      </div>
    </div>
  );
}
