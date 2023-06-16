import React from "react";
import { Routes, Route } from "react-router-dom";
import "./App.css";
import Navbar from "./components/Navbar";
import Home from "./components/Home";

import CassandraFilms from "./components/Cassandra/CassandraFilms";
import CassandraFilmDetails from "./components/Cassandra/CassandraFilmDetails";
import CassandraManager from "./components/Cassandra/CassandraManager";

import MongoDBFilms from "./components/MongoDB/MongoDBFilms";
import MongoDBFilmDetails from "./components/MongoDB/MongoDBFilmDetails";
import MongoDBManager from "./components/MongoDB/MongoDBManager";

import PostgreSQLFilms from "./components/PostgreSQL/PostgreSQLFilms";
import PostgreSQLFilmDetails from "./components/PostgreSQL/PostgreSQLFilmDetails";
import PostgreSQLManager from "./components/PostgreSQL/PostgreSQLManager";

import Statistics from "./components/Statistics";

function App() {
  return (
    <div className="App">
      <Navbar />
      <Routes>
        <Route exact path="/" element={<Home />} />
        <Route exact path="/technologies" element={<Home />} />
        <Route exact path="/authors" element={<Home />} />

        <Route exact path="/cassandra/films" element={<CassandraFilms />} />
        <Route
          exact
          path="/cassandra/details/:film_id"
          element={<CassandraFilmDetails />}
        />
        <Route exact path="/cassandra/manager" element={<CassandraManager />} />

        <Route exact path="/mongodb/films" element={<MongoDBFilms />} />
        <Route
          exact
          path="/mongodb/details/:film_id"
          element={<MongoDBFilmDetails />}
        />
        <Route exact path="/mongodb/manager" element={<MongoDBManager />} />

        <Route exact path="/postgresql/films" element={<PostgreSQLFilms />} />
        <Route
          exact
          path="/postgresql/details/:film_id"
          element={<PostgreSQLFilmDetails />}
        />
        <Route
          exact
          path="/postgresql/manager"
          element={<PostgreSQLManager />}
        />

        <Route exact path="/statistics" element={<Statistics />} />
      </Routes>
    </div>
  );
}

export default App;
