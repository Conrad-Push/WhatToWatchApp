import React, { useState, useEffect } from "react";
import { useParams, useNavigate } from "react-router-dom";
import axios from "axios";
import { ToastContainer, toast } from "react-toastify";
import "react-toastify/dist/ReactToastify.css";

function MongoDBFilmDetails() {
  const dbName = "mongodb";
  const [film, setFilm] = useState(null);
  const [loading, setLoading] = useState(true);
  const [editedDirector, setEditedDirector] = useState("");
  const [editedDescription, setEditedDescription] = useState("");
  const [errorMessage, setErrorMessage] = useState("");
  const { film_id } = useParams();
  const navigate = useNavigate();

  useEffect(() => {
    const abortController = new AbortController();

    const fetchFilmDetails = async () => {
      try {
        const response = await axios.get(`/${dbName}/films/${film_id}`, {
          signal: abortController.signal,
        });

        if (response.status !== 200) {
          throw new Error("Network response was not ok");
        }

        const data = response.data;

        const {
          film_id: filmID,
          title: filmTitle,
          execution_time: execTime,
        } = response.data;

        if (!abortController.signal.aborted) {
          setFilm(data);

          if (filmID && filmTitle && execTime) {
            let infoText = `Details for '${filmTitle}' displayed in ${execTime} second(s)`;

            toast.info(infoText, {
              position: toast.POSITION.BOTTOM_RIGHT,
            });
          }

          setLoading(false);
        }
      } catch (error) {
        console.log(error);
      }
    };

    fetchFilmDetails();

    return () => {
      abortController.abort();
    };
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
    setLoading(true);

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
          `/${dbName}/films/${film_id}`,
          updatedDetails
        );

        if (response.status === 200) {
          const { execution_time: execTime } = response.data;

          setFilm((prevFilm) => ({
            ...prevFilm,
            details: {
              ...prevFilm.details,
              ...updatedDetails,
            },
          }));

          if (execTime) {
            let infoText = `The film (${title}) details have been modified in ${execTime} second(s)`;

            toast.warning(infoText, {
              position: toast.POSITION.BOTTOM_RIGHT,
            });
          }
        }

        setLoading(false);
      } catch (error) {
        console.log(error);

        let errorText = "Error while editing the film's details";
        toast.error(errorText, {
          position: toast.POSITION.BOTTOM_RIGHT,
        });

        setLoading(false);
      }

      setEditedDirector("");
      setEditedDescription("");
    } else {
      setErrorMessage("Please fill at least one field");
    }
  };

  const handleGoBack = () => {
    navigate(`/${dbName}/films`);
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
      <ToastContainer />
    </div>
  );
}

export default MongoDBFilmDetails;
