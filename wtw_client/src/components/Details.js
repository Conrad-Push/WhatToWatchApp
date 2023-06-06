import React, { useState, useEffect } from "react";
import { useParams, useNavigate } from "react-router-dom";
import axios from "axios";

function Details() {
  const [film, setFilm] = useState(null);
  const [loading, setLoading] = useState(true);
  const [editedDirector, setEditedDirector] = useState("");
  const [editedDescription, setEditedDescription] = useState("");
  const [errorMessage, setErrorMessage] = useState("");
  const { film_id } = useParams();
  const navigate = useNavigate();

  useEffect(() => {
    const fetchFilmDetails = async () => {
      try {
        const response = await axios.get(`/postgresql/films/${film_id}`);
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

  const { title, year, rate, img_url, details } = film;

  const handleDirectorChange = (event) => {
    setEditedDirector(event.target.value);
  };

  const handleDescriptionChange = (event) => {
    setEditedDescription(event.target.value);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (editedDirector || editedDescription) {
      setErrorMessage("");

      try {
        const updatedDetails = {};

        if (editedDirector !== "") {
          updatedDetails.director = editedDirector;
        }

        if (editedDescription !== "") {
          updatedDetails.description = editedDescription;
        }

        const response = await axios.patch(
          `/postgresql/details/${details.details_id}`,
          updatedDetails
        );

        if (response.status === 200) {
          setFilm((prevFilm) => ({
            ...prevFilm,
            details: {
              ...prevFilm.details,
              ...updatedDetails,
            },
          }));
        }
      } catch (error) {
        console.log(error);
      }

      setEditedDirector("");
      setEditedDescription("");
    } else {
      setErrorMessage("Please fill at least one field");
    }
  };

  const handleGoBack = () => {
    navigate("/postgresql");
  };

  return (
    <div className="App-header">
      <div className="box">
        <div className="film-details">
          <div className="photo-frame">
            <img className="photo-details" src={img_url} alt={title} />
          </div>
          <div className="details-frame">
            <div id="film-title">{title}</div>
            <div className="details-content">
              <div>
                <div>
                  <b>Rating:</b> {rate.toFixed(1)}
                </div>
                <div>
                  <b>Year of production:</b> {year}
                </div>
                <div>
                  <b>Director:</b> {details.director}
                </div>
                <div className="description">
                  <b>Description:</b> {details.description}
                </div>
              </div>
            </div>
          </div>
        </div>
        <div className="add-film-card">
          <form className="card-content">
            <input
              type="text"
              placeholder="Modify director..."
              value={editedDirector}
              onChange={handleDirectorChange}
            />
            <input
              type="text"
              placeholder="Modify description..."
              value={editedDescription}
              onChange={handleDescriptionChange}
            />
            {errorMessage && <p style={{ color: "red" }}>{errorMessage}</p>}
            <button className="edit-button" onClick={handleSubmit}>
              Save Changes
            </button>
          </form>
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
