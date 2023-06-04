import { useState } from "react";
import axios from "axios";

function AddFilmPanel(props) {
  const [newFilm, setNewFilm] = useState({
    title: "",
    description: "",
    year: "",
    rate: "",
    img_url: "",
    director_id: "",
  });
  const [errorMessage, setErrorMessage] = useState("");

  const handleAddFilm = async (e) => {
    e.preventDefault();

    if (newFilm.title && newFilm.year && newFilm.rate && newFilm.director_id) {
      setErrorMessage("");

      try {
        // Provide default values for description and img_url if they are not filled
        const filmData = {
          ...newFilm,
          description: newFilm.description || "Default description",
          img_url:
            newFilm.img_url ||
            "https://icdn.2cda.pl/obr/oryginalne/171cdd9bc97c7c886071fa43d55709e9.jpg",
        };

        const response = await axios.post("/films", filmData);

        if (response.status === 200) {
          const addedFilm = response.data;

          props.setFilms((prevFilms) => [...prevFilms, addedFilm]);
        }
      } catch (error) {
        console.log(error);
        setErrorMessage("Error while adding a film");
      }

      setNewFilm({
        title: "",
        description: "",
        year: "",
        rate: "",
        img_url: "",
        director_id: "",
      });
    } else {
      setErrorMessage("Please fill in all required fields");
    }
  };

  const handleYearChange = (e) => {
    const value = e.target.value;
    const yearRegex = /^\d{0,4}$/;

    if (yearRegex.test(value)) {
      setNewFilm({ ...newFilm, year: parseInt(value) });
    }
  };

  return (
    <div>
      <h1>Add Film</h1>
      <div className="box">
        <div className="add-film-card">
          <form className="card-content">
            <input
              type="text"
              placeholder="Enter film title..."
              value={newFilm.title}
              onChange={(e) =>
                setNewFilm({ ...newFilm, title: e.target.value })
              }
              required
            />
            <input
              type="number"
              placeholder="Enter film year..."
              value={newFilm.year}
              onChange={handleYearChange}
              required
            />
            <input
              type="number"
              step="0.1"
              placeholder="Enter film rate..."
              value={newFilm.rate}
              onChange={(e) =>
                setNewFilm({ ...newFilm, rate: parseFloat(e.target.value) })
              }
              required
            />
            <input
              type="number"
              placeholder="Enter director ID..."
              value={newFilm.director_id}
              onChange={(e) =>
                setNewFilm({
                  ...newFilm,
                  director_id: parseInt(e.target.value),
                })
              }
              required
            />
            <input
              type="text"
              placeholder="Enter film description... (optional)"
              value={newFilm.description}
              onChange={(e) =>
                setNewFilm({ ...newFilm, description: e.target.value })
              }
            />
            <input
              type="text"
              placeholder="Enter film image URL... (optional)"
              value={newFilm.img_url}
              onChange={(e) =>
                setNewFilm({ ...newFilm, img_url: e.target.value })
              }
            />
            {errorMessage && <p style={{ color: "red" }}>{errorMessage}</p>}
            <button className="add-button" onClick={handleAddFilm}>
              Add Film
            </button>
          </form>
        </div>
      </div>
    </div>
  );
}
export default AddFilmPanel;
