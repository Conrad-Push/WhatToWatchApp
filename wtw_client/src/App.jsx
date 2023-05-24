import React, { useEffect, useState } from "react";
import { Routes, Route } from 'react-router-dom';
import './App.css';
import axios from 'axios';
import Navbar from './components/Navbar';
import Home from './components/Home';
import Redis from './components/Redis';
import MongoDB from './components/MongoDB';
import PostgreSQL from './components/PostgreSQL';
import Details from "./components/Details";

function App() {
  // const [films, setFilms] = useState([]);

  //   useEffect(() => {
  //     axios
  //         .get(`http://localhost:8000/films/`)
  //         .then(function (response) {
  //             console.log(response.data[0]);
  //             setFilms(response.data)
  //         })
  //         .catch(function (error) {
  //             console.log(error);
  //         });
  // }, []);

  //   return (
  //     <div>
  //       <h1>Films list</h1>
  //       <ul>
  //         {films.map((film) => (
  //           <li key={film.film_id}>
  //             <h2>{film.title}</h2>
  //             <p>Year: {film.year}</p>
  //             <p>Rating: {film.rate.toFixed(1)}</p>
  //             <img src={film.img_url} alt={film.title} />
  //           </li>
  //         ))}
  //       </ul>
  //     </div>
  //   );

  return (
    <div className="App" >
    <Navbar/>
    <Routes>
      <Route exact path="/" element={<Home/>} />
      <Route exact path="/redis" element={<Redis/>} />
      <Route exact path="/mongodb" element={<MongoDB/>} />
      <Route exact path="/postgresql" element={<PostgreSQL/>} />
      <Route exact path="/details/:film_id" element={<Details/>} />
    </Routes>
    {/* <header className="App-header">
     Halo
    </header> */}
  </div>
  );

};

export default App;
