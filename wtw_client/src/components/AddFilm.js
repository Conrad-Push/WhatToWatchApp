import axios from "axios";
import { useState } from "react";

function AddFilm() {
  const [title, setTitle] = useState("");
  const [year, setYear] = useState("");
  const [rate, setRate] = useState("");
  const [description, setDescription] = useState("");
  const [director_id, setDirectorID] = useState("");
  const [img_url, setImg] = useState(
    "https://yt3.googleusercontent.com/weD7WfgxB3sjFX7Yr4RBk3oAYKYLT4yjb9N3yK10VwF1Pmusidh7xqk1tAP23QpW1rur2Gst0s4=s900-c-k-c0x00ffffff-no-rj"
  );

  const handleSubmit = (e) => {
    e.preventDefault();

    axios
      .post("/films/", {
        title,
        year,
        rate,
        description,
        director_id,
        img_url,
      })
      .then(function (response) {
        console.log(response.data);
      })
      .catch(function (error) {
        console.log(error);
      });
  };

  return (
    <div className="add-film-container">
      <h1>Add film</h1>
      <div className="pad">
        <form className="add-film">
          <div className="form-group">
            <input
              type="text"
              className="form-control"
              placeholder="Title"
              value={title}
              onChange={(e) => setTitle(e.target.value)}
              required
            />
          </div>
          <div className="form-group">
            <input
              type="number"
              className="form-control"
              placeholder="Year"
              value={year}
              onChange={(e) => setYear(e.target.value)}
              required
            />
          </div>
          <div className="form-group">
            <input
              type="number"
              className="form-control"
              placeholder="Rating"
              value={rate}
              onChange={(e) => setRate(e.target.value)}
              required
            />
          </div>
          <div className="form-group">
            <input
              type="text"
              className="form-control"
              placeholder="Description"
              value={description}
              onChange={(e) => setDescription(e.target.value)}
              required
            />
          </div>
          <div className="form-group">
            <input
              type="text"
              className="form-control"
              placeholder="Director ID"
              value={director_id}
              onChange={(e) => setDirectorID(e.target.value)}
              required
            />
          </div>
          <button
            className="btn btn-warning btn-block my-2 my-sm-0"
            type="submit"
            onClick={handleSubmit}
          >
            Add
          </button>
        </form>
      </div>
    </div>
  );
}
export default AddFilm;
