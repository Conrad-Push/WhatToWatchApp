import { useNavigate } from "react-router-dom";
import axios from "axios";

function Card(props) {
  const navigate = useNavigate();

  const handleRemove = async (filmId) => {
    try {
      const response = await axios.delete(`/postgresql/films/${filmId}`);
      if (response.status === 200) {
        props.setFilms((prevFilms) =>
          prevFilms.filter((film) => film.film_id !== filmId)
        );
      }
    } catch (error) {
      console.log(error);
    }
  };

  return (
    <div>
      <h1>Films list</h1>
      {props.films.length > 0 ? (
        <ul>
          {props.films.map((film) => (
            <div key={film.film_id}>
              <div className="box">
                <div className="list">
                  <div
                    onClick={() => {
                      navigate(`/details/${film.film_id}`);
                    }}
                  >
                    <div className="card-content">
                      <img src={film.img_url} alt={film.title} />
                      <div>
                        <div className="card-title">
                          {film.title} ({film.year})
                        </div>
                        <div className="film-info">
                          <p>Rating: {film.rate.toFixed(1)}</p>
                        </div>
                      </div>
                    </div>
                  </div>
                  <button
                    className="remove-button"
                    onClick={() => handleRemove(film.film_id)}
                  >
                    Remove
                  </button>
                </div>
              </div>
            </div>
          ))}
        </ul>
      ) : (
        <div className="no-films">No films founded</div>
      )}
    </div>
  );
}
export default Card;
