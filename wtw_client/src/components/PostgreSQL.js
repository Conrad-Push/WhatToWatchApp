import { useEffect, useState } from "react";
import axios from "axios";
import Card from './Card';


function PostgreSQL() {

    const [films, setFilms] = useState([]);

    useEffect(() => {
        axios
            .get(`/films/`)
            .then(function (response) {
                // console.log(response.data);
                setFilms(response.data)
            })
            .catch(function (error) {
                console.log(error);
            });
    }, []);


    return (
        <div className="App-header">
            <div className='title'>
                PostgreSQL
            </div>
            <Card
                films={films}
                film_id={films.film_id}
            />
        </div>
    );
}
export default PostgreSQL;