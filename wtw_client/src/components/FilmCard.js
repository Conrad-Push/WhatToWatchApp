import { useNavigate } from "react-router-dom";
import axios from "axios";

function FilmCard(props) {
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

  const handlePrevPage = () => {
    if (props.page > 1) {
      props.setPage((prevPage) => prevPage - 1);
    }
  };

  const handleNextPage = () => {
    if (props.page < props.totalPages) {
      props.setPage((prevPage) => prevPage + 1);
    }
  };

  return (
    <div className="films-list-frame">
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
      <div className="back-button-container">
        {props.page > 1 && (
          <button className="page-button" onClick={handlePrevPage}>
            Previous Page
          </button>
        )}
        {props.page < props.totalPages && (
          <button className="page-button" onClick={handleNextPage}>
            Next Page
          </button>
        )}
      </div>
    </div>
  );
}
export default FilmCard;
