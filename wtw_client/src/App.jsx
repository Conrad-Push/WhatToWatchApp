import React from "react";
import { Routes, Route } from "react-router-dom";
import "./App.css";
import Navbar from "./components/Navbar";
import Home from "./components/Home";
import RedisFilms from "./components/RedisFilms";
import MongoDBFilms from "./components/MongoDBFilms";
import PostgreSQLFilms from "./components/PostgreSQLFilms";
import Details from "./components/Details";

function App() {
  return (
    <div className="App">
      <Navbar />
      <Routes>
        <Route exact path="/" element={<Home />} />
        <Route exact path="/technologies" element={<Home />} />
        <Route exact path="/authors" element={<Home />} />
        <Route exact path="/redis/films" element={<RedisFilms />} />
        <Route exact path="/redis/manager" element={<Home />} />
        <Route exact path="/mongodb/films" element={<MongoDBFilms />} />
        <Route exact path="/mongodb/manager" element={<Home />} />
        <Route exact path="/postgresql/films" element={<PostgreSQLFilms />} />
        <Route exact path="/postgresql/manager" element={<Home />} />
        <Route exact path="/details/:film_id" element={<Details />} />
      </Routes>
    </div>
  );
}

export default App;
