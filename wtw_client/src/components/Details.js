import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import axios from "axios";

function Details() {
    const [films, setFilms] = useState([]);
    const { film_id } = useParams();

    useEffect(() => {
        axios
            .get(`/films/${film_id}`)
            // .get(`/films/3`)
            .then(function (response) {
                console.log(response.data);
                setFilms(response.data)
            })
            .catch(function (error) {
                console.log(error);
            });
    }, []);

    return (
        <div className="App-header">
            {/* <div className='box'>
                <div className='list'>
                    <h2><b>{films.title}</b></h2>
                </div>
            </div> */}
            <div className='box'>
                <div className='film-details'>
                    <div className="photo-frame">
                        <img className="photo-details" src={films.img_url} />
                    </div>
                    <div>
                        <div id="film-title">
                            {films.title}
                        </div>
                        <div className="film-description">
                            <div>
                                <div>
                                    <b>Rating:</b> {films.rate}
                                </div>
                                {/* <p><b>Director:</b> {films.director.name}</p> */}
                                <div classname="description">
                                    <b>Description:</b> Tutaj baaaaaaaaaaaaaaaaaaaaaaardzo długi  opis
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    )
}
export default Details;