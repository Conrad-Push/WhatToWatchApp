import React from "react";
import { Routes, Route } from "react-router-dom";
import "./App.css";
import Navbar from "./components/Navbar";
import Home from "./components/Home";
import Redis from "./components/Redis";
import MongoDB from "./components/MongoDB";
import PostgreSQL from "./components/PostgreSQL";
import Details from "./components/Details";

function App() {
  return (
    <div className="App">
      <Navbar />
      <Routes>
        <Route exact path="/" element={<Home />} />
        <Route exact path="/redis" element={<Redis />} />
        <Route exact path="/mongodb" element={<MongoDB />} />
        <Route exact path="/postgresql" element={<PostgreSQL />} />
        <Route exact path="/details/:film_id" element={<Details />} />
      </Routes>
    </div>
  );
}

export default App;
