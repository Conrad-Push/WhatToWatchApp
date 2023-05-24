import React, { useState, useEffect } from "react";
import { useParams } from "react-router-dom";
import axios from "axios";

function Details() {
  const [film, setFilm] = useState(null);
  const [loading, setLoading] = useState(true);
  const { film_id } = useParams();

  useEffect(() => {
    const fetchFilmDetails = async () => {
      try {
        const response = await axios.get(`/films/${film_id}`);
        if (response.status !== 200) {
          throw new Error("Network response was not ok");
        }
        const data = response.data;
        setFilm(data);
        setLoading(false);
      } catch (error) {
        console.log(error);
      }
    };

    fetchFilmDetails();
  }, [film_id]);

  if (loading) {
    return <div className="loading">Loading...</div>;
  }

  const { title, img_url, rate, director } = film;

  return (
    <div className="App-header">
      <div className="box">
        <div className="film-details">
          <div className="photo-frame">
            <img className="photo-details" src={img_url} alt={title} />
          </div>
          <div>
            <div id="film-title">{title}</div>
            <div className="film-description">
              <div>
                <div>
                  <b>Rating:</b> {rate}
                </div>
                <p>
                  <b>Director:</b> {director.name}
                </p>
                <div className="description">
                  <b>Description:</b> Lorem ipsum dolor sit amet, consectetur
                  adipiscing elit. Vestibulum euismod risus turpis, at lobortis
                  turpis rhoncus non. Proin enim nisl, vehicula et purus nec,
                  tempor blandit dui. Donec eget augue enim. Quisque semper nisi
                  gravida tempor sagittis. Phasellus convallis ut ligula a
                  elementum. Etiam nec neque a nisl rutrum blandit. Proin vel
                  felis eget ligula lobortis lacinia. Nullam interdum ipsum a
                  leo dignissim elementum. Cras scelerisque neque eget imperdiet
                  tincidunt. Aliquam maximus eu odio sed pharetra.
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default Details;
