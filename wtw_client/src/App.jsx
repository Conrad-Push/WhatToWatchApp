import React, { useEffect, useState } from "react";

const App = () => {
  const [films, setFilms] = useState([]);

  const getFilmsList = async () => {
    const requestOptions = {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
      },
    };

    const response = await fetch("/films/", requestOptions);
    const data = await response.json();

    if (!response.ok) {
      console.log("Something went wrong...")
    } else {
      setFilms(data);
    }
  };

  useEffect(() => {
    getFilmsList();
  }, [])
  return (
    <div>
      <h1>Films list</h1>
      <ul>
        {films.map((film) => (
          <li key={film.film_id}>
            <h2>{film.title}</h2>
            <p>Year: {film.year}</p>
            <p>Rating: {film.rate.toFixed(1)}</p>
            <img src={film.img_url} alt={film.title} />
          </li>
        ))}
      </ul>
    </div>
  );
};

export default App;
