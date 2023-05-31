import React, { useState, useEffect } from "react";
import { useParams, useNavigate } from "react-router-dom";
import axios from "axios";
import EditTitle from "./EditTitle";
import EditImg from "./EditImg";

function Details() {
  const [film, setFilm] = useState(null);
  const [loading, setLoading] = useState(true);
  const { film_id } = useParams();
  const navigate = useNavigate();

  useEffect(() => {
    const fetchFilmDetails = async () => {
      try {
        const response = await axios.get(`/films/${film_id}`);
        if (response.status !== 200) {
          throw new Error("Network response was not ok");
        }
        setFilm(response.data);
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

  const { title, year, description, img_url, rate, director } = film;

  const handleGoBack = () => {
    navigate("/postgresql");
  };

  return (
    <div className="App-header">
      <div className="edits">
        <div className="box">
          <div className="film-details">
            <div className="photo-frame">
              <img className="photo-details" src={img_url} alt={title} />
            </div>
            <div>
              <div id="film-title">
                {title} ({year})
              </div>
              <div className="film-description">
                <div>
                  <b>Rating:</b> {rate}
                </div>
                <p>
                  <b>Director:</b> {director.name}
                </p>
                <div className="description">
                  <b>Description:</b> {description}
                </div>
              </div>
            </div>
          </div>
        </div>
        <div>
          <div className="edit-box">
            <EditTitle />
          </div>
          <div className="edit-box">
            <EditImg />
          </div>
        </div>
      </div>
      <div className="back-button-container">
        <button className="back-button" onClick={handleGoBack}>
          Back
        </button>
      </div>
    </div>
  );
}

export default Details;
