import { useState } from "react";
import axios from "axios";
import { ToastContainer, toast } from "react-toastify";
import "react-toastify/dist/ReactToastify.css";

function AddShortFilmPanel(props) {
  const [newFilm, setNewFilm] = useState({
    title: "",
    year: "",
    rate: "",
    img_url: "",
    details_id: "",
  });
  const [errorMessage, setErrorMessage] = useState("");

  const handleAddFilm = async (e) => {
    e.preventDefault();
    props.setLoading(true);

    if (newFilm.title && newFilm.year && newFilm.rate && newFilm.details_id) {
      setErrorMessage("");

      try {
        const filmData = {
          ...newFilm,
          img_url:
            newFilm.img_url ||
            "https://icdn.2cda.pl/obr/oryginalne/171cdd9bc97c7c886071fa43d55709e9.jpg",
        };

        const response = await axios.post(`/${props.dbName}/films`, filmData);

        if (response.status === 201) {
          const addedFilm = response.data;
          const { execution_time: execTime, ...filmData } = addedFilm;

          props.setFilms((prevFilms) => [...prevFilms, filmData]);

          if (filmData && execTime) {
            let infoText = `The new film (${filmData.title}) has been added in ${execTime} second(s)`;

            toast.success(infoText, {
              position: toast.POSITION.BOTTOM_RIGHT,
            });
          }
        }

        props.setLoading(false);
      } catch (error) {
        console.log(error);

        let errorText = "Error while adding a film";
        toast.error(errorText, {
          position: toast.POSITION.BOTTOM_RIGHT,
        });

        props.setLoading(false);
      }

      setNewFilm({
        title: "",
        year: "",
        rate: "",
        img_url: "",
        details_id: "",
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
              placeholder="Enter details ID..."
              value={newFilm.details_id}
              onChange={(e) =>
                setNewFilm({
                  ...newFilm,
                  details_id: parseInt(e.target.value),
                })
              }
              required
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
      <ToastContainer />
    </div>
  );
}
export default AddShortFilmPanel;
