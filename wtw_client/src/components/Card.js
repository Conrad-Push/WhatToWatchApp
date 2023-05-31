import { useNavigate } from "react-router-dom";
import axios from "axios";

function Card(props) {
  const navigate = useNavigate();
  const films = props.films;
  const setFilms = props.setFilms;
  const handleRemove = props.handleRemove;

  return (
    <div>
      <h1>Films list</h1>
      {films.length > 0 ? (
        <ul>
          {films.map((film) => (
            <div key={film.film_id}>
              <div className="box">
                <div className="list">
                  <div
                    onClick={() => {
                      navigate(`/details/${film.film_id}`);
                    }}
                  >
                    <div className="card-looks">
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
