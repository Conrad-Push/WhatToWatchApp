import axios from "axios";

function deleteFilm(props) {
  const film_id = props.film_id;

  axios
    .delete(`/films/${film_id}`)
    .then(function (response) {})
    .catch(function (error) {
      console.log(error);
    });
}
export default deleteFilm;
