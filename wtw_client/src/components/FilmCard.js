import { useNavigate } from "react-router-dom";
import axios from "axios";
import { ToastContainer, toast } from "react-toastify";
import "react-toastify/dist/ReactToastify.css";

function FilmCard(props) {
  const navigate = useNavigate();

  const handleRemove = async (filmId) => {
    props.setLoading(true);

    try {
      const response = await axios.delete(`/postgresql/films/${filmId}`);

      if (response.status === 200) {
        const removedFilm = response.data;
        const { execution_time: execTime, ...filmData } = removedFilm;

        props.setFilms((prevFilms) =>
          prevFilms.filter((film) => film.film_id !== filmId)
        );

        if (filmData && execTime) {
          let infoText = `The film (${filmData.title}) has been removed in ${execTime} second(s)`;

          toast.warning(infoText, {
            position: toast.POSITION.BOTTOM_RIGHT,
          });
        }
      }

      props.setLoading(false);
    } catch (error) {
      console.log(error);

      let errorText = "Error while removing a film";
      toast.error(errorText, {
        position: toast.POSITION.BOTTOM_RIGHT,
      });

      props.setLoading(false);
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
      <ToastContainer />
    </div>
  );
}
export default FilmCard;
