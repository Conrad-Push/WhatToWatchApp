import React, { useState, useEffect } from "react";
import { useParams } from "react-router-dom";
import axios from "axios";

function EditTitle() {
  const [title, setTitle] = useState("");
  const { film_id } = useParams();
  console.log(film_id);

  const handleSubmit = (e) => {
    e.preventDefault();

    axios
      .patch(`/films/${film_id}`, {
        title,
      })
      .then(function (response) {
        console.log(response.data);
      })
      .catch(function (error) {
        console.log(error);
      });
  };

  return (
    <div>
      <div className="pad">
        <form className="edits">
          <div className="form-group">
            <input
              type="text"
              className="form-control"
              placeholder="Edit title"
              value={title}
              onChange={(e) => setTitle(e.target.value)}
              required
            />
          </div>
          <button
            className="btn btn-warning btn-block my-2 my-sm-0"
            type="submit"
            onClick={handleSubmit}
          >
            Edit
          </button>
        </form>
      </div>
    </div>
  );
}
export default EditTitle;
