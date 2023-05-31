import { useNavigate } from "react-router-dom";
import deleteFilm from "../functions/deleteFilm";

function Card(props) {
  const navigate = useNavigate();
  const films = props.films;

  return (
    <div>
      <h1>Films list</h1>
      {films.length > 0 ? (
        <ul>
          {films.map((film) => (
            <div key={film.film_id}>
              <div className="box-padding">
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
                </div>
                <div>
                  <button
                    className="btn btn-danger"
                    onClick={() => {
                      deleteFilm({ film_id: film.film_id });
                    }}
                  >
                    Remove
                  </button>
                </div>
              </div>
            </div>
          ))}
        </ul>
      ) : (
        <div className="no-films">No films available</div>
      )}
    </div>
  );
}
export default Card;
