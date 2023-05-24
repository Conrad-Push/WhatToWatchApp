import { useNavigate } from "react-router-dom";

function Card(props) {

    const navigate = useNavigate();
    const films = props.films
    
    return (
        <div>
            <h1>Films list</h1>
            <ul>
                {films.map(film => (
                    <div key={film.film_id}>
                        <div className='box'>
                            <div className='list'>
                                {/* <div onClick={() => { navigate(`/details/${films.film_id}`); }}> */}
                                <div onClick={() => { navigate(`/details/${film.film_id}`); }}>
                                    <div className='card-looks'>
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
                        </div>
                    </div>
                ))}
            </ul>
        </div>
    );



}
export default Card;